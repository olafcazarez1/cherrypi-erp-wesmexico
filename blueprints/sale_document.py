import cherrypy

from datetime import datetime
from pytz import timezone

from utils.decorators import tools
from utils.query import _OR, _AND, Query
from utils.utils import Utils
from utils.convert import Convert

from models.state import State
from models.locality import Locality
from models.municipality import Municipality

from models.serie import Serie
from models.product_unit import ProductUnit
from models.sale_document import SaleDocument
from models.sale_document_product import SaleDocumentProduct
from models.sale_document_product_unit import SaleDocumentProductUnit
from models.sale_document_tax import SaleDocumentTax
from models.delivery_address import DeliveryAddress
from models.document_payment import DocumentPayment
from models.document_invoice import DocumentInvoice
from models.invoice_document import InvoiceDocument

from models.user import User
from models.employee import Employee
from models.company import Company
from models.branch_office import BranchOffice
from models.warehouse import Warehouse
from models.client import Client
from models.product import Product
from models.measure import Measure
from models.tax import Tax

from models.brand import Brand
from models.brand_model import BrandModel
from models.version import Version


class MapSaleDocument(object):
    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_sales",
            "/sales-documents",
            controller=self,
            action="get_sales",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_document",
            "/sale-document/{document_id}",
            controller=self,
            action="save_document",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "get_document",
            "/sale-document/{document_id}",
            controller=self,
            action="get_document",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "cancel_document",
            "/sale-document/{document_id}",
            controller=self,
            action="cancel_document",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_document_balance",
            "/sale-document/{document_id}/balance",
            controller=self,
            action="get_document_balance",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_sales_delivery_addresses",
            "/sales-delivery-addresses",
            controller=self,
            action="get_sales_delivery_addresses",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_payments",
            "/documents-payments",
            controller=self,
            action="get_payments",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_document_payment",
            "/sale-document/{document_id}/payment/{payment_id}",
            controller=self,
            action="get_document_payment",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_document_payment",
            "/sale-document/{document_id}/payment/{payment_id}",
            controller=self,
            action="save_document_payment",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "cancel_document_payment",
            "/sale-document/{document_id}/payment/{payment_id}",
            controller=self,
            action="cancel_document_payment",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_sales(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 0)
        look_for = kwargs.get("look_for", "")
        start_date = kwargs.get("start_date", None)
        end_date = kwargs.get("end_date", None)
        filters = kwargs.get("filters", "[]")

        # include_payments = kwargs.get("include_payments", False)

        criterias = [
            {"code": look_for, "op": "like"},
            _AND(
                {"transaction_date": start_date, "op": "gte"},
                {"transaction_date": end_date, "op": "lte"},
            ),
        ]

        criterias = criterias + Utils().convert_filters(filters)

        conn = SaleDocument().get_connection()
        query = Query(model=SaleDocument())
        query.where(*criterias)

        if int(limit) >= 0 and int(offset) >= 0:
            query.limit(limit)
            query.offset(offset)

        query.order_by(["-transaction_date", "-code"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for document in result["results"]:
            document["user"] = User().where({"user_id": document["user_id"]}).one_or_none(conn=conn).as_dict()

            document["seller"] = (
                Employee().where({"employee_id": document["seller_id"]}).one_or_none(conn=conn).as_dict()
            )

            document["company"] = (
                Company().where({"company_id": document["company_id"]}).one_or_none(conn=conn).as_dict()
            )

            document["branch"] = (
                BranchOffice().where({"branch_id": document["branch_id"]}).one_or_none(conn=conn).as_dict()
            )

            document["client"] = Client().where({"client_id": document["client_id"]}).one_or_none(conn=conn).as_dict()

            # if include_payments:
            #     document["payments"] = (
            #         DocumentPayment()
            #         .where({"document_id": document["document_id"]})
            #         .limit(100)
            #         .order_by(["code"])
            #         .all(conn=conn, collection=False)
            #     )

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "document_id",
            "company_id",
            "branch_id",
            "warehouse_id",
            "user_id",
            "seller_id",
            "client_id",
            "currency",
            "exchange_rate",
            "amount",
            "subtotal",
            "discount",
            "taxes",
            "total",
            "transaction_method",
            "transaction_date",
            "transaction_status",
            "products",
            # "-payments",
        ]
    )
    def save_document(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        company_id = body.get("company_id", None)
        branch_id = body.get("branch_id", None)
        document_id = body.get("document_id", None)

        conn = SaleDocument().get_connection()
        document = SaleDocument().where({"document_id": document_id}).one_or_none(conn=conn)

        if document:
            raise cherrypy.HTTPError(423, "Document Locked")

        company = Company().where({"company_id": company_id}).one_or_none(conn=conn)
        branch = BranchOffice().where({"branch_id": branch_id}).one_or_none(conn=conn)

        if not company:
            raise cherrypy.HTTPError(400, "Invalid company")

        if not branch:
            raise cherrypy.HTTPError(400, "Invalid branch")

        try:
            conn.begin(conn)
            code = "V{serie}{branch}{date}{number}".format(
                serie=company.serie,
                branch=branch.code,
                date=Convert().datetime2str(dt=None, tz=timezone(branch.timezone), format="%d%m%y"),
                number=Serie.generate(reference="sale-document", key=branch_id, zfill=6, conn=conn),
            )

            document = SaleDocument()
            document.code = code
            document.set_attrs(body, validate_unknown=False)

            document.is_signed = False
            document.status = "active"
            document.created_at = datetime.utcnow()
            document.updated_at = datetime.utcnow()
            document.insert(conn=conn)

            for item in body.get("products", []):
                product = SaleDocumentProduct()
                product.document_id = document_id
                product.set_attrs(item, validate_unknown=False, ignore_restricted=True)
                product.taxes = item["tax"]
                measures = []

                if "measure" in item:
                    measures = [item["measure"]]

                if "measures" in item:
                    measures = item["measures"]

                for measure in measures:
                    product.measure_id = measure["measure_id"]
                    product.created_at = datetime.utcnow()
                    product.updated_at = datetime.utcnow()
                    product.insert(conn=conn)

                for tax in item["taxes"]:
                    product_tax = SaleDocumentTax()
                    product_tax.document_id = document_id
                    product_tax.set_attrs(tax, validate_unknown=False, ignore_restricted=True)
                    product_tax.created_at = datetime.utcnow()
                    product_tax.updated_at = datetime.utcnow()
                    product_tax.insert(conn=conn)

                for unit in item.get("units", []):
                    pu = (
                        ProductUnit()
                        .where({"product_id": product.product_id}, {"uid": unit["uid"]})
                        .one_or_none(conn=conn)
                    )
                    if not pu:
                        cherrypy.HTTPError(
                            500,
                            "Problem saving data: {} {}".format(
                                "Invalid Unit",
                                unit["uid"],
                            ),
                        )
                    pu.status = "sold"
                    pu.update(conn=conn)

                    io_unit = SaleDocumentProductUnit()
                    io_unit.document_id = document.document_id
                    io_unit.product_id = product.product_id
                    io_unit.measure_id = product.measure_id
                    io_unit.unit_id = pu.unit_id
                    io_unit.uid = pu.uid
                    io_unit.created_at = datetime.utcnow()
                    io_unit.updated_at = datetime.utcnow()
                    io_unit.insert(conn=conn)

            # for item in body.get("payments", []):
            #     code = "P{prefix}{date}{number}".format(
            #         prefix=branch.serie,
            #         date=Convert().datetime2str(
            #             dt=None, tz=timezone(branch.timezone), format="%d%m%y"
            #         ),
            #         number=Serie.generate(
            #             reference="document-payment", key=branch_id, zfill=6, conn=conn
            #         ),
            #     )

            #     payment = DocumentPayment()
            #     payment.reference = document.code
            #     payment.code = code
            #     payment.set_attrs(item, validate_unknown=False)
            #     payment.is_signed = False
            #     payment.status = "active"
            #     payment.created_at = datetime.utcnow()
            #     payment.updated_at = datetime.utcnow()
            #     payment.insert(conn=conn)

            conn.commit(conn)
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return document.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_document(self, **kwargs):
        document_id = kwargs.get("document_id", "")

        conn = SaleDocument().get_connection()
        query = Query(model=SaleDocument())
        document = query.where({"document_id": document_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not found")

        document = document.as_dict()
        document["company"] = Company().where({"company_id": document["company_id"]}).one_or_none(conn=conn).as_dict()

        document["branch"] = (
            BranchOffice().where({"branch_id": document["branch_id"]}).one_or_none(conn=conn).as_dict()
        )

        document["branch"]["state"] = (
            State().where({"state_id": document["branch"]["state_id"]}).one_or_none(conn=conn).as_dict()
        )

        document["branch"]["municipality"] = (
            Municipality()
            .where(
                {"state_id": document["branch"]["state_id"]},
                {"municipality_id": document["branch"]["municipality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        document["branch"]["locality"] = (
            Locality()
            .where(
                {"state_id": document["branch"]["state_id"]},
                {"municipality_id": document["branch"]["municipality_id"]},
                {"locality_id": document["branch"]["locality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        document["warehouse"] = (
            Warehouse().where({"warehouse_id": document["warehouse_id"]}).one_or_none(conn=conn).as_dict()
        )

        document["client"] = Client().where({"client_id": document["client_id"]}).one_or_none(conn=conn).as_dict()

        document["client"]["state"] = (
            State().where({"state_id": document["client"]["state_id"]}).one_or_none(conn=conn).as_dict()
        )

        document["client"]["municipality"] = (
            Municipality()
            .where(
                {"state_id": document["client"]["state_id"]},
                {"municipality_id": document["client"]["municipality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        document["client"]["locality"] = (
            Locality()
            .where(
                {"state_id": document["client"]["state_id"]},
                {"municipality_id": document["client"]["municipality_id"]},
                {"locality_id": document["client"]["locality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        document["user"] = User().where({"user_id": document["user_id"]}).one_or_none(conn=conn).as_dict()

        document["seller"] = Employee().where({"employee_id": document["seller_id"]}).one_or_none(conn=conn).as_dict()

        # document["delivery_to"] = {}
        # delivery_to = (
        #     DeliveryAddress().where({"document_id": document_id}).one_or_none()
        # )
        # if delivery_to:
        #     document["delivery_to"] = delivery_to.as_dict()
        #     document["delivery_to"]["state"] = document["branch"]["state"]
        #     document["delivery_to"]["municipality"] = document["branch"]["municipality"]
        #     document["delivery_to"]["locality"] = document["branch"]["locality"]

        items = SaleDocumentProduct().where({"document_id": document["document_id"]}).all(conn=conn, collection=False)

        # prepare products
        products = {}
        for item in items:
            if item["product_id"] not in products:
                product = Product().where({"product_id": item["product_id"]}).one_or_none(conn=conn).as_dict()
                product["brand"] = Brand().where({"brand_id": product["brand_id"]}).one_or_none(conn=conn).as_dict()
                product["model"] = (
                    BrandModel()
                    .where(
                        {"brand_id": product["brand_id"]},
                        {"model_id": product["model_id"]},
                    )
                    .one_or_none(conn=conn)
                    .as_dict()
                )
                product["measures"] = []
            else:
                product = products[item["product_id"]]

            measure = Measure().where({"measure_id": item["measure_id"]}).one_or_none(conn=conn).as_dict()

            measure.update(item)

            units = (
                SaleDocumentProductUnit()
                .where(
                    {"document_id": document_id},
                    {"product_id": product["product_id"]},
                    {"measure_id": measure["measure_id"]},
                )
                .all(conn=conn, collection=False)
            )

            measure["units"] = []
            for entry in units:
                unit = ProductUnit().where({"unit_id": entry["unit_id"]}).one_or_none(conn=conn).as_dict()
                unit["brand"] = product["brand"]
                unit["model"] = product["model"]
                unit["version"] = (
                    Version()
                    .where(
                        {"brand_id": unit["brand_id"]},
                        {"model_id": unit["model_id"]},
                        {"version_id": unit["version_id"]},
                    )
                    .one_or_none(conn=conn)
                    .as_dict()
                )
                unit.update(entry)
                measure["units"].append(unit)
            measure["units"] = sorted(measure["units"], key=lambda i: i["uid"])

            product["measures"].append(measure)
            products[item["product_id"]] = product

        products = list(products.values())
        for product in products:
            product["measures"] = sorted(product["measures"], key=lambda i: i["name"])

            # Get Product taxes
            taxes = (
                SaleDocumentTax()
                .where({"document_id": document_id}, {"product_id": product["product_id"]})
                .all(conn=conn, collection=False)
            )

            # Set taxes
            product["taxes"] = []
            for item in taxes:
                tax = Tax().where({"tax_id": item["tax_id"]}).one_or_none(conn=conn).as_dict()
                tax.update(item)
                product["taxes"].append(tax)

            product["taxes"] = sorted(product["taxes"], key=lambda i: i["name"])

        document["products"] = sorted(products, key=lambda i: i["name"])

        document["payments"] = (
            DocumentPayment()
            .where({"document_id": document_id})
            .limit(100)
            .order_by(["created_at", "code"])
            .all(conn=conn, collection=False)
        )

        document["balance"] = self.get_document_balance(**kwargs)

        items = (
            DocumentInvoice()
            .where({"document_id": document["document_id"]})
            .limit(100000)
            .all(conn=conn, collection=False)
        )

        related_documents = []
        for item in items:
            related = (
                InvoiceDocument()
                .where(
                    {"invoice_id": item["invoice_id"]},
                )
                .one_or_none(conn=conn)
            )

            if related:
                related_documents.append(related.as_dict())

        document["related_documents"] = sorted(related_documents, key=lambda i: i["code"])

        return document

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    def cancel_document(self, **kwargs):
        document_id = kwargs.get("document_id", None)

        conn = SaleDocument().get_connection()
        document = SaleDocument().where({"document_id": document_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not Found")

        # # Evaluate if the document is signed/invoiced
        # invoices = DocumentInvoice().where({"document_id": document_id}).all(conn=conn)

        # invoices_ids = [item.invoice_id for item in invoices.all()]
        # items = (
        #     InvoiceDocument()
        #     .where(
        #         {"invoice_id": invoices_ids, "op": "in"},
        #         {"status": ["pending", "signed"], "op": "in"},
        #     )
        #     .all(conn=conn, collection=False)
        # )

        # if len(items) > 0:
        #     raise cherrypy.HTTPError(423, "Document locked")

        try:
            conn.begin(conn)

            document.status = "inactive"
            document.updated_at = datetime.utcnow()
            document.update(conn=conn)

            units = (
                ProductUnit()
                .where(
                    {
                        "unit_id": (
                            SaleDocumentProductUnit()
                            .fields(["unit_id"])
                            .where(
                                {"document_id": document_id},
                            )
                        ).sql(remove_offset_limit=True),
                        "op": "in",
                    }
                )
                .all(conn=conn, collection=True)
            )
            for unit in units.all():
                unit.status = "active"
                unit.update(conn=conn)

            # payments = (
            #     DocumentPayment().where({"document_id": document_id}).all(conn=conn)
            # )

            # for payment in payments.all():
            #     payment.status = "inactive"
            #     payment.updated_at = datetime.utcnow()
            #     payment.update(conn=conn)

            conn.commit(conn)
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_sales_delivery_addresses(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 0)
        look_for = kwargs.get("look_for", "")
        start_date = kwargs.get("start_date", None)
        end_date = kwargs.get("end_date", None)
        filters = kwargs.get("filters", "[]")

        criterias = [
            _OR({"phone": look_for, "op": "like"}, {"name": look_for, "op": "like"}),
            _AND(
                {"created_at": start_date, "op": "gte"},
                {"created_at": end_date, "op": "lte"},
            ),
        ]

        criterias = criterias + Utils().convert_filters(filters)

        conn = DeliveryAddress().get_connection()
        query = Query(model=DeliveryAddress())
        query.where(*criterias)

        if int(limit) >= 0 and int(offset) >= 0:
            query.limit(limit)
            query.offset(offset)

        query.order_by(["-created_at"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for document in result["results"]:
            document["state"] = State().where({"state_id": document["state_id"]}).one_or_none(conn=conn).as_dict()

            document["municipality"] = (
                Municipality()
                .where(
                    {"state_id": document["state_id"]},
                    {"municipality_id": document["municipality_id"]},
                )
                .one_or_none(conn=conn)
                .as_dict()
            )

            document["locality"] = (
                Locality()
                .where(
                    {"state_id": document["state_id"]},
                    {"municipality_id": document["municipality_id"]},
                    {"locality_id": document["locality_id"]},
                )
                .one_or_none(conn=conn)
                .as_dict()
            )

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_document_balance(self, **kwargs):
        document_id = kwargs.get("document_id", None)

        conn = SaleDocument().get_connection()
        document = SaleDocument().where({"document_id": document_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Sale Document Not Found")

        payments = (
            DocumentPayment()
            .where(
                {"document_id": document_id},
                {"status": "active"},
            )
            .all(conn=conn, collection=False)
        )

        paid = sum(item.get("amount") for item in payments) or 0
        balance = round(document.total - paid, 2)

        if balance < 0:
            balance = 0.0

        return {
            "document_id": document.document_id,
            "code": document.code,
            "transaction_status": document.transaction_status,
            "currency": document.currency,
            "exchange_rate": float(document.exchange_rate or 1),
            "document_total": float(document.total or 0),
            "paid": paid,
            "balance": balance,
            "payments_count": len(payments),
            "can_collect": balance > 0,
        }

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_payments(self, **kwargs):
        token = kwargs.get("token")

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 0)
        look_for = kwargs.get("look_for", "")
        start_date = kwargs.get("start_date", None)
        end_date = kwargs.get("end_date", None)
        filters = kwargs.get("filters", "[]")

        criterias = [
            _OR({"code": look_for, "op": "like"}, {"reference": look_for, "op": "like"}),
            _AND(
                {"transaction_date": start_date, "op": "gte"},
                {"transaction_date": end_date, "op": "lte"},
            ),
        ]

        criterias = criterias + Utils().convert_filters(filters)

        #
        # Users with specific branches should be limited
        #
        branches = User().where({"user_id": token.user_id}).one_or_none().get_branches(only_ids=True)

        if len(branches):
            criterias.append({"branch_id": branches, "op": "in"})

        conn = DocumentPayment().get_connection()
        query = Query(model=DocumentPayment())
        query.where(*criterias)

        if int(limit) >= 0 and int(offset) >= 0:
            query.limit(limit)
            query.offset(offset)

        query.order_by(["-transaction_date", "-code"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for document in result["results"]:
            document["user"] = User().where({"user_id": document["user_id"]}).one_or_none(conn=conn).as_dict()

            document["branch"] = (
                BranchOffice().where({"branch_id": document["branch_id"]}).one_or_none(conn=conn).as_dict()
            )

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_document_payment(self, **kwargs):
        payment_id = kwargs.get("payment_id", "")

        conn = DocumentPayment().get_connection()
        document = DocumentPayment().where({"payment_id": payment_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not found")

        return document.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "payment_id",
            "document_id",
            "user_id",
            "transaction_method",
            "previous_balance",
            "amount",
            "pay_with",
            "change",
            "balance",
            "currency",
            "exchange_rate",
            "transaction_date",
        ]
    )
    def save_document_payment(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        document_id = body.get("document_id", None)

        conn = SaleDocument().get_connection()
        document = SaleDocument().where({"document_id": document_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Sale Document Not Found")

        body["branch_id"] = document.branch_id
        branch = BranchOffice().where({"branch_id": document.branch_id}).one_or_none(conn=conn)

        payment = DocumentPayment()
        payment.set_attrs(body, validate_unknown=False)

        payments = (
            DocumentPayment()
            .where(
                {"document_id": document_id},
                {"status": "active"},
            )
            .all(conn=conn, collection=False)
        )

        paid = round(payment.amount + sum(item["amount"] for item in payments), 2)
        if paid > document.total:
            raise cherrypy.HTTPError(406, "Not Aceptable")

        try:
            conn.begin(conn)

            code = "P{prefix}{date}{number}".format(
                prefix=branch.serie or "",
                date=Convert().datetime2str(dt=None, tz=timezone(branch.timezone), format="%d%m%y"),
                number=Serie.generate(reference="document-payment", key=document.branch_id, zfill=6, conn=conn),
            )

            payment.code = code
            payment.reference = document.code
            payment.is_signed = False
            payment.status = "active"
            payment.created_at = datetime.utcnow()
            payment.updated_at = datetime.utcnow()
            payment.insert(conn=conn)

            if payment.balance == 0:
                document.transaction_status = "paid"
                document.update(conn=conn)

            conn.commit(conn)
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    def cancel_document_payment(self, **kwargs):
        document_id = kwargs.get("document_id", None)
        payment_id = kwargs.get("payment_id", None)

        conn = SaleDocument().get_connection()
        document = SaleDocument().where({"document_id": document_id}).one_or_none(conn=conn)
        if document is None:
            raise cherrypy.HTTPError(404, "Not Found")

        payment = DocumentPayment().where({"payment_id": payment_id}).one_or_none(conn=conn)
        if payment is None:
            raise cherrypy.HTTPError(404, "Not found")

        try:
            conn.begin(conn)

            document.transaction_status = "pending"
            document.update(conn=conn)

            payment.status = "inactive"
            payment.updated_at = datetime.utcnow()
            payment.update(conn=conn)

            conn.commit(conn)
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return {}
