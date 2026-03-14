import cherrypy
import pymysql

from datetime import datetime
from utils.decorators import tools
from utils.query import _OR, Query
from utils.utils import Utils

from models.state import State
from models.locality import Locality
from models.municipality import Municipality

from models.image_document import ImageDocument
from models.serie import Serie
from models.category import Category
from models.contractor import Contractor
from models.contractor_contact import ContractorContact
from models.bank_account import BankAccount
from models.project_contractor import ProjectContractor


class MapContractors(object):
    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_contractors",
            "/catalog/contractors",
            controller=self,
            action="get_contractors",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_contractor_by_id",
            "/catalog/contractor/{contractor_id}",
            controller=self,
            action="get_contractor_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_contractor",
            "/catalog/contractor/{contractor_id}",
            controller=self,
            action="save_contractor",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_contractor",
            "/catalog/contractor/{contractor_id}",
            controller=self,
            action="delete_contractor",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_contractor_contacts",
            "/catalog/contractor/{contractor_id}/contacts",
            controller=self,
            action="get_contractor_contacts",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_contractor_contact_by_id",
            "/catalog/contractor/{contractor_id}/contact/{contact_id}",
            controller=self,
            action="get_contractor_contact_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_contractor_contact",
            "/catalog/contractor/{contractor_id}/contact/{contact_id}",
            controller=self,
            action="save_contractor_contact",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_contractor_contact",
            "/catalog/contractor/{contractor_id}/contact/{contact_id}",
            controller=self,
            action="delete_contractor_contact",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_contractors(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        project_id = kwargs.get("project_id", None)
        filters = kwargs.get("filters", "[]")

        criterias = [
            _OR(
                {"code": look_for, "op": "like"},
                {"legal_name": look_for, "op": "like"},
                {"trade_name": look_for, "op": "like"},
            )
        ]

        if project_id:
            ###
            # Return the contractors associated to project
            ###
            criterias.append(
                {
                    "contractor_id": (
                        ProjectContractor()
                        .fields(["contractor_id"])
                        .where({"project_id": project_id})
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = Contractor().get_connection()
        query = Query(model=Contractor())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code", "legal_name"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        for contractor in result["results"]:
            category = Category().where({"category_id": contractor["category_id"]}).one_or_none()
            contractor["category"] = category.as_dict()

            documents = (
                ImageDocument()
                .where(
                    {"transaction_id": contractor["contractor_id"]},
                    {"path": ""},
                    {"origin": "contractor-document"},
                )
                .order_by(["index"])
                .all(collection=False, ignore_limit=True, conn=conn)
            )
            contractor["check"] = "negative" if documents else "positive"

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_contractor_by_id(self, **kwargs):

        # Get body content
        contractor_id = kwargs.get("contractor_id", None)

        conn = Contractor().get_connection()
        contractor = (
            Contractor()
            .where(_OR({"contractor_id": contractor_id}, {"taxpayer_id": contractor_id}))
            .one_or_none(conn=conn)
        )

        if contractor is None:
            raise cherrypy.HTTPError(404, "Not Found")

        category = Category().where({"category_id": contractor.category_id}).one_or_none(conn=conn)

        state = State().where({"state_id": contractor.state_id}).one_or_none(conn=conn)

        municipality = (
            Municipality()
            .where({"state_id": contractor.state_id}, {"municipality_id": contractor.municipality_id})
            .one_or_none(conn=conn)
        )

        locality = (
            Locality()
            .where(
                {"state_id": contractor.state_id},
                {"municipality_id": contractor.municipality_id},
                {"locality_id": contractor.locality_id},
            )
            .one_or_none(conn=conn)
        )

        account = (
            BankAccount()
            .where({"associated_with": "contractor"}, {"associated_id": contractor_id}, {"is_default": 1})
            .one_or_none(conn=conn)
        )

        documents = (
            ImageDocument()
            .where({"transaction_id": contractor_id}, {"origin": "contractor-document"})
            .order_by(["index"])
            .all(collection=False, ignore_limit=True, conn=conn)
        )

        contractor = contractor.as_dict()
        contractor["bank_account"] = account.as_dict() if account else None
        contractor["category"] = category.as_dict()
        contractor["state"] = state.as_dict()
        contractor["municipality"] = municipality.as_dict()
        contractor["locality"] = locality.as_dict()
        contractor["documents"] = documents

        return contractor

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "legal_name",
            "trade_name",
            "address_street",
            "address_external_number",
            "-address_internal_number",
            "neighborhood",
            "state_id",
            "municipality_id",
            "locality_id",
            "zip",
            "taxpayer_id",
            "tax_regime_id",
            "-repse",
            "phone",
            "-email",
            "-cell_phone",
            "-references",
            "-notes",
            "documents",
            "status",
        ]
    )
    def save_contractor(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        contractor_id = body.get("contractor_id", None)

        conn = Contractor().get_connection()
        contractor = Contractor().where({"contractor_id": contractor_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            is_new = False
            if contractor is None:
                is_new = True
                body["code"] = Serie.generate(reference="general", key="contractors", conn=conn)
                contractor = Contractor()
                contractor.created_at = datetime.utcnow()

            contractor.set_attrs(body, validate_unknown=False)
            contractor.updated_at = datetime.utcnow()
            contractor.insert(conn=conn) if is_new else contractor.update(conn=conn)

            sql = (
                """
                    DELETE FROM `{table}`
                    WHERE
                        `transaction_id` = %s
                """
            ).format(table=ImageDocument()._TABLE)

            args = [contractor_id]
            conn.execute(sql, *args, connection=None)

            for index, item in enumerate(body["documents"]):
                document = ImageDocument()
                document.transaction_id = contractor_id
                document.document_id = f"{contractor_id}-{index}"
                document.index = index
                document.origin = "contractor-document"
                document.path = item
                document.created_at = datetime.utcnow()
                document.updated_at = datetime.utcnow()
                document.update_or_insert(conn=conn)

            conn.commit(conn)
        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))
        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_contractor(self, **kwargs):

        # Get body content
        contractor_id = kwargs.get("contractor_id", None)

        conn = Contractor().get_connection()
        contractor = Contractor().where({"contractor_id": contractor_id}).one_or_none(conn=conn)

        if contractor is None:
            raise cherrypy.HTTPError(404, "Not Found")

        contractor.status = "inactive"
        contractor.updated_at = datetime.utcnow()
        contractor.update(conn=conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_contractor_contacts(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        contractor_id = kwargs.get("contractor_id")
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [
            {"contractor_id": contractor_id},
            _OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"}, {"email": look_for, "op": "like"}),
        ]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = ContractorContact().get_connection()
        query = Query(model=ContractorContact())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_contractor_contact_by_id(self, **kwargs):

        # Get body content
        contractor_id = kwargs.get("contractor_id", None)
        contact_id = kwargs.get("contact_id", None)

        conn = ContractorContact().get_connection()
        contact = (
            ContractorContact()
            .where(
                {"contractor_id": contractor_id},
                {"contact_id": contact_id},
            )
            .one_or_none(conn=conn)
        )

        if contact is None:
            raise cherrypy.HTTPError(404, "Not Found")

        return contact.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["name", "position", "email", "phone", "extension", "cell_phone", "status"])
    def save_contractor_contact(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        contractor_id = body.get("contractor_id", None)
        contact_id = body.get("contact_id", None)

        conn = ContractorContact().get_connection()
        contractor = (
            ContractorContact()
            .where({"contractor_id": contractor_id}, {"contact_id": contact_id})
            .one_or_none(conn=conn)
        )

        try:
            conn.begin(conn)

            is_new = False
            if contractor is None:
                is_new = True
                body["code"] = Serie.generate(
                    reference="contractor_{}".format(body.get("contract_id")), key="contacts", conn=conn
                )
                contractor = ContractorContact()
                contractor.created_at = datetime.utcnow()

            contractor.set_attrs(body)
            contractor.updated_at = datetime.utcnow()
            contractor.insert(conn=conn) if is_new else contractor.update(conn=conn)
            conn.commit(conn)
        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))
        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_contractor_contact(self, **kwargs):

        # Get kwargs content
        contractor_id = kwargs.get("contractor_id", None)
        contact_id = kwargs.get("contact_id", None)

        conn = ContractorContact().get_connection()
        contractor = (
            ContractorContact()
            .where({"contractor_id": contractor_id}, {"contact_id": contact_id})
            .one_or_none(conn=conn)
        )

        if contractor is None:
            raise cherrypy.HTTPError(404, "Not Found")

        contractor.status = "inactive"
        contractor.updated_at = datetime.utcnow()
        contractor.update(conn=conn)

        return {}
