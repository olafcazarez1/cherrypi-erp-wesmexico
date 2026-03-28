import uuid
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
from models.warehouse import Warehouse
from models.invoice_document import InvoiceDocument
from models.invoice_document_product import InvoiceDocumentProduct
from models.invoice_document_product_tax import InvoiceDocumentProductTax
from models.document_invoice import DocumentInvoice
from models.sale_document import SaleDocument
from models.sale_document_product import SaleDocumentProduct
from models.sale_document_tax import SaleDocumentTax

from models.user import User
from models.client import Client
from models.product import Product
from models.measure import Measure
from models.tax import Tax


class MapInvoiceDocument(object):
    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_invoiced_documents",
            "/invoices-documents",
            controller=self,
            action="get_invoiced_documents",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_invoice_document",
            "/invoice-document/{invoice_id}",
            controller=self,
            action="save_invoice_document",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "patch_invoice_document",
            "/invoice-document/{invoice_id}",
            controller=self,
            action="patch_invoice_document",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        mapper.connect(
            "get_invoiced_document",
            "/invoice-document/{invoice_id}",
            controller=self,
            action="get_invoiced_document",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        # mapper.connect(
        # 	'cancel_invoice_document',
        # 	'/invoice-document/{invoice_id}',
        # 	controller=self,
        # 	action='cancel_invoice_document',
        # 	conditions=dict(method=['DELETE', 'OPTIONS'])
        # )

        mapper.connect(
            "generate_invoice_from_document",
            "/document/{document_id}/generate-invoice",
            controller=self,
            action="generate_invoice_from_document",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_invoiced_documents(self, **kwargs):
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

        conn = InvoiceDocument().get_connection()
        query = Query(model=InvoiceDocument())
        query.where(*criterias)

        if int(limit) >= 0 and int(offset) >= 0:
            query.limit(limit)
            query.offset(offset)

        query.order_by(["-transaction_date", "-code"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for document in result["results"]:
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
            "invoice_id",
            "company_id",
            "branch_id",
            "warehouse_id",
            "client_id",
            "user_id",
            "payment_type_id",
            "payment_method_id",
            "receipt_type_id",
            "currency",
            "exchange_rate",
            "amount",
            "subtotal",
            "discount",
            "taxes",
            "total",
            "transaction_method",
            "transaction_type",
            "transaction_date",
            "transaction_status",
            # 'products',
            "documents",
        ]
    )
    def save_invoice_document(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        invoice_id = body.get("invoice_id", None)
        company_id = body.get("company_id", None)
        branch_id = body.get("branch_id", None)

        conn = InvoiceDocument().get_connection()
        document = InvoiceDocument().where({"invoice_id": invoice_id}).one_or_none(conn=conn)

        if document:
            return document.as_dict()

        company = Company().where({"company_id": company_id}).one_or_none(conn=conn)
        branch = BranchOffice().where({"branch_id": branch_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            code = "F{serie}{branch}{date}{number}".format(
                serie=company.serie,
                branch=branch.code,
                date=Convert().datetime2str(dt=None, tz=timezone(branch.timezone), format="%d%m%y"),
                number=Serie.generate(reference="invoice-document", key=branch_id, zfill=6, conn=conn),
            )

            document = InvoiceDocument()
            document.invoice_id = invoice_id
            document.code = code
            document.set_attrs(body, validate_unknown=False)
            document.status = "pending"
            document.created_at = datetime.utcnow()
            document.updated_at = datetime.utcnow()
            document.insert(conn=conn)

            for item in body.get("products", []):
                for measure in item["measures"]:
                    product = InvoiceDocumentProduct()
                    product.invoice_id = invoice_id
                    product.product_id = item["product_id"]
                    product.set_attrs(measure, validate_unknown=False, ignore_restricted=True)
                    product.created_at = datetime.utcnow()
                    product.updated_at = datetime.utcnow()
                    product.insert(conn=conn)

                for tax in item["taxes"]:
                    product_tax = InvoiceDocumentProductTax()
                    product_tax.invoice_id = invoice_id
                    product_tax.set_attrs(tax, validate_unknown=False, ignore_restricted=True)
                    product_tax.created_at = datetime.utcnow()
                    product_tax.updated_at = datetime.utcnow()
                    product_tax.insert(conn=conn)

            # Add relation invoice-sales
            for item in body.get("documents", []):
                relation = DocumentInvoice()
                relation.invoice_id = invoice_id
                relation.document_id = item["document_id"]
                relation.status = "active"
                relation.created_at = datetime.utcnow()
                relation.updated_at = datetime.utcnow()
                relation.insert(conn=conn)

                # Mark sale as sigend
                sale = (
                    SaleDocument()
                    .where(
                        {"document_id": item["document_id"]},
                    )
                    .one_or_none(conn=conn)
                )
                sale.is_signed = True
                sale.updated_at = datetime.utcnow()
                sale.update(conn=conn)

            conn.commit(conn)
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return document.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    def patch_invoice_document(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        invoice_id = kwargs.get("invoice_id", None)

        conn = InvoiceDocument().get_connection()
        document = InvoiceDocument().where({"invoice_id": invoice_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not Found")

        try:
            conn.begin(conn)

            document.set_attrs(body, validate_unknown=False)
            document.updated_at = datetime.utcnow()
            document.update(conn=conn)

            status = body.get("status", None)
            if status:
                signed = False
                if status in ["signed", "pending"]:
                    signed = True

                """Document Signed"""
                items = DocumentInvoice().where({"invoice_id": document.invoice_id}).limit(100000).all(conn=conn)

                for item in items.all():
                    item.status = "active" if signed else "inactive"
                    item.updated_at = datetime.utcnow()
                    item.update(conn=conn)

                    related = (
                        SaleDocument()
                        .where(
                            {"document_id": item.document_id},
                        )
                        .one_or_none(conn=conn)
                    )

                    if related:
                        related.is_signed = signed
                        related.updated_at = datetime.utcnow()
                        related.update(conn=conn)

            conn.commit(conn)
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_invoiced_document(self, **kwargs):
        invoice_id = kwargs.get("invoice_id", "")

        conn = InvoiceDocument().get_connection()
        query = Query(model=InvoiceDocument())
        document = query.where({"invoice_id": invoice_id}).one_or_none(conn=conn)

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

        items = InvoiceDocumentProduct().where({"invoice_id": document["invoice_id"]}).all(conn=conn, collection=False)

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
                InvoiceDocumentProductTax()
                .where(
                    {"invoice_id": document["invoice_id"]},
                    {"product_id": product["product_id"]},
                )
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

        items = (
            DocumentInvoice()
            .where({"invoice_id": document["invoice_id"]})
            .limit(100000)
            .all(conn=conn, collection=False)
        )

        related_documents = []
        for item in items:
            related = (
                SaleDocument()
                .where(
                    {"document_id": item["document_id"]},
                )
                .one_or_none(conn=conn)
            )

            if related:
                related_documents.append(related.as_dict())

        document["related_documents"] = sorted(related_documents, key=lambda i: i["code"])

        return document

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @cherrypy.tools.json_in()
    # @tools.secured()
    # def cancel_invoice_document(self, **kwargs):

    # 	# Get body content
    # 	body = cherrypy.request.json
    # 	invoice_id = kwargs.get('invoice_id', None)

    # 	conn = InvoiceDocument().get_connection()
    # 	document = (
    # 		InvoiceDocument()
    # 		.where({'invoice_id': invoice_id})
    # 		.one_or_none(conn = conn)
    # 	)

    # 	if document is None:
    # 		raise cherrypy.HTTPError(
    # 			404,
    # 			'Not Found'
    # 		)

    # 	document.status = 'cancelled'
    # 	document.updated_at = datetime.utcnow()
    # 	document.update(
    # 		conn = conn
    # 	)

    # 	items = (
    # 		DocumentInvoice()
    # 		.where(
    # 			{'invoice_id': document['invoice_id']}
    # 		).all(
    # 			conn = conn,
    # 			collection=False
    # 		)
    # 	)

    # 	for item in items:
    # 		related = (
    # 			SaleDocument()
    # 			.where(
    # 				{'document_id': item['document_id']},
    # 			).one_or_none(
    # 				conn = conn
    # 			)
    # 		)

    # 		if related:
    # 			related.is_signed = False
    # 			related.updated_at = datetime.utcnow()
    # 			related.update(
    # 				conn = conn
    # 			)

    # 	return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    def generate_invoice_from_document(self, **kwargs):
        # Get body content
        document_id = kwargs.get("document_id", None)
        invoice_id = str(uuid.uuid4())

        conn = SaleDocument().get_connection()
        document = SaleDocument().where({"document_id": document_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not Found")

        # check is exist an active invoice related
        relation = DocumentInvoice().where({"document_id": document_id}, {"status": "active"}).one_or_none()
        if relation:
            return InvoiceDocument().where({"invoice_id": relation.invoice_id}).one_or_none(conn=conn).as_dict()

        company = Company().where({"company_id": document.company_id}).one_or_none(conn=conn)
        branch = BranchOffice().where({"branch_id": document.branch_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            code = "F{serie}{branch}{date}{number}".format(
                serie=company.serie,
                branch=branch.code,
                date=Convert().datetime2str(dt=None, tz=timezone(branch.timezone), format="%d%m%y"),
                number=Serie.generate(reference="invoice-document", key=document.branch_id, zfill=6, conn=conn),
            )

            invoice = InvoiceDocument()
            invoice.set_attrs(document.as_dict(), validate_unknown=False, ignore_restricted=True)
            invoice.invoice_id = invoice_id
            invoice.code = code
            invoice.payment_method_id = document.payment_method
            invoice.payment_type_id = document.payment_type
            invoice.receipt_type_id = document.fiscal_use
            invoice.status = "pending"
            print(invoice.as_dict())
            invoice.insert(conn=conn)

            products = SaleDocumentProduct().where({"document_id": document_id}).all(conn=conn, collection=False)
            for item in products:

                product = InvoiceDocumentProduct()
                product.invoice_id = invoice_id
                product.set_attrs(item, validate_unknown=False, ignore_restricted=True)
                product.insert(conn=conn)

                # Get Product taxes
                taxes = (
                    SaleDocumentTax()
                    .where({"document_id": document_id}, {"product_id": product.product_id})
                    .all(conn=conn, collection=False)
                )

                for tax in taxes:
                    product_tax = InvoiceDocumentProductTax()
                    product_tax.invoice_id = invoice_id
                    product_tax.set_attrs(tax, validate_unknown=False, ignore_restricted=True)
                    product_tax.insert(conn=conn)

            relation = DocumentInvoice()
            relation.invoice_id = invoice_id
            relation.document_id = document_id
            relation.status = "active"
            relation.created_at = document.created_at
            relation.updated_at = document.updated_at
            relation.insert(conn=conn)

            conn.commit(conn)
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return invoice.as_dict()
