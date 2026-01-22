import json
import cherrypy
import urllib

from models.branch_office import BranchOffice
from models.client import Client
from models.invoice_document import InvoiceDocument
from models.product_unit import ProductUnit

from utils.query import Query
from utils.singleton_meta import MetaConfig
from utils.decorators import tools

from helpers.notification import Notification


class MapHelpers(object):
    def __init__(self):
        pass

    def init(self, mapper=None):
        mapper.connect(
            "send_signed_invoice",
            "/helper/send-signed-invoice/{invoice_id}",
            controller=self,
            action="send_signed_invoice",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "evaluate_new_product_unit",
            "/helper/evaluate-new-product-unit",
            controller=self,
            action="evaluate_new_product_unit",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "evaluate_product_unit_for_disposal",
            "/helper/evaluate-product-unit-stock-out",
            controller=self,
            action="evaluate_product_unit_for_disposal",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "evaluate_product_unit_for_sell",
            "/helper/evaluate-product-unit-to-sell",
            controller=self,
            action="evaluate_product_unit_for_sell",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def send_signed_invoice(self, **kwargs):
        # Get body content
        invoice_id = kwargs.get("invoice_id", None)

        conn = InvoiceDocument().get_connection()
        query = Query(model=InvoiceDocument())
        document = query.where({"invoice_id": invoice_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not found")

        document = document.as_dict()
        document["branch"] = (
            BranchOffice().where({"branch_id": document["branch_id"]}).one_or_none(conn=conn).as_dict()
        )

        document["client"] = Client().where({"client_id": document["client_id"]}).one_or_none(conn=conn).as_dict()

        # bcc_emails = (
        # 	BranchOfficeEmail()
        # 	.where(
        # 		{'branch_id': document['branch_id']},
        # 		{'status': 'active'}
        # 	).order_by(
        # 		['email']
        # 	).all(
        # 		conn = conn,
        # 		collection=False
        # 	)
        # )
        bcc_emails = []

        meta = MetaConfig.instance()
        settings = meta.get_config("settings")
        url = "http://{server}/{endpoint}?{args}"
        try:
            # This urlencodes your data (that's why we need to import urllib at the top)
            query_args = urllib.parse.urlencode(
                {
                    "action": json.dumps(
                        {
                            "classe": "ErpWesmexico",
                            "method": "getSignedInvoice",
                            "is_static": "true",
                            "params": {"invoice_id": invoice_id},
                        }
                    )
                }
            )

            req = urllib.request.Request(
                url=url.format(
                    server=settings["pdf-reports-host"],
                    endpoint="data.php",
                    args=query_args,
                ),
                headers={
                    "Access-Token": cherrypy.request.headers.get("Access-Token"),
                    "Client-Identifier": cherrypy.request.headers.get("Client-Identifier"),
                    "Authorization": cherrypy.request.headers.get("Authorization"),
                },
            )
            result = urllib.request.urlopen(req)
            response = json.loads(result.read().decode("utf-8"))

            # download report
            req = urllib.request.Request(
                url=url.format(
                    server=settings["pdf-reports-host"],
                    endpoint="download.php",
                    args=urllib.parse.urlencode({"filename": response["report_name"]}),
                ),
                headers={
                    "Access-Token": cherrypy.request.headers.get("Access-Token"),
                    "Client-Identifier": cherrypy.request.headers.get("Client-Identifier"),
                    "Authorization": cherrypy.request.headers.get("Authorization"),
                },
            )
            report = urllib.request.urlopen(req)

        except urllib.error.HTTPError as e:
            raise cherrypy.HTTPError(e.code, e.reason)

        notification = Notification()
        notification.send_signed_invoice(
            {
                "report": report,
                "report_name": response["report_name"],
                "document": document,
                "bcc": [entry["email"] for entry in bcc_emails],
            }
        )

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["product_id", "uid"])
    def evaluate_new_product_unit(self, **kwargs):
        body = cherrypy.request.json

        unit = ProductUnit().where({"product_id": body["product_id"]}, {"uid": body["uid"]}).one_or_none()

        if not unit:
            return {}

        raise cherrypy.HTTPError(406, json.dumps({"code": 101, "msg": "existing product unit uid"}))

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["product_id", "uid"])
    def evaluate_product_unit_for_disposal(self, **kwargs):
        body = cherrypy.request.json

        unit = ProductUnit().where({"product_id": body["product_id"]}, {"uid": body["uid"]}).one_or_none()

        if not unit:
            raise cherrypy.HTTPError(406, json.dumps({"code": 404, "msg": "existing product unit uid"}))

        if unit.status not in ["active"]:
            raise cherrypy.HTTPError(406, json.dumps({"code": 102, "msg": "existing product unit uid"}))

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["product_id", "uid"])
    def evaluate_product_unit_for_sell(self, **kwargs):
        body = cherrypy.request.json

        unit = ProductUnit().where({"product_id": body["product_id"]}, {"uid": body["uid"]}).one_or_none()

        if not unit:
            raise cherrypy.HTTPError(406, json.dumps({"code": 404, "msg": "existing product unit uid"}))

        if unit.status not in ["active"]:
            raise cherrypy.HTTPError(406, json.dumps({"code": 102, "msg": "existing product unit uid"}))

        return {}
