import cherrypy

from datetime import datetime
from pytz import timezone

from utils.decorators import tools
from utils.query import _AND
from utils.query import Query
from utils.utils import Utils
from utils.convert import Convert

from models.state import State
from models.locality import Locality
from models.municipality import Municipality

from models.serie import Serie
from models.company import Company
from models.branch_office import BranchOffice
from models.quote_document import QuoteDocument
from models.quote_document_product import QuoteDocumentProduct
from models.quote_document_tax import QuoteDocumentTax

from models.user import User
from models.warehouse import Warehouse
from models.employee import Employee
from models.client import Client
from models.product import Product
from models.measure import Measure
from models.tax import Tax


class MapQuoteDocument(object):
    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_quotes",
            "/quotes-documents",
            controller=self,
            action="get_quotes",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_quote",
            "/quote-document/{quote_id}",
            controller=self,
            action="save_quote",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "get_quote",
            "/quote-document/{quote_id}",
            controller=self,
            action="get_quote",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "cancel_quote",
            "/quote-document/{quote_id}",
            controller=self,
            action="cancel_quote",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_quotes(self, **kwargs):

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
            {"code": look_for, "op": "like"},
            _AND(
                {"transaction_date": start_date, "op": "gte"},
                {"transaction_date": end_date, "op": "lte"},
            ),
        ]

        criterias = criterias + Utils().convert_filters(filters)

        conn = QuoteDocument().get_connection()
        query = Query(model=QuoteDocument())
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

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "quote_id",
            "company_id",
            "branch_id",
            "warehouse_id",
            "user_id",
            "seller_id",
            "client_id",
            "currency",
            "exchange_rate",
            "subtotal",
            "discount",
            "taxes",
            "total",
            "transaction_date",
            "products",
        ]
    )
    def save_quote(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        quote_id = body.get("quote_id", None)
        company_id = body.get("company_id", None)
        branch_id = body.get("branch_id", None)

        conn = QuoteDocument().get_connection()
        document = QuoteDocument().where({"quote_id": quote_id}).one_or_none(conn=conn)

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
            code = "C{serie}{branch}{date}{number}".format(
                serie=company.serie,
                branch=branch.code,
                date=Convert().datetime2str(dt=None, tz=timezone(branch.timezone), format="%d%m%y"),
                number=Serie.generate(reference="quote-document", key=branch_id, zfill=6, conn=conn),
            )

            document = QuoteDocument()
            document.code = code
            document.set_attrs(body, validate_unknown=False)

            document.status = "active"
            document.created_at = datetime.utcnow()
            document.updated_at = datetime.utcnow()
            document.insert(conn=conn)

            for item in body.get("products", []):
                product = QuoteDocumentProduct()
                product.quote_id = quote_id
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
                    product_tax = QuoteDocumentTax()
                    product_tax.quote_id = quote_id
                    product_tax.set_attrs(tax, validate_unknown=False, ignore_restricted=True)
                    product_tax.created_at = datetime.utcnow()
                    product_tax.updated_at = datetime.utcnow()
                    product_tax.insert(conn=conn)

            conn.commit(conn)
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return document.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_quote(self, **kwargs):
        quote_id = kwargs.get("quote_id", "")

        conn = QuoteDocument().get_connection()
        query = Query(model=QuoteDocument())
        document = query.where({"quote_id": quote_id}).one_or_none(conn=conn)

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

        items = QuoteDocumentProduct().where({"quote_id": document["quote_id"]}).all(conn=conn, collection=False)

        # prepare products
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

            # Get Product taxes
            taxes = (
                QuoteDocumentTax()
                .where({"quote_id": quote_id}, {"product_id": product["product_id"]})
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

        # items = (
        #     DocumentInvoice()
        #     .where({"quote_id": document["quote_id"]})
        #     .limit(100000)
        #     .all(conn=conn, collection=False)
        # )

        # related_documents = []
        # for item in items:
        #     related = (
        #         InvoiceDocument()
        #         .where(
        #             {"invoice_id": item["invoice_id"]},
        #         )
        #         .one_or_none(conn=conn)
        #     )

        #     if related:
        #         related_documents.append(related.as_dict())

        # document["related_documents"] = sorted(
        #     related_documents, key=lambda i: i["code"]
        # )

        return document

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    def cancel_quote(self, **kwargs):
        quote_id = kwargs.get("quote_id", None)

        conn = QuoteDocument().get_connection()
        document = QuoteDocument().where({"quote_id": quote_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not Found")

        try:
            conn.begin(conn)

            document.status = "inactive"
            document.updated_at = datetime.utcnow()
            document.update(conn=conn)

            conn.commit(conn)
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return {}
