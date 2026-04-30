import cherrypy

from datetime import datetime
from pytz import timezone

from utils.decorators import tools
from utils.query import _AND
from utils.query import Query
from utils.utils import Utils
from utils.convert import Convert

from models.serie import Serie
from models.company import Company
from models.branch_office import BranchOffice

from models.purchase_order_document import PurchaseOrderDocument
from models.purchase_order_document_product import PurchaseOrderDocumentProduct
from models.purchase_order_document_tax import PurchaseOrderDocumentTax

from models.user import User
from models.warehouse import Warehouse
from models.employee import Employee
from models.supplier import Supplier
from models.product import Product
from models.measure import Measure
from models.tax import Tax


class MapPurchaseOrderDocument(object):
    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_purchase_orders",
            "/purchase-orders",
            controller=self,
            action="get_purchase_orders",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_purchase_order",
            "/purchase-order/{purchase_order_id}",
            controller=self,
            action="save_purchase_order",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "get_purchase_order",
            "/purchase-order/{purchase_order_id}",
            controller=self,
            action="get_purchase_order",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "cancel_purchase_order",
            "/purchase-order/{purchase_order_id}",
            controller=self,
            action="cancel_purchase_order",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "patch_purchase_order",
            "/purchase-order/{purchase_order_id}",
            controller=self,
            action="patch_purchase_order",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_purchase_orders(self, **kwargs):
        result = {"results": [], "total_rows": 0}

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 0)
        look_for = kwargs.get("look_for", "")
        start_date = kwargs.get("start_date", None)
        end_date = kwargs.get("end_date", None)
        filters = kwargs.get("filters", "[]")

        criterias = [
            {"code": look_for, "op": "like"},
            _AND(
                {"transaction_date": start_date, "op": "gte"},
                {"transaction_date": end_date, "op": "lte"},
            ),
        ]

        criterias = criterias + Utils().convert_filters(filters)

        conn = PurchaseOrderDocument().get_connection()
        query = Query(model=PurchaseOrderDocument())
        query.where(*criterias)

        if int(limit) >= 0 and int(offset) >= 0:
            query.limit(limit)
            query.offset(offset)

        query.order_by(["-transaction_date", "-code"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for document in result["results"]:
            document["user"] = User().where({"user_id": document["user_id"]}).one_or_none(conn=conn).as_dict()
            document["employee"] = (
                Employee().where({"employee_id": document["employee_id"]}).one_or_none(conn=conn).as_dict()
            )
            document["company"] = (
                Company().where({"company_id": document["company_id"]}).one_or_none(conn=conn).as_dict()
            )
            document["branch"] = (
                BranchOffice().where({"branch_id": document["branch_id"]}).one_or_none(conn=conn).as_dict()
            )
            document["supplier"] = (
                Supplier().where({"supplier_id": document["supplier_id"]}).one_or_none(conn=conn).as_dict()
            )

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "purchase_order_id",
            "company_id",
            "branch_id",
            "warehouse_id",
            "user_id",
            "employee_id",
            "supplier_id",
            "currency",
            "exchange_rate",
            "amount",
            "subtotal",
            "discount",
            "taxes",
            "total",
            "transaction_date",
            "products",
        ]
    )
    def save_purchase_order(self, **kwargs):
        body = cherrypy.request.json

        purchase_order_id = body.get("purchase_order_id", None)
        company_id = body.get("company_id", None)
        branch_id = body.get("branch_id", None)

        conn = PurchaseOrderDocument().get_connection()
        document = PurchaseOrderDocument().where({"purchase_order_id": purchase_order_id}).one_or_none(conn=conn)

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

            code = "OC{serie}{branch}{date}{number}".format(
                serie=company.serie,
                branch=branch.code,
                date=Convert().datetime2str(dt=None, tz=timezone(branch.timezone), format="%d%m%y"),
                number=Serie.generate(reference="purchase-order", key=branch_id, zfill=6, conn=conn),
            )

            document = PurchaseOrderDocument()
            document.code = code
            document.set_attrs(body, validate_unknown=False)
            document.reference = body.get("reference", "")
            document.priority = body.get("priority", "medium")
            document.status = "new"
            document.created_at = datetime.utcnow()
            document.updated_at = datetime.utcnow()
            document.insert(conn=conn)

            for item in body.get("products", []):
                product = PurchaseOrderDocumentProduct()
                product.purchase_order_id = purchase_order_id
                product.set_attrs(item, validate_unknown=False, ignore_restricted=True)
                product.taxes = item.get("tax", item.get("taxes", 0.00))

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

                for tax in item.get("taxes", []):
                    product_tax = PurchaseOrderDocumentTax()
                    product_tax.purchase_order_id = purchase_order_id
                    product_tax.set_attrs(tax, validate_unknown=False, ignore_restricted=True)
                    product_tax.created_at = datetime.utcnow()
                    product_tax.updated_at = datetime.utcnow()
                    product_tax.insert(conn=conn)

            conn.commit(conn)

        except Exception as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return document.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_purchase_order(self, **kwargs):
        purchase_order_id = kwargs.get("purchase_order_id", "")

        conn = PurchaseOrderDocument().get_connection()
        document = (
            Query(model=PurchaseOrderDocument()).where({"purchase_order_id": purchase_order_id}).one_or_none(conn=conn)
        )

        if document is None:
            raise cherrypy.HTTPError(404, "Not found")

        document = document.as_dict()

        document["company"] = Company().where({"company_id": document["company_id"]}).one_or_none(conn=conn).as_dict()
        document["branch"] = (
            BranchOffice().where({"branch_id": document["branch_id"]}).one_or_none(conn=conn).as_dict()
        )
        document["warehouse"] = (
            Warehouse().where({"warehouse_id": document["warehouse_id"]}).one_or_none(conn=conn).as_dict()
        )
        document["supplier"] = (
            Supplier().where({"supplier_id": document["supplier_id"]}).one_or_none(conn=conn).as_dict()
        )
        document["user"] = User().where({"user_id": document["user_id"]}).one_or_none(conn=conn).as_dict()
        document["employee"] = (
            Employee().where({"employee_id": document["employee_id"]}).one_or_none(conn=conn).as_dict()
        )

        items = (
            PurchaseOrderDocumentProduct()
            .where({"purchase_order_id": document["purchase_order_id"]})
            .all(conn=conn, collection=False)
        )

        products = {}
        for item in items:
            if item["product_id"] not in products:
                product = Product().where({"product_id": item["product_id"]}).one_or_none(conn=conn).as_dict()
                product["measures"] = []
            else:
                product = products[item["product_id"]]

            measure = Measure().where({"measure_id": item["measure_id"]}).one_or_none(conn=conn).as_dict()
            measure.update(item)
            product["measures"].append(measure)
            products[item["product_id"]] = product

        products = list(products.values())

        for product in products:
            product["measures"] = sorted(product["measures"], key=lambda i: i["name"])

            taxes = (
                PurchaseOrderDocumentTax()
                .where({"purchase_order_id": purchase_order_id}, {"product_id": product["product_id"]})
                .all(conn=conn, collection=False)
            )

            product["taxes"] = []
            for item in taxes:
                tax = Tax().where({"tax_id": item["tax_id"]}).one_or_none(conn=conn).as_dict()
                tax.update(item)
                product["taxes"].append(tax)

            product["taxes"] = sorted(product["taxes"], key=lambda i: i["name"])

        document["products"] = sorted(products, key=lambda i: i["name"])
        document["related_documents"] = []

        return document

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    def patch_purchase_order(self, **kwargs):
        token = kwargs.get("token")

        purchase_order_id = kwargs.get("purchase_order_id", None)
        body = cherrypy.request.json

        conn = PurchaseOrderDocument().get_connection()
        document = PurchaseOrderDocument().where({"purchase_order_id": purchase_order_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not Found")

        try:
            conn.begin(conn)

            if "status" in body:
                if body["status"] not in ["new", "approved", "sent", "cancelled"]:
                    raise cherrypy.HTTPError(400, "Invalid status")

                document.status = body["status"]

            if "is_approved" in body:
                document.is_approved = Convert().str2int(body["is_approved"])

                if document.is_approved:
                    document.approved_by = token.user_id
                    document.approved_at = datetime.utcnow()

            document.updated_at = datetime.utcnow()
            document.update(conn=conn)

            conn.commit(conn)

        except Exception as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem updating data: {}".format(str(e)))

        return document.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    def cancel_purchase_order(self, **kwargs):
        purchase_order_id = kwargs.get("purchase_order_id", None)

        conn = PurchaseOrderDocument().get_connection()
        document = PurchaseOrderDocument().where({"purchase_order_id": purchase_order_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not Found")

        try:
            conn.begin(conn)

            document.status = "cancelled"
            document.updated_at = datetime.utcnow()
            document.update(conn=conn)

            conn.commit(conn)

        except Exception as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return {}
