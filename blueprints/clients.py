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
from models.bank_account import BankAccount
from models.client import Client
from models.client_contact import ClientContact


class MapClients(object):
    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_clients",
            "/catalog/clients",
            controller=self,
            action="get_clients",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_client_by_id",
            "/catalog/client/{client_id}",
            controller=self,
            action="get_client_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_client",
            "/catalog/client/{client_id}",
            controller=self,
            action="save_client",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_client",
            "/catalog/client/{client_id}",
            controller=self,
            action="delete_client",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_client_contacts",
            "/catalog/client/{client_id}/contacts",
            controller=self,
            action="get_client_contacts",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_client_contact_by_id",
            "/catalog/client/{client_id}/contact/{contact_id}",
            controller=self,
            action="get_client_contact_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_client_contact",
            "/catalog/client/{client_id}/contact/{contact_id}",
            controller=self,
            action="save_client_contact",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_client_contact",
            "/catalog/client/{client_id}/contact/{contact_id}",
            controller=self,
            action="delete_client_contact",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_clients(self, **kwargs):
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

        conn = Client().get_connection()
        query = Query(model=Client())
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
    def get_client_by_id(self, **kwargs):
        # Get body content
        client_id = kwargs.get("client_id", None)

        conn = Client().get_connection()
        client = Client().where(_OR({"client_id": client_id}, {"taxpayer_id": client_id})).one_or_none(conn=conn)

        if client is None:
            raise cherrypy.HTTPError(404, "Not Found")

        category = Category().where({"category_id": client.category_id}).one_or_none(conn=conn)

        state = State().where({"state_id": client.state_id}).one_or_none(conn=conn)

        municipality = (
            Municipality()
            .where(
                {"state_id": client.state_id},
                {"municipality_id": client.municipality_id},
            )
            .one_or_none(conn=conn)
        )

        locality = (
            Locality()
            .where(
                {"state_id": client.state_id},
                {"municipality_id": client.municipality_id},
                {"locality_id": client.locality_id},
            )
            .one_or_none(conn=conn)
        )

        account = (
            BankAccount()
            .where(
                {"associated_with": "client"},
                {"associated_id": client_id},
                {"is_default": 1},
            )
            .one_or_none(conn=conn)
        )

        documents = (
            ImageDocument()
            .where({"transaction_id": client_id}, {"origin": "client-document"})
            .order_by(["index"])
            .all(collection=False, ignore_limit=True, conn=conn)
        )

        client = client.as_dict()
        client["bank_account"] = account.as_dict() if account else None
        client["category"] = category.as_dict()
        client["state"] = state.as_dict()
        client["municipality"] = municipality.as_dict()
        client["locality"] = locality.as_dict()
        client["documents"] = documents

        return client

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
            "phone",
            "-email",
            "-cell_phone",
            "-references",
            "documents",
            "status",
        ]
    )
    def save_client(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        client_id = body.get("client_id", None)

        conn = Client().get_connection()
        client = Client().where({"client_id": client_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            is_new = False
            if client is None:
                is_new = True
                body["code"] = Serie.generate(reference="general", key="clients", conn=conn)
                client = Client()
                client.created_at = datetime.utcnow()

            client.set_attrs(body, validate_unknown=False)
            client.updated_at = datetime.utcnow()
            client.insert(conn=conn) if is_new else client.update(conn=conn)

            sql = (
                """
                    DELETE FROM `{table}`
                    WHERE
                        `transaction_id` = %s
                """
            ).format(table=ImageDocument()._TABLE)

            args = [client_id]
            conn.execute(sql, *args, connection=None)

            for index, item in enumerate(body["documents"]):
                document = ImageDocument()
                document.transaction_id = client_id
                document.document_id = f"{client_id}-{index}"
                document.index = index
                document.origin = "client-document"
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
    def delete_client(self, **kwargs):
        # Get body content
        client_id = kwargs.get("client_id", None)

        conn = Client().get_connection()
        client = Client().where({"client_id": client_id}).one_or_none(conn=conn)

        if client is None:
            raise cherrypy.HTTPError(404, "Not Found")

        client.status = "inactive"
        client.updated_at = datetime.utcnow()
        client.update(conn=conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_client_contacts(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        client_id = kwargs.get("client_id")
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [
            {"client_id": client_id},
            _OR(
                {"code": look_for, "op": "like"},
                {"name": look_for, "op": "like"},
                {"email": look_for, "op": "like"},
            ),
        ]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = ClientContact().get_connection()
        query = Query(model=ClientContact())
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
    def get_client_contact_by_id(self, **kwargs):
        # Get body content
        client_id = kwargs.get("client_id", None)
        contact_id = kwargs.get("contact_id", None)

        conn = ClientContact().get_connection()
        contact = (
            ClientContact()
            .where(
                {"client_id": client_id},
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
    def save_client_contact(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        client_id = body.get("client_id", None)
        contact_id = body.get("contact_id", None)

        conn = ClientContact().get_connection()
        client = ClientContact().where({"client_id": client_id}, {"contact_id": contact_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            is_new = False
            if client is None:
                is_new = True
                body["code"] = Serie.generate(
                    reference="client_{}".format(body.get("client_id")),
                    key="contacts",
                    conn=conn,
                )
                client = ClientContact()
                client.created_at = datetime.utcnow()

            client.set_attrs(body)
            client.updated_at = datetime.utcnow()
            client.insert(conn=conn) if is_new else client.update(conn=conn)
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
    def delete_client_contact(self, **kwargs):
        # Get kwargs content
        client_id = kwargs.get("client_id", None)
        contact_id = kwargs.get("contact_id", None)

        conn = ClientContact().get_connection()
        client = ClientContact().where({"client_id": client_id}, {"contact_id": contact_id}).one_or_none(conn=conn)

        if client is None:
            raise cherrypy.HTTPError(404, "Not Found")

        client.status = "inactive"
        client.updated_at = datetime.utcnow()
        client.update(conn=conn)

        return {}
