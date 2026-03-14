import cherrypy
from datetime import datetime
from pytz import timezone

from utils.decorators import tools
from utils.query import _OR, _AND, Query
from utils.utils import Utils
from utils.convert import Convert

from models.company import Company
from models.branch_office import BranchOffice
from models.warehouse import Warehouse
from models.client import Client
from models.user import User
from models.employee import Employee
from models.product import Product
from models.measure import Measure
from models.product_unit import ProductUnit
from models.brand import Brand
from models.brand_model import BrandModel
from models.version import Version
from models.state import State
from models.municipality import Municipality
from models.locality import Locality

from models.serie import Serie

from models.sale_document import SaleDocument
from models.sale_document_product import SaleDocumentProduct
from models.sale_document_product_unit import SaleDocumentProductUnit


from models.sale_delivery_order import SaleDeliveryOrder
from models.sale_delivery_order_product import SaleDeliveryOrderProduct
from models.sale_delivery_order_product_unit import SaleDeliveryOrderProductUnit


class MapDeliveryOrders(object):
    def init(self, mapper):

        mapper.connect(
            "get_delivery_orders",
            "/sales-delivery-orders",
            controller=self,
            action="get_delivery_orders",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_sale_order",
            "/sale-order/{reference}",
            controller=self,
            action="get_sale_order",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_delivery_order",
            "/sale-delivery-order/{order_id}",
            controller=self,
            action="save_delivery_order",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "get_delivery_order",
            "/sale-delivery-order/{order_id}",
            controller=self,
            action="get_delivery_order",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "cancel_delivery_order",
            "/sale-delivery-order/{order_id}",
            controller=self,
            action="cancel_delivery_order",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    # ------------------------------------------------------------------------------
    # GET list
    # ------------------------------------------------------------------------------
    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_delivery_orders(self, **kwargs):

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

        conn = SaleDeliveryOrder().get_connection()
        query = Query(model=SaleDeliveryOrder()).where(*criterias)

        if int(limit) >= 0 and int(offset) >= 0:
            query.limit(limit)
            query.offset(offset)

        query.order_by(["-transaction_date", "-code"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for order in result["results"]:

            order["user"] = User().where({"user_id": order["user_id"]}).one_or_none(conn=conn).as_dict()

            order["worker"] = Employee().where({"employee_id": order["worker_id"]}).one_or_none(conn=conn).as_dict()

            order["company"] = Company().where({"company_id": order["company_id"]}).one_or_none(conn=conn).as_dict()

            order["branch"] = BranchOffice().where({"branch_id": order["branch_id"]}).one_or_none(conn=conn).as_dict()

            order["warehouse"] = (
                Warehouse().where({"warehouse_id": order["warehouse_id"]}).one_or_none(conn=conn).as_dict()
            )

            order["client"] = Client().where({"client_id": order["client_id"]}).one_or_none(conn=conn).as_dict()

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_sale_order(self, reference: str, **kwargs):

        conn = SaleDocument().get_connection()

        # ------------------------------------------------------------
        # Find the sale document by code
        # ------------------------------------------------------------
        query = Query(model=SaleDocument())
        document = query.where({"code": reference, "status": "active"}).one_or_none(conn=conn)

        if document is None:
            raise cherrypy.HTTPError(404, "Not found")

        document = document.as_dict()

        # ------------------------------------------------------------
        # Base info adapted for delivery
        # ------------------------------------------------------------
        document["reference"] = reference
        document["code"] = ""  # delivery order will have its own code
        document["notes"] = ""
        document["status"] = "active"

        document["company"] = Company().where({"company_id": document["company_id"]}).one_or_none(conn=conn).as_dict()

        document.pop("transaction_date", None)
        document.pop("status", None)

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

        # ------------------------------------------------------------
        # Load sale products
        # ------------------------------------------------------------
        items = SaleDocumentProduct().where({"document_id": document["document_id"]}).all(conn=conn, collection=False)

        products = {}

        for item in items:
            pid = item["product_id"]
            mid = item["measure_id"]

            # Prepare product block
            if pid not in products:
                product = Product().where({"product_id": pid}).one_or_none(conn=conn).as_dict()
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
                product = products[pid]

            # --------------------------------------------------------
            # delivered_before: all deliveries for this sale (document)
            # --------------------------------------------------------
            delivered_entries = (
                SaleDeliveryOrderProduct()
                .where(
                    {"product_id": pid},
                    {"measure_id": mid},
                    {
                        "order_id": (
                            SaleDeliveryOrder()
                            .fields(["order_id"])
                            .where({"document_id": item["document_id"]})
                            .sql(remove_offset_limit=True)
                        ),
                        "op": "in",
                    },
                )
                .all(conn=conn, collection=False)
            )

            delivered_before = 0
            for d in delivered_entries:
                delivered_before += d.get("quantity", 0)

            ordered = item["quantity"]
            remaining = ordered - delivered_before

            # --------------------------------------------------------
            # Measure block with delivery fields
            # --------------------------------------------------------
            measure = Measure().where({"measure_id": mid}).one_or_none(conn=conn).as_dict()

            measure.update(
                {
                    "product_id": product["product_id"],
                    "ordered": ordered,
                    "delivered_before": delivered_before,
                    "remaining": remaining,
                    "quantity": 0,  # to be filled in new delivery
                }
            )

            # --------------------------------------------------------
            # Units (available + delivered) using delivered-unit logic
            # --------------------------------------------------------

            # Units that BELONG to the sale document (original sale units)
            base_units = (
                SaleDocumentProductUnit()
                .where(
                    {"document_id": document["document_id"]},
                    {"product_id": product["product_id"]},
                    {"measure_id": measure["measure_id"]},
                )
                .all(conn=conn, collection=False)
            )

            # Units ALREADY DELIVERED across all delivery orders for this document
            delivered_units = (
                SaleDeliveryOrderProductUnit()
                .where(
                    {"product_id": pid},
                    {"measure_id": mid},
                    {
                        "order_id": (
                            SaleDeliveryOrder()
                            .fields(["order_id"])
                            .where({"document_id": document["document_id"]})
                            .sql(remove_offset_limit=True)
                        ),
                        "op": "in",
                    },
                )
                .all(conn=conn, collection=False)
            )

            delivered_unit_ids = {u["unit_id"] for u in delivered_units}

            measure["units"] = []

            for entry in base_units:

                # Load product unit (even if inactive, so FE knows historical info)
                unit = ProductUnit().where({"unit_id": entry["unit_id"]}).one_or_none(conn=conn)
                if not unit:
                    continue

                unit = unit.as_dict()

                # Add brand/model/version info
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

                # Merge fields from sale_document_product_unit
                unit.update(entry)

                # --------------------------------------------------------
                # Mark if this unit has already been delivered
                # --------------------------------------------------------
                unit["is_delivered"] = unit["unit_id"] in delivered_unit_ids

                measure["units"].append(unit)

            # Sort units visually by UID
            measure["units"] = sorted(measure["units"], key=lambda i: i["uid"])

            product["measures"].append(measure)
            products[pid] = product

        # Sort and assign
        products = list(products.values())
        for p in products:
            p["measures"] = sorted(p["measures"], key=lambda i: i["name"])

        document["products"] = sorted(products, key=lambda i: i["name"])

        # In this context we don't need related_documents / invoices for the delivery
        return document

    # ------------------------------------------------------------------------------
    # POST – save delivery order
    # ------------------------------------------------------------------------------
    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "order_id",
            "document_id",
            "company_id",
            "branch_id",
            "warehouse_id",
            "client_id",
            "user_id",
            "worker_id",
            "transaction_date",
            "notes",
            "products",
        ]
    )
    def save_delivery_order(self, **kwargs):

        body = cherrypy.request.json
        company_id = body.get("company_id")
        branch_id = body.get("branch_id")
        warehouse_id = body.get("warehouse_id")
        document_id = body.get("document_id")
        order_id = body.get("order_id")

        conn = SaleDeliveryOrder().get_connection()

        # Existing?
        order = SaleDeliveryOrder().where({"order_id": order_id}).one_or_none(conn=conn)

        if order:
            raise cherrypy.HTTPError(423, "Order Locked")

        company = Company().where({"company_id": company_id}).one_or_none(conn=conn)
        branch = BranchOffice().where({"branch_id": branch_id}).one_or_none(conn=conn)
        warehouse = Warehouse().where({"warehouse_id": warehouse_id}).one_or_none(conn=conn)

        if not company:
            raise cherrypy.HTTPError(400, "Invalid company")

        if not branch:
            raise cherrypy.HTTPError(400, "Invalid branch")

        if not warehouse:
            raise cherrypy.HTTPError(400, "Invalid warehouse")

        # Ensure sale document exists
        sale_doc = SaleDocument().where({"document_id": document_id}).one_or_none(conn=conn)
        if not sale_doc:
            raise cherrypy.HTTPError(400, "Invalid source sale document")

        try:
            conn.begin(conn)

            # Generate code
            code = "E{serie}{branch}{date}{num}".format(
                serie=company.serie,
                branch=branch.code,
                date=Convert().datetime2str(dt=None, tz=timezone(branch.timezone), format="%d%m%y"),
                num=Serie.generate(reference="sale-delivery-order", key=branch_id, zfill=6, conn=conn),
            )

            order = SaleDeliveryOrder()
            order.code = code
            order.set_attrs(body, validate_unknown=False)
            order.status = "active"
            order.created_at = datetime.utcnow()
            order.updated_at = datetime.utcnow()
            order.insert(conn=conn)

            # ------------------------------------------------------------------
            # Products
            # ------------------------------------------------------------------
            for item in body.get("products", []):

                delivery_product = SaleDeliveryOrderProduct()
                delivery_product.order_id = order_id
                delivery_product.set_attrs(item, validate_unknown=False, ignore_restricted=True)
                delivery_product.created_at = datetime.utcnow()
                delivery_product.updated_at = datetime.utcnow()
                delivery_product.insert(conn=conn)

                # --------------------------------------------------------------
                # Units
                # --------------------------------------------------------------
                for unit in item.get("units", []):

                    pu = (
                        ProductUnit()
                        .where(
                            {"product_id": delivery_product.product_id},
                            {"uid": unit["uid"]},
                        )
                        .one_or_none(conn=conn)
                    )

                    if not pu:
                        raise cherrypy.HTTPError(500, "Invalid Unit {}".format(unit["uid"]))

                    pu.status = "delivered"
                    pu.update(conn=conn)

                    io_unit = SaleDeliveryOrderProductUnit()
                    io_unit.order_id = order_id
                    io_unit.product_id = delivery_product.product_id
                    io_unit.measure_id = delivery_product.measure_id
                    io_unit.unit_id = pu.unit_id
                    io_unit.uid = pu.uid
                    io_unit.created_at = datetime.utcnow()
                    io_unit.updated_at = datetime.utcnow()
                    io_unit.insert(conn=conn)

            conn.commit(conn)

        except Exception as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return order.as_dict()

    # ------------------------------------------------------------------------------
    # GET single delivery order
    # ------------------------------------------------------------------------------
    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_delivery_order(self, **kwargs):

        order_id = kwargs.get("order_id", "")

        conn = SaleDeliveryOrder().get_connection()
        query = Query(model=SaleDeliveryOrder())
        order = query.where({"order_id": order_id}).one_or_none(conn=conn)

        if order is None:
            raise cherrypy.HTTPError(404, "Not Found")

        order = order.as_dict()

        # Company, branch, warehouse, client, user, worker
        order["company"] = Company().where({"company_id": order["company_id"]}).one_or_none(conn=conn).as_dict()

        order["branch"] = BranchOffice().where({"branch_id": order["branch_id"]}).one_or_none(conn=conn).as_dict()

        order["branch"]["state"] = (
            State().where({"state_id": order["branch"]["state_id"]}).one_or_none(conn=conn).as_dict()
        )

        order["branch"]["municipality"] = (
            Municipality()
            .where(
                {"state_id": order["branch"]["state_id"]},
                {"municipality_id": order["branch"]["municipality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        order["branch"]["locality"] = (
            Locality()
            .where(
                {"state_id": order["branch"]["state_id"]},
                {"municipality_id": order["branch"]["municipality_id"]},
                {"locality_id": order["branch"]["locality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        order["warehouse"] = (
            Warehouse().where({"warehouse_id": order["warehouse_id"]}).one_or_none(conn=conn).as_dict()
        )

        order["client"] = Client().where({"client_id": order["client_id"]}).one_or_none(conn=conn).as_dict()

        order["client"]["state"] = (
            State().where({"state_id": order["client"]["state_id"]}).one_or_none(conn=conn).as_dict()
        )

        order["client"]["municipality"] = (
            Municipality()
            .where(
                {"state_id": order["client"]["state_id"]},
                {"municipality_id": order["client"]["municipality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        order["client"]["locality"] = (
            Locality()
            .where(
                {"state_id": order["client"]["state_id"]},
                {"municipality_id": order["client"]["municipality_id"]},
                {"locality_id": order["client"]["locality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        order["user"] = User().where({"user_id": order["user_id"]}).one_or_none(conn=conn).as_dict()

        order["worker"] = Employee().where({"employee_id": order["worker_id"]}).one_or_none(conn=conn).as_dict()

        # --------------------------------------------------------------------------
        # Products
        # --------------------------------------------------------------------------
        items = SaleDeliveryOrderProduct().where({"order_id": order_id}).all(conn=conn, collection=False)

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
                SaleDeliveryOrderProductUnit()
                .where(
                    {"order_id": order_id},
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

        # Final sorting
        products = list(products.values())
        for product in products:
            product["measures"] = sorted(product["measures"], key=lambda i: i["name"])

        order["products"] = sorted(products, key=lambda i: i["name"])

        return order

    # ------------------------------------------------------------------------------
    # DELETE – cancel delivery order
    # ------------------------------------------------------------------------------
    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def cancel_delivery_order(self, **kwargs):

        order_id = kwargs.get("order_id")

        conn = SaleDeliveryOrder().get_connection()
        order = SaleDeliveryOrder().where({"order_id": order_id}).one_or_none(conn=conn)

        if order is None:
            raise cherrypy.HTTPError(404, "Not Found")

        try:
            conn.begin(conn)

            order.status = "inactive"
            order.updated_at = datetime.utcnow()
            order.update(conn=conn)

            units = (
                ProductUnit()
                .where(
                    {
                        "unit_id": (
                            SaleDeliveryOrderProductUnit().fields(["unit_id"]).where({"order_id": order_id})
                        ).sql(remove_offset_limit=True),
                        "op": "in",
                    }
                )
                .all(conn=conn, collection=True)
            )

            for unit in units.all():
                unit.status = "active"
                unit.update(conn=conn)

            conn.commit(conn)

        except Exception as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return {}
