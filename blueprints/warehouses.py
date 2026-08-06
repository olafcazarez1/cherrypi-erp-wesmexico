import cherrypy
import pymysql

from datetime import datetime
from pytz import timezone

from models.serie import Serie
from models.tax import Tax
from models.warehouse import Warehouse
from models.category import Category
from models.subcategory import SubCategory
from models.brand import Brand
from models.brand_model import BrandModel
from models.version import Version
from models.product import Product
from models.product_tax import ProductTax
from models.product_unit import ProductUnit
from models.stock import Stock
from models.measure import Measure
from models.custom import CustomOffice
from models.stock_io import StockInOut
from models.stock_io_product import StockInOutProduct
from models.stock_io_product_tax import StockInOutProductTax
from models.stock_io_product_unit import StockInOutProductUnit

from models.user import User
from models.company import Company
from models.branch_office import BranchOffice
from models.employee import Employee
from models.supplier import Supplier

from views.product_measure import vProductMeasure

from utils.query import _OR

from utils.query import _AND
from utils.query import Query
from utils.decorators import tools
from utils.convert import Convert
from utils.utils import Utils


class MapWarehouses(object):

    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_warehouses",
            "/catalog/warehouses",
            controller=self,
            action="get_warehouses",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_warehouse_by_id",
            "/catalog/warehouse/{warehouse_id}",
            controller=self,
            action="get_warehouse_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_warehouse",
            "/catalog/warehouse/{warehouse_id}",
            controller=self,
            action="save_warehouse",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_warehouse",
            "/catalog/warehouse/{warehouse_id}",
            controller=self,
            action="delete_warehouse",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_warehouse_products",
            "/warehouse/{warehouse_id}/products",
            controller=self,
            action="get_warehouse_products",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_warehouse_product_by_id",
            "/warehouse/{warehouse_id}/product/{product_id}",
            controller=self,
            action="get_warehouse_product_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_product_price",
            "/warehouse/{warehouse_id}/product/{product_id}/price",
            controller=self,
            action="save_product_price",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        mapper.connect(
            "get_warehouse_stock_io",
            "/warehouse/{warehouse_id}/stock-io",
            controller=self,
            action="get_warehouse_stock_io",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_warehouse_stock_io_by_id",
            "/warehouse/{warehouse_id}/stock-io/{stock_io_id}",
            controller=self,
            action="get_warehouse_stock_io_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_warehouse_stock_io",
            "/warehouse/{warehouse_id}/stock-io/{stock_io_id}",
            controller=self,
            action="save_warehouse_stock_io",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "get_warehouses_transfers",
            "/warehouses-transfers",
            controller=self,
            action="get_warehouses_transfers",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_warehouses_transfers_by_id",
            "/warehouses-transfers/{transfer_id}",
            controller=self,
            action="get_warehouses_transfers_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_warehouses_transfers",
            "/warehouses-transfers/{transfer_id}",
            controller=self,
            action="save_warehouses_transfers",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_warehouses(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")

        conn = Warehouse().get_connection()
        query = Query(model=Warehouse())
        query.where(
            _OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"}),
            {"status": "active"},
        )
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code", "name"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_warehouse_by_id(self, **kwargs):

        # Get body content
        warehouse_id = kwargs.get("warehouse_id", None)
        warehouse = Warehouse().where({"warehouse_id": warehouse_id}).one_or_none()

        if warehouse is None:
            raise cherrypy.HTTPError(404, "Not Found")

        return warehouse.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["warehouse_id", "-image", "name", "type", "weight", "status"])
    def save_warehouse(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        warehouse_id = body.get("warehouse_id", None)

        conn = Warehouse().get_connection()
        warehouse = Warehouse().where({"warehouse_id": warehouse_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)
            is_new = False
            if warehouse is None:
                is_new = True
                body["code"] = Serie.generate(reference="general", key="warehouses", conn=conn)
                warehouse = Warehouse()
                warehouse.created_at = datetime.utcnow()

            warehouse.set_attrs(body)
            warehouse.updated_at = datetime.utcnow()

            if is_new:
                warehouse.insert(conn=conn)
            else:
                warehouse.update(conn=conn)

            conn.commit(conn)
        except pymysql.err.IntegrityError as e:
            # Rollback changes
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
    def delete_warehouse(self, **kwargs):

        # Get body content
        warehouse_id = kwargs.get("warehouse_id", None)

        conn = Warehouse().get_connection()
        warehouse = Warehouse().where({"warehouse_id": warehouse_id}).one_or_none(conn=conn)

        if warehouse is None:
            raise cherrypy.HTTPError(404, "Not Found")

        warehouse.status = "inactive"
        warehouse.updated_at = datetime.utcnow()
        warehouse.update(conn=conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_warehouse_products(self, **kwargs):
        conn = Warehouse().get_connection()
        # Get body content
        warehouse_id = kwargs.get("warehouse_id", None)
        limit = kwargs.get("limit", 9999)
        offset = kwargs.get("offset", 0)

        warehouse = Warehouse().where({"warehouse_id": warehouse_id}, {"status": "active"}).one_or_none(conn=conn)

        if warehouse is None:
            raise cherrypy.HTTPError(404, "Not Found")

        products = (
            Product()
            .where({"status": "active"})
            .order_by(["-code", "name"])
            .limit(limit)
            .offset(offset)
            .all(conn=conn, collection=False)
        )

        # Return only default measures
        only_default_measures = kwargs.get("only_default_measures", False)
        for product in products:

            # Get Category & Subcategory
            category = Category().where({"category_id": product["category_id"]}).one_or_none(conn=conn)

            subcategory = (
                SubCategory()
                .where(
                    {"category_id": product["category_id"]},
                    {"subcategory_id": product["subcategory_id"]},
                )
                .one_or_none(conn=conn)
            )

            product["category"] = category.as_dict()
            product["subcategory"] = subcategory.as_dict()

            # Get Product taxes
            taxes = ProductTax().where({"product_id": product["product_id"]}).all(conn=conn, collection=False)

            # Set taxes
            product["taxes"] = []
            for item in taxes:
                tax = Tax().where({"tax_id": item["tax_id"]}).one_or_none(conn=conn).as_dict()
                tax.update(item)
                product["taxes"].append(tax)

            product["taxes"] = sorted(product["taxes"], key=lambda i: i["name"])

            # Get Product Measures
            filters = [{"product_id": product["product_id"]}, {"status": "active"}]

            if only_default_measures:
                filters.append({"default": 1})

            measures = vProductMeasure().where(*filters).order_by(["weight", "name"]).all(conn=conn, collection=False)

            # Set Price
            for measure in measures:
                item = (
                    Stock()
                    .where(
                        {"warehouse_id": warehouse_id},
                        {"product_id": measure["product_id"]},
                        {"measure_id": measure["measure_id"]},
                        {"status": "active"},
                    )
                    .one_or_none(conn=conn)
                )

                if item is None:
                    item = Stock()
                    item.warehouse_id = warehouse_id
                    item.product_id = product["product_id"]
                    item.measure_id = measure["measure_id"]
                    item.price = 0.00
                    item.discount = 0.00
                    item.quantity = 0.00
                    item.status = "active"

                measure["warehouse_id"] = item.warehouse_id
                measure["quantity"] = item.quantity
                measure["discount"] = item.discount
                measure["price"] = item.price

            product["stock"] = measures
        return products

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_warehouse_product_by_id(self, **kwargs):
        conn = Warehouse().get_connection()
        # Get body content
        warehouse_id = kwargs.get("warehouse_id", None)
        product_id = kwargs.get("product_id", None)

        product = (
            Product()
            .where(
                _OR(
                    {"product_id": product_id},
                    {"code": product_id},
                ),
                {"status": "active"},
            )
            .one_or_none(conn=conn)
        )

        if product is None:
            raise cherrypy.HTTPError(404, "Not Found")

        product = product.as_dict()
        # Get Category & Subcategory
        category = Category().where({"category_id": product["category_id"]}).one_or_none(conn=conn)

        subcategory = (
            SubCategory()
            .where(
                {"category_id": product["category_id"]},
                {"subcategory_id": product["subcategory_id"]},
            )
            .one_or_none(conn=conn)
        )

        product["category"] = category.as_dict()
        product["subcategory"] = subcategory.as_dict()

        # Get Product Measures
        measures = (
            vProductMeasure()
            .where({"product_id": product["product_id"]}, {"status": "active"})
            .order_by(["weight", "name"])
            .all(conn=conn, collection=False)
        )

        # Set Price
        for measure in measures:
            item = (
                Stock()
                .where(
                    {"warehouse_id": warehouse_id},
                    {"product_id": measure["product_id"]},
                    {"measure_id": measure["measure_id"]},
                    {"status": "active"},
                )
                .one_or_none(conn=conn)
            )

            if item is None:
                item = Stock()
                item.warehouse_id = warehouse_id
                item.product_id = product["product_id"]
                item.measure_id = measure["measure_id"]
                item.price = 0.00
                item.discount = 0.00
                item.quantity = 0.00
                item.status = "active"

            measure["warehouse_id"] = item.warehouse_id
            measure["quantity"] = item.quantity
            measure["discount"] = item.discount
            measure["price"] = item.price

        product["stock"] = measures

        # Get Product taxes
        taxes = (
            ProductTax()
            .where({"product_id": product["product_id"]}, {"status": "active"})
            .all(conn=conn, collection=False)
        )

        # Set taxes
        product["taxes"] = []
        for item in taxes:
            tax = Tax().where({"tax_id": item["tax_id"]}).one_or_none(conn=conn).as_dict()
            tax.update(item)
            product["taxes"].append(tax)

        product["taxes"] = sorted(product["taxes"], key=lambda i: i["name"])
        product["related"] = []

        return product

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["warehouse_id", "product_id", "measure_id", "price", "discount"])
    def save_product_price(self, **kwargs):
        conn = Warehouse().get_connection()

        # Get body content
        body = cherrypy.request.json

        warehouse_id = body.get("warehouse_id", None)
        product_id = body.get("product_id", None)
        measure_id = body.get("measure_id", None)
        price = body.get("price", None)
        discount = body.get("discount", None)

        warehouse = Warehouse().where({"warehouse_id": warehouse_id}, {"status": "active"}).one_or_none(conn=conn)

        if warehouse is None:
            raise cherrypy.HTTPError(404, "Not Found")

        item = (
            Stock()
            .where(
                {"warehouse_id": warehouse_id},
                {"product_id": product_id},
                {"measure_id": measure_id},
            )
            .one_or_none(conn=conn)
        )

        if item is None:
            item = Stock()
            item.warehouse_id = warehouse_id
            item.product_id = product_id
            item.measure_id = measure_id
            item.price = 0
            item.discount = 0
            item.quantity = 0
            item.status = "active"
            item.created_at = datetime.utcnow()
            item.updated_at = datetime.utcnow()
            item.insert(conn=conn)

        item.price = price
        item.discount = discount
        item.updated_at = datetime.utcnow()
        item.update(conn=conn)
        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_warehouse_stock_io(self, **kwargs):
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
            _OR(
                {"code": look_for, "op": "like"},
                {"reference": look_for, "op": "like"},
            ),
            _AND(
                {"transaction_date": start_date, "op": "gte"},
                {"transaction_date": end_date, "op": "lte"},
            ),
        ]

        criterias = criterias + Utils().convert_filters(filters)

        conn = StockInOut().get_connection()
        query = Query(model=StockInOut())
        query.where(*criterias)

        if int(limit) >= 0 and int(offset) >= 0:
            query.limit(limit)
            query.offset(offset)

        query.order_by(["-code"])

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

            document["warehouse"] = (
                Warehouse().where({"warehouse_id": document["warehouse_id"]}).one_or_none(conn=conn).as_dict()
            )

            document["supplier"] = (
                Supplier().where({"supplier_id": document["supplier_id"]}).one_or_none(conn=conn).as_dict()
            )

            document["custom_office"] = (
                CustomOffice().where({"custom_id": document["custom_id"]}).one_or_none(conn=conn).as_dict()
            )

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_warehouse_stock_io_by_id(self, **kwargs):

        stock_io_id = kwargs.get("stock_io_id", "")

        conn = StockInOut().get_connection()
        query = Query(model=StockInOut())
        document = query.where({"stock_io_id": stock_io_id}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not found")

        document = document.as_dict()
        document["user"] = User().where({"user_id": document["user_id"]}).one_or_none(conn=conn).as_dict()

        document["employee"] = (
            Employee().where({"employee_id": document["employee_id"]}).one_or_none(conn=conn).as_dict()
        )

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

        document["custom_office"] = (
            CustomOffice().where({"custom_id": document["custom_id"]}).one_or_none(conn=conn).as_dict()
        )

        items = StockInOutProduct().where({"stock_io_id": document["stock_io_id"]}).all(conn=conn, collection=False)

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

            # Get Product taxes
            units = (
                StockInOutProductUnit()
                .where(
                    {"stock_io_id": stock_io_id},
                    {"product_id": product["product_id"]},
                    {"measure_id": item["measure_id"]},
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
                StockInOutProductTax()
                .where({"stock_io_id": stock_io_id}, {"product_id": product["product_id"]})
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

        return document

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "stock_io_id",
            "user_id",
            "employee_id",
            "company_id",
            "branch_id",
            "warehouse_id",
            "supplier_id",
            "reference",
            "transaction_type",
            "document_type",
            "currency",
            "exchange_rate",
            "amount",
            "subtotal",
            "discount",
            "tax",
            "total",
            "type",
            "transaction_date",
            "payment_type",
            "payment_method",
            "tax_receipt",
            "purchase_origin",
            "importation_number",
            "importation_date",
            "custom_id",
            "products",
            "documents",
        ]
    )
    def save_warehouse_stock_io(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        stock_io_id = body.get("stock_io_id", None)
        company_id = body.get("company_id", None)

        conn = StockInOut().get_connection()
        document = StockInOut().where({"stock_io_id": stock_io_id}).one_or_none(conn=conn)

        if document:
            raise cherrypy.HTTPError(423, "Document Locked")

        company = Company().where({"company_id": company_id}).one_or_none(conn=conn)

        # try:
        #     conn.begin(conn)

        code = "{prefix}{date}{number}".format(
            prefix=company.serie,
            date=Convert().datetime2str(dt=None, tz=timezone(company.timezone), format="%d%m%y"),
            number=Serie.generate(reference="general", key="stock-io", zfill=6, conn=conn),
        )

        document = StockInOut()
        document.stock_io_id = stock_io_id
        document.code = code
        document.set_attrs(body, validate_unknown=False)
        document.status = "active"
        document.created_at = datetime.utcnow()
        document.updated_at = datetime.utcnow()
        document.insert(conn=conn)

        for item in body.get("products", []):
            # for measure in item["measures"]:
            product = StockInOutProduct()
            product.stock_io_id = stock_io_id
            product.set_attrs(item, validate_unknown=False, ignore_restricted=True)
            product.created_at = datetime.utcnow()
            product.updated_at = datetime.utcnow()
            product.insert(conn=conn)

            for tax in item["taxes"]:
                t = StockInOutProductTax()
                t.stock_io_id = stock_io_id
                t.set_attrs(tax, validate_unknown=False, ignore_restricted=True)
                t.created_at = datetime.utcnow()
                t.updated_at = datetime.utcnow()
                t.insert(conn=conn)

            # Update stock
            entry = (
                Stock()
                .where(
                    {"warehouse_id": document.warehouse_id},
                    {"product_id": product.product_id},
                    {"measure_id": product.measure_id},
                )
                .one_or_none(conn=conn)
            )

            if entry is None:
                entry = Stock()
                entry.warehouse_id = document.warehouse_id
                entry.product_id = product.product_id
                entry.measure_id = product.measure_id
                entry.price = 0
                entry.discount = 0
                entry.quantity = 0
                entry.status = "active"
                entry.created_at = datetime.utcnow()
                entry.updated_at = datetime.utcnow()
                entry.insert(conn=conn)

            if document.type in ["purchases", "input"]:
                entry.quantity = entry.quantity + product.quantity
            elif document.type in ["output", "declines", "losses"]:
                entry.quantity = entry.quantity - product.quantity

            entry.updated_at = datetime.utcnow()
            entry.update(conn=conn)

            # Add Units
            if "units" in item and document.type in ["purchases", "input"]:
                for unit in item["units"]:
                    #  Create Unit
                    pu = ProductUnit()
                    pu.code = Serie.generate(
                        reference="product_{}".format(item["product_id"]),
                        key="unit",
                        prefix=item["code"],
                        conn=conn,
                    )

                    pu.company_id = document.company_id
                    pu.product_id = product.product_id
                    pu.unit_id = unit["unit_id"]
                    pu.brand_id = unit["brand_id"]
                    pu.model_id = unit["model_id"]
                    pu.version_id = unit["version_id"]
                    pu.department_id = "ed77e6e8-2c99-43e4-b4a4-a945e9afd444"
                    pu.serie = ""
                    pu.reference = ""
                    pu.uid = unit["uid"]
                    pu.description = ""
                    pu.importation_number = document.importation_number
                    pu.importation_date = document.importation_date
                    pu.custom_id = document.custom_id
                    pu.status = "active"
                    pu.created_at = datetime.utcnow()
                    pu.updated_at = datetime.utcnow()
                    pu.insert(conn=conn)

                    # Asociate

                    io_unit = StockInOutProductUnit()
                    io_unit.stock_io_id = document.stock_io_id
                    io_unit.product_id = product.product_id
                    io_unit.measure_id = product.measure_id
                    io_unit.unit_id = pu.unit_id
                    io_unit.uid = pu.uid
                    io_unit.created_at = datetime.utcnow()
                    io_unit.updated_at = datetime.utcnow()
                    io_unit.insert(conn=conn)

            elif "units" in item and document.type in ["declines", "losses"]:
                for unit in item["units"]:
                    pu = (
                        ProductUnit()
                        .where({"product_id": product.product_id}, {"uid": unit["uid"]})
                        .one_or_none(conn=conn)
                    )

                    pu.status = "disposal"
                    pu.update(conn=conn)

                    # Asociate

                    io_unit = StockInOutProductUnit()
                    io_unit.stock_io_id = document.stock_io_id
                    io_unit.product_id = product.product_id
                    io_unit.measure_id = product.measure_id
                    io_unit.unit_id = pu.unit_id
                    io_unit.uid = pu.uid
                    io_unit.created_at = datetime.utcnow()
                    io_unit.updated_at = datetime.utcnow()
                    io_unit.insert(conn=conn)

        # for item in item["documents"]:
        # 	if item == '':
        # 		continue
        # 	tag = item.split('/')[-1]
        # 	document_id = tag.split('.')[0]

        # 	document = PaymentTransactionDocument()
        # 	document.transaction_id = transaction_id
        # 	document.document_id = document_id
        # 	document.path = item
        # 	document.created_at = datetime.utcnow()
        # 	document.updated_at = datetime.utcnow()
        # 	document.insert(
        # 		conn = conn
        # 	)

        # conn.commit(conn)
        # except Exception as e:
        #     # Rollback changes
        #     conn.rollback(conn)
        #     raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return {}

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @tools.secured()
    # def get_warehouses_transfers(self, **kwargs):
    #     token = kwargs.get("token")

    #     result = {}
    #     result["results"] = []
    #     result["total_rows"] = 0

    #     offset = kwargs.get("offset", 0)
    #     limit = kwargs.get("limit", 0)
    #     look_for = kwargs.get("look_for", "")
    #     start_date = kwargs.get("start_date", None)
    #     end_date = kwargs.get("end_date", None)
    #     filters = kwargs.get("filters", "[]")

    #     criterias = [
    #         _OR(
    #             {"code": look_for, "op": "like"},
    #             {"reference": look_for, "op": "like"},
    #         ),
    #         _AND(
    #             {"transaction_date": start_date, "op": "gte"},
    #             {"transaction_date": end_date, "op": "lte"},
    #         ),
    #     ]

    #     criterias = criterias + Utils().convert_filters(filters)

    #     conn = WarehouseTransfer().get_connection()
    #     query = Query(model=WarehouseTransfer())
    #     query.where(*criterias)

    #     if int(limit) >= 0 and int(offset) >= 0:
    #         query.limit(limit)
    #         query.offset(offset)

    #     query.order_by(["-transaction_date", "-code"])

    #     result["results"] = query.all(conn=conn, collection=False)
    #     result["total_rows"] = query.count(conn=conn)

    #     for document in result["results"]:
    #         document["user"] = User().where({"user_id": document["user_id"]}).one_or_none(conn=conn).as_dict()

    #         document["employee"] = (
    #             Employee().where({"employee_id": document["employee_id"]}).one_or_none(conn=conn).as_dict()
    #         )

    #         document["src_company"] = (
    #             Company().where({"company_id": document["src_company_id"]}).one_or_none(conn=conn).as_dict()
    #         )

    #         document["src_branch"] = (
    #             BranchOffice().where({"branch_id": document["src_branch_id"]}).one_or_none(conn=conn).as_dict()
    #         )

    #         document["src_warehouse"] = (
    #             Warehouse().where({"warehouse_id": document["src_warehouse_id"]}).one_or_none(conn=conn).as_dict()
    #         )

    #         document["dst_company"] = (
    #             Company().where({"company_id": document["dst_company_id"]}).one_or_none(conn=conn).as_dict()
    #         )

    #         document["dst_branch"] = (
    #             BranchOffice().where({"branch_id": document["dst_branch_id"]}).one_or_none(conn=conn).as_dict()
    #         )

    #         document["dst_warehouse"] = (
    #             Warehouse().where({"warehouse_id": document["dst_warehouse_id"]}).one_or_none(conn=conn).as_dict()
    #         )

    #     return result

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @tools.secured()
    # def get_warehouses_transfers_by_id(self, **kwargs):
    #     token = kwargs.get("token")

    #     transfer_id = kwargs.get("transfer_id", "")

    #     conn = WarehouseTransfer().get_connection()
    #     query = Query(model=WarehouseTransfer())
    #     document = query.where({"transfer_id": transfer_id}).one_or_none(conn=conn)

    #     if document is None:
    #         raise cherrypy.HTTPError(404, "Not found")

    #     document = document.as_dict()
    #     document["user"] = User().where({"user_id": document["user_id"]}).one_or_none(conn=conn).as_dict()

    #     document["employee"] = (
    #         Employee().where({"employee_id": document["employee_id"]}).one_or_none(conn=conn).as_dict()
    #     )

    #     document["src_company"] = (
    #         Company().where({"company_id": document["src_company_id"]}).one_or_none(conn=conn).as_dict()
    #     )

    #     document["src_branch"] = (
    #         BranchOffice().where({"branch_id": document["src_branch_id"]}).one_or_none(conn=conn).as_dict()
    #     )

    #     document["src_warehouse"] = (
    #         Warehouse().where({"warehouse_id": document["src_warehouse_id"]}).one_or_none(conn=conn).as_dict()
    #     )

    #     document["dst_company"] = (
    #         Company().where({"company_id": document["dst_company_id"]}).one_or_none(conn=conn).as_dict()
    #     )

    #     document["dst_branch"] = (
    #         BranchOffice().where({"branch_id": document["dst_branch_id"]}).one_or_none(conn=conn).as_dict()
    #     )

    #     document["dst_warehouse"] = (
    #         Warehouse().where({"warehouse_id": document["dst_warehouse_id"]}).one_or_none(conn=conn).as_dict()
    #     )

    #     items = (
    #         WarehouseTransferProduct().where({"transfer_id": document["transfer_id"]}).all(conn=conn, collection=False)
    #     )

    #     # prepare products
    #     products = {}
    #     for item in items:
    #         if item["product_id"] not in products:
    #             product = Product().where({"product_id": item["product_id"]}).one_or_none(conn=conn).as_dict()
    #             product["measures"] = []
    #         else:
    #             product = products[item["product_id"]]

    #         measure = Measure().where({"measure_id": item["measure_id"]}).one_or_none(conn=conn).as_dict()

    #         measure.update(item)
    #         product["measures"].append(measure)
    #         products[item["product_id"]] = product

    #     products = list(products.values())
    #     document["products"] = sorted(products, key=lambda i: i["name"])

    #     return document

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @cherrypy.tools.json_in()
    # @tools.secured()
    # @tools.validate_body_params(
    #     [
    #         "transfer_id",
    #         "reference",
    #         "src_company_id",
    #         "src_branch_id",
    #         "src_warehouse_id",
    #         "dst_company_id",
    #         "dst_branch_id",
    #         "dst_warehouse_id",
    #         "transaction_date",
    #         "notes",
    #         "products",
    #         "notes",
    #     ]
    # )
    # def save_warehouses_transfers(self, **kwargs):
    #     # Get body content
    #     body = cherrypy.request.json
    #     transfer_id = body.get("transfer_id", None)
    #     company_id = body.get("src_company_id", None)

    #     conn = WarehouseTransfer().get_connection()
    #     document = WarehouseTransfer().where({"transfer_id": transfer_id}).one_or_none(conn=conn)

    #     if document:
    #         raise cherrypy.HTTPError(423, "Document Locked")

    #     company = Company().where({"company_id": company_id}).one_or_none(conn=conn)

    #     try:
    #         conn.begin(conn)

    #         code = "{prefix}{date}{number}".format(
    #             prefix=company.serie,
    #             date=Convert().datetime2str(dt=None, tz=timezone(company.timezone), format="%d%m%y"),
    #             number=Serie.generate(reference="general", key="warehouse-transfer", zfill=6, conn=conn),
    #         )

    #         document = WarehouseTransfer()
    #         document.transfer_id = transfer_id
    #         document.code = code
    #         document.set_attrs(body, validate_unknown=False)
    #         document.status = "active"
    #         document.created_at = datetime.utcnow()
    #         document.updated_at = datetime.utcnow()
    #         document.insert(conn=conn)

    #         for item in body.get("products", []):
    #             # for measure in item["measures"]:
    #             product = WarehouseTransferProduct()
    #             product.transfer_id = transfer_id
    #             product.set_attrs(item, validate_unknown=False, ignore_restricted=True)
    #             product.created_at = datetime.utcnow()
    #             product.updated_at = datetime.utcnow()
    #             product.insert(conn=conn)

    #         for action in ["output", "input"]:
    #             # generate stock-io
    #             code = "{prefix}{date}{number}".format(
    #                 prefix=company.serie,
    #                 date=Convert().datetime2str(dt=None, tz=timezone(company.timezone), format="%d%m%y"),
    #                 number=Serie.generate(
    #                     reference="general",
    #                     key="stock-io",
    #                     zfill=6,
    #                     conn=conn,
    #                 ),
    #             )
    #             io = StockInOut()
    #             io.stock_io_id = str(uuid.uuid4())
    #             io.user_id = document.user_id
    #             io.employee_id = document.employee_id

    #             if action == "output":
    #                 io.company_id = document.src_company_id
    #                 io.branch_id = document.src_branch_id
    #                 io.warehouse_id = document.src_warehouse_id
    #             elif action == "input":
    #                 io.company_id = document.dst_company_id
    #                 io.branch_id = document.dst_branch_id
    #                 io.warehouse_id = document.dst_warehouse_id

    #             io.supplier_id = "f4538ac1-a9c5-11ed-9f14-809133bea1e5"
    #             io.code = code
    #             io.reference = document.reference
    #             io.transaction_type = ("cash",)
    #             io.document_type = ("sale_note",)
    #             io.currency = "mxn"
    #             io.exchange_rate = 1.00
    #             io.amount = 0.00
    #             io.subtotal = 0.00
    #             io.discount = 0.00
    #             io.tax = 0.00
    #             io.total = 0.00
    #             io.type = action
    #             io.transaction_date = document.transaction_date
    #             io.payment_type = "e9979472-a1d6-4a57-b631-508ca0c5fa49"
    #             io.payment_method = "8f966b79-d02f-4a74-8c55-cbdab903d649"
    #             io.tax_receipt = "cd53b6e4-554e-11e8-a542-66d4b3ba2dec"
    #             io.notes = document.notes
    #             io.status = "active"
    #             io.created_at = datetime.utcnow()
    #             io.updated_at = datetime.utcnow()

    #             io.insert(conn=conn)

    #             for item in body.get("products", []):
    #                 # for measure in item["measures"]:
    #                 product = StockInOutProduct()
    #                 product.stock_io_id = io.stock_io_id
    #                 product.set_attrs(item, validate_unknown=False, ignore_restricted=True)
    #                 product.currency = "mxn"
    #                 product.subtotal = 0.00
    #                 product.discount = 0.00
    #                 product.tax = 0.00
    #                 product.total = 0.00
    #                 product.created_at = datetime.utcnow()
    #                 product.updated_at = datetime.utcnow()
    #                 product.insert(conn=conn)

    #                 for tax in item["taxes"]:
    #                     t = StockInOutProductTax()
    #                     t.stock_io_id = io.stock_io_id
    #                     t.set_attrs(tax, validate_unknown=False, ignore_restricted=True)
    #                     t.created_at = datetime.utcnow()
    #                     t.updated_at = datetime.utcnow()
    #                     t.insert(conn=conn)

    #                 # Update stock
    #                 entry = (
    #                     Stock()
    #                     .where(
    #                         {"warehouse_id": io.warehouse_id},
    #                         {"product_id": product.product_id},
    #                         {"measure_id": product.measure_id},
    #                     )
    #                     .one_or_none(conn=conn)
    #                 )

    #                 if entry is None:
    #                     entry = Stock()
    #                     entry.warehouse_id = io.warehouse_id
    #                     entry.product_id = product.product_id
    #                     entry.measure_id = product.measure_id
    #                     entry.price = 0
    #                     entry.discount = 0
    #                     entry.quantity = 0
    #                     entry.status = "active"
    #                     entry.created_at = datetime.utcnow()
    #                     entry.updated_at = datetime.utcnow()
    #                     entry.insert(conn=conn)

    #                 if io.type in ["purchases", "input"]:
    #                     entry.quantity = entry.quantity + product.quantity
    #                 elif io.type in ["output", "declines", "losses"]:
    #                     entry.quantity = entry.quantity - product.quantity

    #                 entry.updated_at = datetime.utcnow()
    #                 entry.update(conn=conn)

    #         conn.commit(conn)
    #     except Exception as e:
    #         # Rollback changes
    #         conn.rollback(conn)
    #         raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

    #     return {}
