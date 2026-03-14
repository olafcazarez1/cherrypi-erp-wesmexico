import cherrypy
import pymysql

from datetime import datetime

from utils.decorators import tools
from utils.utils import Utils
from utils.query import _OR
from utils.query import Query

from models.state import State
from models.locality import Locality
from models.municipality import Municipality

from models.image_document import ImageDocument
from models.serie import Serie
from models.category import Category
from models.supplier import Supplier
from models.supplier_setting import SupplierSetting
from models.supplier_contact import SupplierContact
from models.bank_account import BankAccount


class MapSuppliers(object):
    def __init__(self):
        pass

    def init(self, mapper):

        mapper.connect(
            "get_suppliers",
            "/catalog/suppliers",
            controller=self,
            action="get_suppliers",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_supplier_by_id",
            "/catalog/supplier/{supplier_id}",
            controller=self,
            action="get_supplier_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_supplier",
            "/catalog/supplier/{supplier_id}",
            controller=self,
            action="save_supplier",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_supplier",
            "/catalog/supplier/{supplier_id}",
            controller=self,
            action="delete_supplier",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_supplier_contacts",
            "/catalog/supplier/{supplier_id}/contacts",
            controller=self,
            action="get_supplier_contacts",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_supplier_contact_by_id",
            "/catalog/supplier/{supplier_id}/contact/{contact_id}",
            controller=self,
            action="get_supplier_contact_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_supplier_contact",
            "/catalog/supplier/{supplier_id}/contact/{contact_id}",
            controller=self,
            action="save_supplier_contact",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_supplier_contact",
            "/catalog/supplier/{supplier_id}/contact/{contact_id}",
            controller=self,
            action="delete_supplier_contact",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_suppliers(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [
            _OR(
                {"code": look_for, "op": "like"},
                {"legal_name": look_for, "op": "like"},
                {"trade_name": look_for, "op": "like"},
            )
        ]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = Supplier().get_connection()
        query = Query(model=Supplier())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code", "legal_name"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_supplier_by_id(self, **kwargs):

        # Get body content
        supplier_id = kwargs.get("supplier_id", None)

        conn = Supplier().get_connection()
        supplier = Supplier().where({"supplier_id": supplier_id}).one_or_none(conn=conn)

        if supplier is None:
            raise cherrypy.HTTPError(404, "Not Found")

        category = Category().where({"category_id": supplier.category_id}).one_or_none(conn=conn)

        state = State().where({"state_id": supplier.state_id}).one_or_none(conn=conn)

        municipality = (
            Municipality()
            .where(
                {"state_id": supplier.state_id},
                {"municipality_id": supplier.municipality_id},
            )
            .one_or_none(conn=conn)
        )

        locality = (
            Locality()
            .where(
                {"state_id": supplier.state_id},
                {"municipality_id": supplier.municipality_id},
                {"locality_id": supplier.locality_id},
            )
            .one_or_none(conn=conn)
        )

        account = (
            BankAccount()
            .where(
                {"associated_with": "supplier"},
                {"associated_id": supplier_id},
                {"is_default": 1},
            )
            .one_or_none(conn=conn)
        )

        settings = (
            SupplierSetting()
            .where(
                {"supplier_id": supplier_id},
            )
            .one_or_none(conn=conn)
        )

        documents = (
            ImageDocument()
            .where({"transaction_id": supplier_id}, {"origin": "supplier-document"})
            .order_by(["index"])
            .all(collection=False, ignore_limit=True, conn=conn)
        )

        supplier = supplier.as_dict()
        supplier["bank_account"] = account.as_dict() if account else None
        supplier["category"] = category.as_dict()
        supplier["state"] = state.as_dict()
        supplier["municipality"] = municipality.as_dict()
        supplier["locality"] = locality.as_dict()
        supplier["settings"] = settings.as_dict() if settings else {}
        supplier["documents"] = documents

        return supplier

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
            "email",
            "phone",
            "-cell_phone",
            "-references",
            "documents",
            "status",
        ]
    )
    def save_supplier(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        supplier_id = body.get("supplier_id", None)

        conn = Supplier().get_connection()
        supplier = Supplier().where({"supplier_id": supplier_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            is_new = False
            if supplier is None:
                is_new = True
                body["code"] = Serie.generate(reference="general", key="suppliers", conn=conn)
                supplier = Supplier()
                supplier.created_at = datetime.utcnow()

            supplier.set_attrs(body, validate_unknown=False)
            supplier.updated_at = datetime.utcnow()
            supplier.insert(conn=conn) if is_new else supplier.update(conn=conn)

            sql = (
                """
                    DELETE FROM `{table}`
                    WHERE
                        `transaction_id` = %s
                """
            ).format(table=ImageDocument()._TABLE)

            args = [supplier_id]
            conn.execute(sql, *args, connection=None)

            for index, item in enumerate(body["documents"]):
                document = ImageDocument()
                document.transaction_id = supplier_id
                document.document_id = f"{supplier_id}-{index}"
                document.index = index
                document.origin = "supplier-document"
                document.path = item
                document.created_at = datetime.utcnow()
                document.updated_at = datetime.utcnow()
                document.update_or_insert(conn=conn)

            if "settings" in body:
                setting = SupplierSetting()
                setting.created_at = datetime.utcnow()
                setting.set_attrs(body["settings"], validate_unknown=False)
                setting.updated_at = datetime.utcnow()
                setting.update_or_insert(conn=conn)

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
    def delete_supplier(self, **kwargs):

        # Get body content
        supplier_id = kwargs.get("supplier_id", None)

        conn = Supplier().get_connection()
        supplier = Supplier().where({"supplier_id": supplier_id}).one_or_none(conn=conn)

        if supplier is None:
            raise cherrypy.HTTPError(404, "Not Found")

        supplier.status = "inactive"
        supplier.updated_at = datetime.utcnow()
        supplier.update(conn=conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_supplier_contacts(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        supplier_id = kwargs.get("supplier_id")
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [
            {"supplier_id": supplier_id},
            _OR(
                {"code": look_for, "op": "like"},
                {"name": look_for, "op": "like"},
                {"email": look_for, "op": "like"},
            ),
        ]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = SupplierContact().get_connection()
        query = Query(model=SupplierContact())
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
    def get_supplier_contact_by_id(self, **kwargs):

        # Get body content
        supplier_id = kwargs.get("supplier_id", None)
        contact_id = kwargs.get("contact_id", None)

        conn = SupplierContact().get_connection()
        contact = (
            SupplierContact()
            .where(
                {"supplier_id": supplier_id},
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
    def save_supplier_contact(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        supplier_id = body.get("supplier_id", None)
        contact_id = body.get("contact_id", None)

        conn = SupplierContact().get_connection()
        supplier = (
            SupplierContact().where({"supplier_id": supplier_id}, {"contact_id": contact_id}).one_or_none(conn=conn)
        )

        try:
            conn.begin(conn)

            is_new = False
            if supplier is None:
                is_new = True
                body["code"] = Serie.generate(
                    reference="supplier_{}".format(body.get("supplier_id")),
                    key="contacts",
                    conn=conn,
                )
                supplier = SupplierContact()
                supplier.created_at = datetime.utcnow()

            supplier.set_attrs(body)
            supplier.updated_at = datetime.utcnow()
            supplier.insert(conn=conn) if is_new else supplier.update(conn=conn)
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
    def delete_supplier_contact(self, **kwargs):

        # Get kwargs content
        supplier_id = kwargs.get("supplier_id", None)
        contact_id = kwargs.get("contact_id", None)

        conn = SupplierContact().get_connection()
        supplier = (
            SupplierContact().where({"supplier_id": supplier_id}, {"contact_id": contact_id}).one_or_none(conn=conn)
        )

        if supplier is None:
            raise cherrypy.HTTPError(404, "Not Found")

        supplier.status = "inactive"
        supplier.updated_at = datetime.utcnow()
        supplier.update(conn=conn)

        return {}
