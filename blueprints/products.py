import cherrypy
import pymysql

# import uuid

from pytz import timezone

from helpers.helper_product_unit import HelperProductUnit
from helpers.helper_relation import HelperRelation

from utils.decorators import tools
from utils.query import _OR

# from utils.query import _AND
from utils.query import Query
from utils.utils import Utils
from utils.convert import Convert

from datetime import datetime
from models.serie import Serie

# from models.state import State
# from models.municipality import Municipality
# from models.locality import Locality

from models.brand import Brand
from models.brand_model import BrandModel
from models.version import Version

# from models.version import Version

from models.user import User
from models.company import Company
from models.branch_office import BranchOffice
from models.warehouse import Warehouse

# from models.supplier import Supplier
from models.employee import Employee
from models.employee_product import EmployeeProduct
from models.employee_product_unit import EmployeeProductUnit
from models.category import Category
from models.subcategory import SubCategory
from models.measure import Measure
from models.tax import Tax


from models.product import Product
from models.product_measure import ProductMeasure
from models.product_tax import ProductTax

from models.product_unit import ProductUnit
from models.product_related import ProductRelated

from models.v_product_car import vProductCar

from models.product_assignment import ProductAssignment
from models.product_assignment_item import ProductAssignmentItem
from models.product_assignment_document import ProductAssignmentDocument

from models.product_unit_spec import ProductUnitSpec
from models.product_unit_invoice import ProductUnitInvoice
from models.product_unit_config import ProductUnitConfig

from models.product_unit_assignment import ProductUnitAssignment
from models.product_unit_assignment_item import ProductUnitAssignmentItem
from models.product_unit_assignment_document import ProductUnitAssignmentDocument
from models.product_unit_car import ProductUnitCar
from models.product_unit_car_insurance import ProductUnitCarInsurance
from models.product_unit_car_circulation_card import ProductUnitCarCirculationCard

# from models.product_unit_car_measurement import ProductUnitCarMeasurement


# from models.work_order import WorkOrder
# from models.work_order_client import WorkOrderClient
# from models.work_order_product import WorkOrderProduct

# from models.unit_service_concept import UnitServiceConcept
from models.unit_maintenance import UnitMaintenance

# from models.unit_maintenance_concept import UnitMaintenanceConcept
# from models.unit_maintenance_evidence import UnitMaintenanceEvidence
# from models.unit_maintenance_next_service import UnitMaintenanceNextService

from models.stock import Stock

# from models.car_maintenance_notification import CarMaintenanceNotification


class MapProducts(object):
    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_products",
            "/catalog/products",
            controller=self,
            action="get_products",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_product_by_id",
            "/catalog/product/{product_id}",
            controller=self,
            action="get_product_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_product",
            "/catalog/product/{product_id}",
            controller=self,
            action="save_product",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "patch_product",
            "/catalog/product/{product_id}",
            controller=self,
            action="patch_product",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        mapper.connect(
            "delete_product",
            "/catalog/product/{product_id}",
            controller=self,
            action="delete_product",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_product_units",
            "/catalog/product/{product_id}/units",
            controller=self,
            action="get_product_units",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_product_unit_by_id",
            "/catalog/product/{product_id}/unit/{unit_id}",
            controller=self,
            action="get_product_unit_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_product_unit",
            "/catalog/product/{product_id}/unit/{unit_id}",
            controller=self,
            action="save_product_unit",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        # mapper.connect(
        #     "add_product_unit_logbook",
        #     "/catalog/product/{product_id}/unit/{unit_id}/logbook",
        #     controller=self,
        #     action="add_product_unit_logbook",
        #     conditions=dict(method=["POST", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "add_product_unit_logbook",
        #     "/catalog/product/{product_id}/unit/{unit_id}/logbook/{measurement_id}",
        #     controller=self,
        #     action="add_product_unit_logbook",
        #     conditions=dict(method=["POST", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "get_product_unit_logbook",
        #     "/catalog/product/{product_id}/unit/{unit_id}/logbook/{measurement_id}",
        #     controller=self,
        #     action="get_product_unit_logbook",
        #     conditions=dict(method=["GET", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "delete_product_unit",
        #     "/catalog/product/{product_id}/unit/{unit_id}",
        #     controller=self,
        #     action="delete_product_unit",
        #     conditions=dict(method=["DELETE", "OPTIONS"]),
        # )

        mapper.connect(
            "get_assigned_equipments",
            "/catalog/assigned-equipments",
            controller=self,
            action="get_assigned_equipments",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_assigned_equipment_by_id",
            "/catalog/assigned-equipment/{assignment_id}",
            controller=self,
            action="get_assigned_equipment_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_units_assignment",
            "/catalog/assign-equipment/{assignment_id}",
            controller=self,
            action="save_units_assignment",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "update_units_assignment",
            "/catalog/assign-equipment/{assignment_id}",
            controller=self,
            action="update_units_assignment",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        mapper.connect(
            "save_units_assignment",
            "/catalog/return-equipment/{assignment_id}",
            controller=self,
            action="save_units_assignment",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "update_units_assignment",
            "/catalog/return-equipment/{assignment_id}",
            controller=self,
            action="update_units_assignment",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        mapper.connect(
            "get_assigned_products",
            "/catalog/assigned-products",
            controller=self,
            action="get_assigned_products",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_assigned_product_by_id",
            "/catalog/assigned-product/{assignment_id}",
            controller=self,
            action="get_assigned_product_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_assignment",
            "/catalog/assign-product/{assignment_id}",
            controller=self,
            action="save_assignment",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "update_assignment",
            "/catalog/assign-product/{assignment_id}",
            controller=self,
            action="update_assignment",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        # mapper.connect(
        #     "save_assignment",
        #     "/catalog/return-product/{assignment_id}",
        #     controller=self,
        #     action="save_assignment",
        #     conditions=dict(method=["POST", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "get_units_services_concepts",
        #     "/catalog/units-services-concepts",
        #     controller=self,
        #     action="get_units_services_concepts",
        #     conditions=dict(method=["GET", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "get_unit_service_concept_by_id",
        #     "/catalog/unit-service-concept/{service_id}",
        #     controller=self,
        #     action="get_unit_service_concept_by_id",
        #     conditions=dict(method=["GET", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "save_unit_service_concept",
        #     "/catalog/unit-service-concept/{service_id}",
        #     controller=self,
        #     action="save_unit_service_concept",
        #     conditions=dict(method=["POST", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "delete_unit_service_concept",
        #     "/catalog/unit-service-concept/{service_id}",
        #     controller=self,
        #     action="delete_unit_service_concept",
        #     conditions=dict(method=["DELETE", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "get_units_maintenances",
        #     "/catalog/units-maintenances",
        #     controller=self,
        #     action="get_units_maintenances",
        #     conditions=dict(method=["GET", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "get_unit_maintenance_by_id",
        #     "/catalog/unit-maintenance/{maintenance_id}",
        #     controller=self,
        #     action="get_unit_maintenance_by_id",
        #     conditions=dict(method=["GET", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "save_unit_maintenance",
        #     "/catalog/unit-maintenance/{maintenance_id}",
        #     controller=self,
        #     action="save_unit_maintenance",
        #     conditions=dict(method=["POST", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "get_product_units_logbook",
        #     "/helper/cars-logbook",
        #     controller=self,
        #     action="get_product_units_logbook",
        #     conditions=dict(method=["GET", "OPTIONS"]),
        # )

        # mapper.connect(
        #     "get_product_units_notifications",
        #     "/helper/units-maintenances-history",
        #     controller=self,
        #     action="get_product_units_notifications",
        #     conditions=dict(method=["GET", "OPTIONS"]),
        # )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_products(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        type = kwargs.get("type", None)
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [
            _OR(
                {"code": look_for, "op": "like"},
                {"name": look_for, "op": "like"},
                {"description": look_for, "op": "like"},
            )
        ]

        if type:
            criterias.append({"type": type})

        # This is really specific, if this need to grow
        # it's better to move this sections to a helper
        criterias = criterias + Utils().convert_filters(
            filters=filters,
            ignore=["related-to-work-order-client", "related-to-employee-equipment", "type"],
            force_status=True,
        )

        filter = Utils().get_filter(filters=filters, key="type")
        if filter:
            criterias.append({"type": filter["type"].split(","), "op": "in"})

        # related_to_contract = Utils().get_filter(filters=filters, key="related-to-work-order-client")
        # if related_to_contract:
        #     criterias.append(
        #         {
        #             "product_id": (
        #                 WorkOrderProduct()
        #                 .fields(["item_id"])
        #                 .where(
        #                     {
        #                         "work_order_id": (
        #                             WorkOrder()
        #                             .fields(["work_order_id"])
        #                             .where(
        #                                 _OR(
        #                                     {
        #                                         "client_id": related_to_contract["related-to-work-order-client"],
        #                                         "op": "in",
        #                                     },
        #                                     {
        #                                         "work_order_id": (
        #                                             WorkOrderClient()
        #                                             .fields(["work_order_id"])
        #                                             .where(
        #                                                 {
        #                                                     "client_id": related_to_contract[
        #                                                         "related-to-work-order-client"
        #                                                     ],
        #                                                     "op": "in",
        #                                                 },
        #                                                 {"status": "active"},
        #                                             )
        #                                             .sql(remove_offset_limit=True)
        #                                         ),
        #                                         "op": "in",
        #                                     },
        #                                 ),
        #                                 {"end_at": datetime.utcnow(), "op": "gt"},
        #                                 {"status": "active"},
        #                             )
        #                             .sql(remove_offset_limit=True)
        #                         ),
        #                         "op": "in",
        #                     },
        #                     {"status": "active"},
        #                 )
        #                 .sql(remove_offset_limit=True)
        #             ),
        #             "op": "in",
        #         }
        #     )

        # has "related-to-employee-equipment"
        filter = Utils().get_filter(filters=filters, key="related-to-employee-equipment")
        if filter:
            criterias.append(
                {
                    "product_id": (
                        EmployeeProductUnit()
                        .fields(["product_id"])
                        .where(
                            {
                                "employee_id": filter["related-to-employee-equipment"],
                                "status": "assigned",
                            }
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        conn = Product().get_connection()
        query = Query(model=Product())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code", "name"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for product in result["results"]:
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

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_product_by_id(self, **kwargs):
        # Get body content
        product_id = kwargs.get("product_id", None)

        conn = Product().get_connection()
        product = Product().where({"product_id": product_id}).one_or_none(conn=conn)

        if product is None:
            raise cherrypy.HTTPError(404, "Not Found")

        brand = Brand().where({"brand_id": product.brand_id}).one_or_none(conn=conn)
        model = (
            BrandModel()
            .where(
                {"brand_id": product.brand_id},
                {"model_id": product.model_id},
            )
            .one_or_none(conn=conn)
        )

        category = Category().where({"category_id": product.category_id}).one_or_none(conn=conn)

        subcategory = (
            SubCategory()
            .where(
                {"category_id": product.category_id},
                {"subcategory_id": product.subcategory_id},
            )
            .one_or_none(conn=conn)
        )

        result = ProductMeasure().where({"product_id": product_id}, {"status": "active"}).all(conn=conn)

        measures = []
        for item in result.all():
            measure = Measure().where({"measure_id": item.measure_id}).one_or_none(conn=conn)
            m_data = measure.as_dict()
            m_data.update(item.as_dict())
            measures.append(m_data)

        result = ProductTax().where({"product_id": product_id}, {"status": "active"}).all(conn=conn)

        taxes = []
        for item in result.all():
            tax = Tax().where({"tax_id": item.tax_id}).one_or_none(conn=conn)
            m_data = tax.as_dict()
            m_data.update(item.as_dict())
            taxes.append(m_data)

        result = ProductRelated().where({"product_id": product_id}, {"status": "active"}).all(conn=conn)

        products_related = []
        for item in result.all():
            related = Product().where({"product_id": item.item_id}).one_or_none(conn=conn)

            related_measure = Measure().where({"measure_id": item.measure_id}).one_or_none(conn=conn)
            m_data = item.as_dict()
            m_data["product"] = related.as_dict()
            m_data["measure"] = related_measure.as_dict()
            products_related.append(m_data)

        product = product.as_dict()
        product["brand"] = brand.as_dict()
        product["model"] = model.as_dict()
        product["category"] = category.as_dict()
        product["subcategory"] = subcategory.as_dict()
        product["measures"] = measures
        product["taxes"] = taxes
        product["related"] = products_related

        return product

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "product_id",
            "brand_id",
            "model_id",
            "category_id",
            "subcategory_id",
            "name",
            "short_name",
            "description",
            "-image",
            "currency",
            "type",
            "measures",
            "taxes",
            "related",
            "has_units",
            "status",
        ]
    )
    def save_product(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        product_id = body.get("product_id", None)
        category_id = body.get("category_id", None)
        subcategory_id = body.get("subcategory_id", None)

        measures = body.get("measures", [])
        taxes = body.get("taxes", [])
        related = body.get("related", [])

        conn = Product().get_connection()
        category = Category().where({"category_id": category_id}).one_or_none(conn=conn)

        if category is None:
            raise cherrypy.HTTPError(404, "Not Found Category")

        subcategory = (
            SubCategory()
            .where({"category_id": category_id}, {"subcategory_id": subcategory_id})
            .one_or_none(conn=conn)
        )

        if subcategory is None:
            raise cherrypy.HTTPError(404, "Not Found SubCategory")

        try:
            conn.begin(conn)

            product = Product().where({"product_id": product_id}).one_or_none(conn=conn)

            is_new = False
            if product is None:
                is_new = True
                body["code"] = Serie.generate(prefix=body["type"][0], reference="general", key=body["type"])
                product = Product()
                product.created_at = datetime.utcnow()

            product.set_attrs(body, validate_unknown=False)

            product.updated_at = datetime.utcnow()
            if is_new:
                product.insert(conn=conn)
            else:
                product.update(conn=conn)

            # disable current measures
            result = ProductMeasure().where({"product_id": product_id}, {"status": "active"}).all(conn=conn)

            for item in result.all():
                item.status = "inactive"
                item.updated_at = datetime.utcnow()
                item.update(conn=conn)

            # add new measures
            for item in measures:
                measure = ProductMeasure()
                measure.product_id = product_id
                measure.set_attrs(item, validate_unknown=False, ignore_restricted=True)
                measure.status = "active"
                measure.created_at = datetime.utcnow()
                measure.updated_at = datetime.utcnow()
                measure.update_or_insert(conn=conn)

            # disable current taxes
            result = ProductTax().where({"product_id": product_id}, {"status": "active"}).all(conn=conn)

            for item in result.all():
                item.status = "inactive"
                item.updated_at = datetime.utcnow()
                item.update(conn=conn)

            # add new taxes
            for item in taxes:
                tax = ProductTax()
                tax.product_id = product_id
                tax.set_attrs(item, validate_unknown=False, ignore_restricted=True)
                tax.status = "active"
                tax.created_at = datetime.utcnow()
                tax.updated_at = datetime.utcnow()
                tax.update_or_insert(conn=conn)

            # disable current related products
            result = ProductRelated().where({"product_id": product_id}, {"status": "active"}).all(conn=conn)

            for item in result.all():
                item.status = "inactive"
                item.updated_at = datetime.utcnow()
                item.update(conn=conn)

            # add new related products
            for item in related:
                related = ProductRelated()
                related.product_id = product_id
                related.set_attrs(item, validate_unknown=False, ignore_restricted=True)
                related.status = "active"
                related.created_at = datetime.utcnow()
                related.updated_at = datetime.utcnow()
                related.update_or_insert(conn=conn)

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
    @cherrypy.tools.json_in()
    @tools.secured()
    def patch_product(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        product_id = kwargs.get("product_id", None)

        conn = Product().get_connection()
        product = Product().where({"product_id": product_id}).one_or_none(conn=conn)

        if product is None:
            raise cherrypy.HTTPError(404, "Not Found")

        product.set_attrs(body, validate_unknown=False)
        product.updated_at = datetime.utcnow()
        product.update(conn=conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_product(self, **kwargs):
        # Get body content
        product_id = kwargs.get("product_id", None)

        product = Product().where({"product_id": product_id}).one_or_none()

        if product is None:
            raise cherrypy.HTTPError(404, "Not Found")

        product.status = "inactive"
        product.updated_at = datetime.utcnow()
        product.update()

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_product_units(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        product_id = kwargs.get("product_id", None)
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")
        order_by = kwargs.get("order_by", "-code").split(",")

        criterias = [
            {"product_id": product_id},
            _OR(
                {"code": look_for, "op": "like"},
                {"serie": look_for, "op": "like"},
                {"reference": look_for, "op": "like"},
                {"uid": look_for, "op": "like"},
            ),
        ]

        criterias = criterias + Utils().convert_filters(
            filters,
            ignore=[
                "related-to-employee-equipment",
                "invoice_agency",
                "invoice_client",
                "invoice_amount",
                "department",
                "work_area",
                "circulation_card_expedition_date",
                "circulation_card_register_id",
                "circulation_card_amount",
                "insurance_expedition_date",
                "insurance_folio",
                "insurance_amount",
            ],
            force_status=False,
        )

        # has "related-to-employee-equipment"
        filter = Utils().get_filter(filters=filters, key="related-to-employee-equipment")
        if filter:
            criterias.append(
                {
                    "unit_id": (
                        EmployeeProductUnit()
                        .fields(["unit_id"])
                        .where(
                            {"employee_id": filter["related-to-employee-equipment"]},
                            {"status": "assigned"},
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "invoice_agency"
        filter = Utils().get_filter(filters=filters, key="invoice_agency")
        if filter:
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitInvoice()
                        .fields(["unit_id"])
                        .where(
                            {
                                "agency": filter["invoice_agency"],
                                "op": filter["op"],
                            }
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "invoice_client"
        filter = Utils().get_filter(filters=filters, key="invoice_client")
        if filter:
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitInvoice()
                        .fields(["unit_id"])
                        .where(
                            {
                                "client": filter["invoice_client"],
                                "op": filter["op"],
                            }
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "invoice_amount"
        filter = Utils().get_filter(filters=filters, key="invoice_amount")
        if filter:
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitInvoice()
                        .fields(["unit_id"])
                        .where(
                            {
                                "total": float(filter["invoice_amount"]),
                                "op": filter["op"],
                            }
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # # has "department"
        # filter = Utils().get_filter(filters=filters, key="department")
        # if filter:
        #     criterias.append(
        #         {
        #             "unit_id": (
        #                 EmployeeProductUnit()
        #                 .fields(["unit_id"])
        #                 .where(
        #                     {
        #                         "employee_id": (
        #                             Employee()
        #                             .fields(["employee_id"])
        #                             .where({"department": filter["department"]})
        #                             .sql(remove_offset_limit=True)
        #                         ),
        #                         "op": "in",
        #                     },
        #                     {"status": "assigned"},
        #                 )
        #                 .sql(remove_offset_limit=True)
        #             ),
        #             "op": "in",
        #         }
        #     )

        # # has "work_area"
        # filter = Utils().get_filter(filters=filters, key="work_area")
        # if filter:
        #     criterias.append(
        #         {
        #             "unit_id": (
        #                 EmployeeProductUnit()
        #                 .fields(["unit_id"])
        #                 .where(
        #                     {
        #                         "employee_id": (
        #                             Employee()
        #                             .fields(["employee_id"])
        #                             .where({"work_area": filter["work_area"]})
        #                             .sql(remove_offset_limit=True)
        #                         ),
        #                         "op": "in",
        #                     },
        #                     {"status": "assigned"},
        #                 )
        #                 .sql(remove_offset_limit=True)
        #             ),
        #             "op": "in",
        #         }
        #     )

        # has "circulation_card_expedition_date"
        filter = Utils().get_filter(filters=filters, key="circulation_card_expedition_date")
        if filter:
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitCar()
                        .fields(["unit_id"])
                        .where({"has_circulation_card": 1})
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitCarCirculationCard()
                        .fields(["unit_id"])
                        .where(
                            {
                                "expiration_date": filter["circulation_card_expedition_date"],
                                "op": filter["op"],
                            }
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "circulation_card_register_id"
        filter = Utils().get_filter(filters=filters, key="circulation_card_register_id")
        if filter:
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitCarCirculationCard()
                        .fields(["unit_id"])
                        .where(
                            {
                                "register_id": filter["circulation_card_register_id"],
                                "op": filter["op"],
                            }
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "circulation_card_amount"
        filter = Utils().get_filter(filters=filters, key="circulation_card_amount")
        if filter:
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitCarCirculationCard()
                        .fields(["unit_id"])
                        .where(
                            {
                                "total": float(filter["circulation_card_amount"]),
                                "op": filter["op"],
                            }
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "insurance_expedition_date"
        filter = Utils().get_filter(filters=filters, key="insurance_expedition_date")
        if filter:
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitCar().fields(["unit_id"]).where({"has_insurance": 1}).sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitCarInsurance()
                        .fields(["unit_id"])
                        .where(
                            {
                                "expiration_date": filter["insurance_expedition_date"],
                                "op": filter["op"],
                            }
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "insurance_folio"
        filter = Utils().get_filter(filters=filters, key="insurance_folio")
        if filter:
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitCarInsurance()
                        .fields(["unit_id"])
                        .where(
                            {
                                "folio": filter["insurance_folio"],
                                "op": filter["op"],
                            }
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "insurance_amount"
        filter = Utils().get_filter(filters=filters, key="insurance_amount")
        if filter:
            criterias.append(
                {
                    "unit_id": (
                        ProductUnitCarInsurance()
                        .fields(["unit_id"])
                        .where(
                            {
                                "total": float(filter["insurance_amount"]),
                                "op": filter["op"],
                            }
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        conn = ProductUnit().get_connection()
        query = Query(model=ProductUnit())
        if product_id in [
            # car
            "e776a49c-2173-4b21-b69a-fe9a1ff35caa",
            "5d7b8a14-23ea-41f4-b7d7-9ddb33b3d964",
        ]:
            query = Query(model=vProductCar())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(order_by)

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for unit in result["results"]:
            unit["company"] = Company().where({"company_id": unit["company_id"]}).one_or_none(conn=conn).as_dict()

            unit["product"] = Product().where({"product_id": unit["product_id"]}).one_or_none(conn=conn).as_dict()

            unit["brand"] = Brand().where({"brand_id": unit["brand_id"]}).one_or_none(conn=conn).as_dict()

            unit["model"] = (
                BrandModel()
                .where({"brand_id": unit["brand_id"]}, {"model_id": unit["model_id"]})
                .one_or_none(conn=conn)
                .as_dict()
            )

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

            invoice = ProductUnitInvoice().where({"unit_id": unit["unit_id"]}).one_or_none(conn=conn)
            unit["invoice"] = invoice.as_dict() if invoice else {}

            # Special Unit Type ?
            if product_id in [
                # car
                "e776a49c-2173-4b21-b69a-fe9a1ff35caa",
                "5d7b8a14-23ea-41f4-b7d7-9ddb33b3d964",
            ]:
                car = ProductUnitCar().where({"unit_id": unit["unit_id"]}).one_or_none(conn=conn)

                unit.update(car.as_dict() if car else {})

                unit["circulation_card_status"] = "undefined"
                unit["circulation_card_expiration_date"] = "undefined"

                unit["insurance_status"] = "undefined"
                unit["insurance_expiration_date"] = "undefined"

                if unit["has_insurance"]:
                    sql = ("""
                            SELECT *, (`expiration_date` > NOW()) AS `is_valid`
                            FROM `{table}`
                            WHERE
                                `product_id`=%s AND
                                `unit_id`=%s

                        """).format(table=ProductUnitCarInsurance()._TABLE)

                    args = [
                        unit["product_id"],
                        unit["unit_id"],
                    ]
                    rows = conn.execute(sql, *args, connection=None)
                    unit["insurance_status"] = "valid" if rows[0]["is_valid"] else "expired"
                    unit["insurance_expiration_date"] = rows[0]["expiration_date"]

                if unit["has_circulation_card"]:
                    sql = ("""
                            SELECT *, (`expiration_date` > NOW()) AS `is_valid`
                            FROM `{table}`
                            WHERE
                                `product_id`=%s AND
                                `unit_id`=%s
                        """).format(table=ProductUnitCarCirculationCard()._TABLE)

                    args = [
                        unit["product_id"],
                        unit["unit_id"],
                    ]
                    rows = conn.execute(sql, *args, connection=None)
                    unit["circulation_card_status"] = "valid" if rows[0]["is_valid"] else "expired"
                    unit["circulation_card_expiration_date"] = rows[0]["expiration_date"]

            if unit["status"] == "assigned":
                employee = (
                    Employee()
                    .where(
                        {
                            "employee_id": (
                                EmployeeProductUnit()
                                .fields(["employee_id"])
                                .where({"unit_id": unit["unit_id"]}, {"status": "assigned"})
                                .sql(remove_offset_limit=True)
                            ),
                            "op": "in",
                        }
                    )
                    .one_or_none()
                )

                unit["employee"] = None
                if employee:
                    unit["employee"] = employee.as_dict()
                    unit["employee"]["department"] = (
                        Category()
                        .where({"category_id": unit["employee"]["department_id"]})
                        .one_or_none(conn=conn)
                        .as_dict()
                    )

                    unit["employee"]["work_area"] = (
                        Category()
                        .where({"category_id": unit["employee"]["work_area_id"]})
                        .one_or_none(conn=conn)
                        .as_dict()
                    )

            # in maintenance
            sql = ("""
                    SELECT count(*) AS `total`
                    FROM `{table}`
                    WHERE
                        `product_id`=%s AND
                        `unit_id`=%s AND
                        `status` = "in-progress"
                """).format(table=UnitMaintenance()._TABLE)

            args = [
                unit["product_id"],
                unit["unit_id"],
            ]
            rows = conn.execute(sql, *args, connection=None)
            unit["in_maintenance"] = True if rows[0]["total"] > 0 else False

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    # @tools.secured()
    def get_product_unit_by_id(self, **kwargs):
        # Get body content
        product_id = kwargs.get("product_id", None)
        unit_id = kwargs.get("unit_id", None)

        conn = ProductUnit().get_connection()
        unit = HelperProductUnit.get(product_id=product_id, unit_id=unit_id, conn=conn)

        return unit

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "product_id",
            "unit_id",
            "product_id",
            "brand_id",
            "model_id",
            "version_id",
            "serie",
            "reference",
            "uid",
            "description",
            "specs",
            "invoice",
            "status",
        ]
    )
    def save_product_unit(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        product_id = body.get("product_id", None)
        unit_id = body.get("unit_id", None)

        conn = ProductUnit().get_connection()

        product = Product().where({"product_id": product_id}).one_or_none(conn=conn)

        if product is None:
            raise cherrypy.HTTPError(404, "Not Found")

        try:
            unit = ProductUnit().where({"unit_id": unit_id}).one_or_none(conn=conn)

            is_new = False
            if unit is None:
                is_new = True
                body["code"] = Serie.generate(
                    reference="product_{}".format(product_id),
                    key="unit",
                    prefix=product.code,
                )
                unit = ProductUnit()
                unit.created_at = datetime.utcnow()

            unit.set_attrs(body, validate_unknown=False)
            unit.updated_at = datetime.utcnow()

            if is_new:
                unit.insert(conn=conn)
            else:
                unit.update(conn=conn)

            # remove concepts
            sql = ("""
                    DELETE FROM `{table}`
                    WHERE
                        `product_id` = %s AND
                        `unit_id` = %s
                """).format(table=ProductUnitSpec()._TABLE)
            args = [product_id, unit_id]
            conn.execute(sql, *args, connection=None)

            for index, spec in enumerate(body["specs"]):
                item = ProductUnitSpec()
                item.product_id = product_id
                item.unit_id = unit_id
                item.set_attrs(spec, validate_unknown=False, ignore_restricted=True)
                item.index = index
                item.created_at = unit.created_at
                item.updated_at = unit.updated_at
                item.insert(conn=conn)

            invoice = ProductUnitInvoice()
            invoice.set_attrs(body["invoice"], validate_unknown=False)
            invoice.created_at = unit.created_at
            invoice.updated_at = unit.updated_at
            invoice.update_or_insert(conn=conn)

            config = ProductUnitConfig().where({"product_id": product_id}, {"unit_id": unit_id}).one_or_none(conn=conn)

            if config is None:
                config = ProductUnitConfig()
                config.set_attrs(body["config"], validate_unknown=False)
                config.created_at = unit.created_at
                config.updated_at = unit.updated_at
                config.insert(conn=conn)

            if "per_hours" in body["config"]:
                config.per_hours = body["config"]["per_hours"]

            if "per_mileage" in body["config"]:
                config.per_mileage = body["config"]["per_mileage"]

            if "per_days" in body["config"]:
                config.per_days = body["config"]["per_days"]

            config.created_at = unit.created_at
            config.update(conn=conn)

            # Special Unit Type ?
            if product_id in [
                # car
                "e776a49c-2173-4b21-b69a-fe9a1ff35caa",
                "5d7b8a14-23ea-41f4-b7d7-9ddb33b3d964",
            ]:
                car = ProductUnitCar()
                car.set_attrs(body, validate_unknown=False)
                car.created_at = unit.created_at
                car.updated_at = unit.updated_at
                car.update_or_insert(conn=conn)

                insurance = ProductUnitCarInsurance()
                insurance.set_attrs(body["insurance"], validate_unknown=False)
                insurance.created_at = unit.created_at
                insurance.updated_at = unit.updated_at
                insurance.update_or_insert(conn=conn)

                circulation_card = ProductUnitCarCirculationCard()
                circulation_card.set_attrs(body["circulation_card"], validate_unknown=False)
                circulation_card.created_at = unit.created_at
                circulation_card.updated_at = unit.updated_at
                circulation_card.update_or_insert(conn=conn)

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
    def delete_product_unit(self, **kwargs):
        # Get body content
        unit_id = kwargs.get("unit_id", None)

        unit = ProductUnit().where({"unit_id": unit_id}).one_or_none()

        if unit is None:
            raise cherrypy.HTTPError(404, "Not Found")

        unit.status = "inactive"
        unit.updated_at = datetime.utcnow()
        unit.update()

        return {}

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @cherrypy.tools.json_in()
    # @tools.validate_body_params(
    #     [
    #         "product_id",
    #         "unit_id",
    #         "source",
    #         "reference",
    #         "fuel",
    #         "hours",
    #         "previous_mileage",
    #         "mileage",
    #         "status",
    #     ]
    # )
    # def add_product_unit_logbook(self, **kwargs):
    #     # Get body content
    #     body = cherrypy.request.json
    #     product_id = body.get("product_id", None)
    #     unit_id = body.get("unit_id", None)
    #     measurement_id = body.get("measurement_id", str(uuid.uuid4()))

    #     conn = ProductUnit().get_connection()

    #     product = Product().where({"product_id": product_id}).one_or_none(conn=conn)

    #     if product is None:
    #         raise cherrypy.HTTPError(404, "Not Found")

    #     unit = ProductUnit().where({"unit_id": unit_id}).one_or_none(conn=conn)

    #     if unit is None:
    #         raise cherrypy.HTTPError(404, "Not Found")

    #     is_new = False
    #     measurement = ProductUnitCarMeasurement().where({"measurement_id": measurement_id}).one_or_none(conn=conn)
    #     if measurement is None:
    #         is_new = True
    #         measurement = ProductUnitCarMeasurement()
    #         measurement.measurement_id = measurement_id
    #         measurement.created_at = datetime.utcnow()
    #         measurement.updated_at = datetime.utcnow()
    #     else:
    #         # update previus_mileage in next registers
    #         # disable current employees
    #         sql = (
    #             """
    #                 UPDATE `{table}`
    #                 SET
    #                     `previous_mileage` = %s
    #                 WHERE
    #                     `product_id` = %s AND
    #                     `unit_id` = %s AND
    #                     `previous_mileage` = %s AND
    #                     `created_at` > %s
    #             """
    #         ).format(table=ProductUnitCarMeasurement()._TABLE)

    #         args = [
    #             body.get("mileage"),
    #             measurement.product_id,
    #             measurement.unit_id,
    #             measurement.mileage,
    #             measurement.created_at,
    #         ]
    #         conn.execute(sql, *args, connection=None)

    #     measurement.product_id = product_id
    #     measurement.unit_id = unit_id
    #     measurement.set_attrs(body, validate_unknown=False)
    #     measurement.insert(conn=conn) if is_new else measurement.update(conn=conn)

    #     return {}

    # @tools.cors
    # @cherrypy.tools.json_out()
    # def get_product_unit_logbook(self, **kwargs):
    #     product_id = kwargs.get("product_id", None)
    #     unit_id = kwargs.get("unit_id", None)
    #     measurement_id = kwargs.get("measurement_id", None)

    #     conn = ProductUnit().get_connection()

    #     product = Product().where({"product_id": product_id}).one_or_none(conn=conn)
    #     if product is None:
    #         raise cherrypy.HTTPError(404, "Not Found")

    #     unit = ProductUnit().where({"unit_id": unit_id}).one_or_none(conn=conn)
    #     if unit is None:
    #         raise cherrypy.HTTPError(404, "Not Found")

    #     measurement = ProductUnitCarMeasurement().where({"measurement_id": measurement_id}).one_or_none(conn=conn)
    #     if measurement is None:
    #         raise cherrypy.HTTPError(404, "Not Found")

    #     log = measurement.as_dict()
    #     log["unit"] = HelperProductUnit.get(product_id=product_id, unit_id=unit_id, conn=conn)

    #     return log

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_assigned_equipments(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")
        sort = kwargs.get("sort", ["-transaction_date"])

        criterias = [_OR({"code": look_for, "op": "like"})]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        query = Query(model=ProductUnitAssignment())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(sort)

        conn = ProductUnitAssignment().get_connection()
        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        # company = (
        #     Company()
        #     .where({"company_id": "17805fe9-c51e-43fd-9235-72f7477b1464"})
        #     .one_or_none(conn=conn)
        #     .as_dict()
        # )

        for item in result["results"]:
            item["user"] = User().where({"user_id": item["user_id"]}).one_or_none(conn=conn).as_dict()

            item["employee"] = Employee().where({"employee_id": item["employee_id"]}).one_or_none(conn=conn).as_dict()

            item["department"] = (
                Category().where({"category_id": item["department_id"]}).one_or_none(conn=conn).as_dict()
            )

            item["work_area"] = (
                Category().where({"category_id": item["work_area_id"]}).one_or_none(conn=conn).as_dict()
            )

            # item["employee"]["department"] = (
            #     Category()
            #     .where({"category_id": item["employee"]["department"]})
            #     .one_or_none(conn=conn)
            #     .as_dict()
            # )

            # item["employee"]["work_area"] = (
            #     Category()
            #     .where({"category_id": item["employee"]["work_area"]})
            #     .one_or_none(conn=conn)
            #     .as_dict()
            # )

            # item["employee"]["work_position"] = (
            #     Category()
            #     .where({"category_id": item["employee"]["work_position"]})
            #     .one_or_none(conn=conn)
            #     .as_dict()
            # )

            # item["equipment"] = (
            #     ProductUnitAssignmentItem()
            #     .where({"assignment_id": item["assignment_id"]})
            #     .all(conn=conn, collection=False)
            # )

            # for entry in item["equipment"]:
            #     entry.update(
            #         HelperProductUnit.get(
            #             product_id=entry["product_id"],
            #             unit_id=entry["unit_id"],
            #             conn=conn,
            #         )
            #     )

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_assigned_equipment_by_id(self, **kwargs):
        # Get body content
        assignment_id = kwargs.get("assignment_id", None)

        conn = ProductUnitAssignment().get_connection()
        assignment = ProductUnitAssignment().where({"assignment_id": assignment_id}).one_or_none(conn=conn)

        if assignment is None:
            raise cherrypy.HTTPError(404, "Not Found")

        assignment = assignment.as_dict()
        assignment["user"] = User().where({"user_id": assignment["user_id"]}).one_or_none(conn=conn).as_dict()

        assignment["employee"] = (
            Employee().where({"employee_id": assignment["employee_id"]}).one_or_none(conn=conn).as_dict()
        )

        assignment["department"] = (
            Category().where({"category_id": assignment["department_id"]}).one_or_none(conn=conn).as_dict()
        )

        assignment["work_area"] = (
            Category().where({"category_id": assignment["work_area_id"]}).one_or_none(conn=conn).as_dict()
        )

        assignment["company"] = HelperRelation.get_company(company_id=assignment["employee"]["company_id"])

        assignment["equipment"] = (
            ProductUnitAssignmentItem().where({"assignment_id": assignment_id}).all(conn=conn, collection=False)
        )

        for item in assignment["equipment"]:
            item.update(HelperProductUnit.get(product_id=item["product_id"], unit_id=item["unit_id"], conn=conn))

        assignment["documents"] = (
            ProductUnitAssignmentDocument()
            .where({"assignment_id": assignment_id})
            .all(collection=False, ignore_limit=True, conn=conn)
        )

        return assignment

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "assignment_id",
            "transaction_date",
            "type",
            "user_id",
            "employee_id",
            "department_id",
            "work_area_id",
            "notes",
            "equipment",
            "documents",
        ]
    )
    def save_units_assignment(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        assignment_id = body.get("assignment_id", None)
        documents = body.get("documents", [])

        conn = ProductUnitAssignment().get_connection()
        assignment = ProductUnitAssignment().where({"assignment_id": assignment_id}).one_or_none(conn=conn)

        if assignment:
            raise cherrypy.HTTPError(409, "Conflict - Duplicate Document")

        try:
            conn.begin(conn)

            body["code"] = "AP{date}{number}".format(
                date=Convert().datetime2str(dt=None, tz=timezone("America/Mazatlan"), format="%d%m%y"),
                number=Serie.generate(reference="general", key="units-assignments", conn=conn),
            )

            assignment = ProductUnitAssignment()
            assignment.set_attrs(body, validate_unknown=False)
            assignment.status = "active"
            assignment.updated_at = datetime.utcnow()
            assignment.created_at = datetime.utcnow()

            assignment.insert(conn=conn)

            for entry in body["equipment"]:
                item = ProductUnitAssignmentItem()
                item.set_attrs(entry, validate_unknown=False, ignore_restricted=True)
                item.assignment_id = assignment_id
                item.type = assignment.type
                item.updated_at = datetime.utcnow()
                item.created_at = datetime.utcnow()
                item.insert(conn=conn)

                u = EmployeeProductUnit()
                u.employee_id = assignment.employee_id
                u.product_id = item.product_id
                u.unit_id = item.unit_id
                u.status = "assigned" if assignment.type == "assignment" else "returned"
                u.updated_at = datetime.utcnow()
                u.created_at = datetime.utcnow()
                u.update_or_insert(conn=conn)

                unit = (
                    ProductUnit()
                    .where({"product_id": item.product_id}, {"unit_id": item.unit_id})
                    .one_or_none(conn=conn)
                )
                unit.status = "assigned" if assignment.type == "assignment" else "active"
                unit.updated_at = datetime.utcnow()
                unit.created_at = datetime.utcnow()
                unit.update(conn=conn)

            for item in documents:
                if item == "":
                    continue
                tag = item.split("/")[-1]
                document_id = tag.split(".")[0]

                document = ProductUnitAssignmentDocument()
                document.assignment_id = assignment_id
                document.document_id = document_id
                document.path = item
                document.created_at = datetime.utcnow()
                document.updated_at = datetime.utcnow()
                document.insert(conn=conn)

        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))
        finally:
            conn.commit(conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "assignment_id",
            "documents",
        ]
    )
    def update_units_assignment(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        assignment_id = body.get("assignment_id", None)
        documents = body.get("documents", [])

        conn = ProductUnitAssignment().get_connection()
        assignment = ProductUnitAssignment().where({"assignment_id": assignment_id}).one_or_none(conn=conn)

        if not assignment:
            raise cherrypy.HTTPError(404, "Not Found")

        try:
            conn.begin(conn)

            # remove documents
            sql = ("""
                    DELETE FROM `{table}`
                    WHERE
                        `assignment_id` = %s
                """).format(table=ProductUnitAssignmentDocument()._TABLE)

            args = [assignment_id]
            conn.execute(sql, *args, connection=None)

            for item in documents:
                if item == "":
                    continue
                tag = item.split("/")[-1]
                document_id = tag.split(".")[0]

                document = ProductUnitAssignmentDocument()
                document.assignment_id = assignment_id
                document.document_id = document_id
                document.path = item
                document.created_at = datetime.utcnow()
                document.updated_at = datetime.utcnow()
                document.insert(conn=conn)

        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))
        finally:
            conn.commit(conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_assigned_products(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")
        sort = kwargs.get("sort", ["-transaction_date"])

        criterias = [_OR({"code": look_for, "op": "like"})]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        query = Query(model=ProductAssignment())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(sort)

        conn = ProductAssignment().get_connection()
        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for item in result["results"]:
            item["user"] = User().where({"user_id": item["user_id"]}).one_or_none(conn=conn).as_dict()

            # item["assigned_by"] = (
            #     Employee()
            #     .where({"employee_id": item["assigned_by"]})
            #     .one_or_none(conn=conn)
            #     .as_dict()
            # )

            item["employee"] = Employee().where({"employee_id": item["employee_id"]}).one_or_none(conn=conn).as_dict()

            item["department"] = (
                Category().where({"category_id": item["department_id"]}).one_or_none(conn=conn).as_dict()
            )

            item["work_area"] = (
                Category().where({"category_id": item["work_area_id"]}).one_or_none(conn=conn).as_dict()
            )

            item["company"] = Company().where({"company_id": item["company_id"]}).one_or_none(conn=conn).as_dict()

            item["branch"] = BranchOffice().where({"branch_id": item["branch_id"]}).one_or_none(conn=conn).as_dict()

            item["warehouse"] = (
                Warehouse().where({"warehouse_id": item["warehouse_id"]}).one_or_none(conn=conn).as_dict()
            )

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_assigned_product_by_id(self, **kwargs):
        # Get body content
        assignment_id = kwargs.get("assignment_id", None)

        conn = ProductAssignment().get_connection()
        assignment = ProductAssignment().where({"assignment_id": assignment_id}).one_or_none(conn=conn)

        if assignment is None:
            raise cherrypy.HTTPError(404, "Not Found")

        assignment = assignment.as_dict()
        assignment["user"] = User().where({"user_id": assignment["user_id"]}).one_or_none(conn=conn).as_dict()

        # assignment["assigned_by"] = (
        #     Employee()
        #     .where({"employee_id": assignment["assigned_by"]})
        #     .one_or_none(conn=conn)
        #     .as_dict()
        # )

        assignment["employee"] = (
            Employee().where({"employee_id": assignment["employee_id"]}).one_or_none(conn=conn).as_dict()
        )

        assignment["department"] = (
            Category().where({"category_id": assignment["department_id"]}).one_or_none(conn=conn).as_dict()
        )

        assignment["work_area"] = (
            Category().where({"category_id": assignment["work_area_id"]}).one_or_none(conn=conn).as_dict()
        )

        assignment["company"] = HelperRelation.get_company(company_id=assignment["company_id"])

        assignment["branch"] = (
            BranchOffice().where({"branch_id": assignment["branch_id"]}).one_or_none(conn=conn).as_dict()
        )

        assignment["warehouse"] = (
            Warehouse().where({"warehouse_id": assignment["warehouse_id"]}).one_or_none(conn=conn).as_dict()
        )

        # assignment["department"] = (
        #     Category()
        #     .where({"category_id": assignment["department_id"]})
        #     .one_or_none(conn=conn)
        #     .as_dict()
        # )

        # assignment["work_area"] = (
        #     Category()
        #     .where({"category_id": assignment["work_area_id"]})
        #     .one_or_none(conn=conn)
        #     .as_dict()
        # )

        items = ProductAssignmentItem().where({"assignment_id": assignment_id}).all(conn=conn, collection=False)

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
        assignment["products"] = sorted(products, key=lambda i: i["name"])

        assignment["documents"] = (
            ProductAssignmentDocument()
            .where({"assignment_id": assignment_id})
            .all(collection=False, ignore_limit=True, conn=conn)
        )

        return assignment

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "assignment_id",
            "transaction_date",
            "type",
            "user_id",
            # "assigned_by",
            "employee_id",
            "department_id",
            "work_area_id",
            "company_id",
            "branch_id",
            "warehouse_id",
            "notes",
            "products",
            "documents",
        ]
    )
    def save_assignment(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        assignment_id = body.get("assignment_id", None)
        # documents = body.get("documents", [])

        conn = ProductAssignment().get_connection()
        assignment = ProductAssignment().where({"assignment_id": assignment_id}).one_or_none(conn=conn)

        if assignment:
            raise cherrypy.HTTPError(409, "Conflict - Duplicate Document")

        try:
            conn.begin(conn)

            body["code"] = "AM{date}{number}".format(
                date=Convert().datetime2str(dt=None, tz=timezone("America/Mazatlan"), format="%d%m%y"),
                number=Serie.generate(reference="general", key="products-assignments", conn=conn),
            )

            assignment = ProductAssignment()
            assignment.set_attrs(body, validate_unknown=False)
            assignment.status = "active"
            assignment.updated_at = datetime.utcnow()
            assignment.created_at = datetime.utcnow()

            assignment.insert(conn=conn)

            for entry in body["products"]:
                item = ProductAssignmentItem()
                item.set_attrs(entry, validate_unknown=False, ignore_restricted=True)
                item.assignment_id = assignment_id
                item.type = assignment.type
                item.updated_at = datetime.utcnow()
                item.created_at = datetime.utcnow()
                item.insert(conn=conn)

                unit = (
                    Stock()
                    .where(
                        {"warehouse_id": assignment.warehouse_id},
                        {"product_id": item.product_id},
                        {"measure_id": item.measure_id},
                    )
                    .one_or_none(conn=conn)
                )

                if unit is None:
                    raise cherrypy.HTTPError(428, "Invalid stock item")

                if assignment.type == "assignment":
                    unit.quantity -= item.quantity
                elif assignment.type == "return":
                    unit.quantity += item.quantity

                unit.updated_at = datetime.utcnow()
                unit.update(conn=conn)

                ep = (
                    EmployeeProduct()
                    .where(
                        {"employee_id": assignment.employee_id},
                        {"product_id": item.product_id},
                        {"measure_id": item.measure_id},
                    )
                    .one_or_none(conn=conn)
                )

                if ep is None:
                    ep = EmployeeProduct()
                    ep.employee_id = assignment.employee_id
                    ep.product_id = item.product_id
                    ep.measure_id = item.measure_id
                    ep.quantity = 0
                    ep.updated_at = datetime.utcnow()
                    ep.created_at = datetime.utcnow()
                    ep.insert(conn=conn)

                if assignment.type == "assignment":
                    ep.quantity += item.quantity
                elif assignment.type == "return":
                    ep.quantity -= item.quantity

                ep.updated_at = datetime.utcnow()
                ep.update(conn=conn)

            # for item in documents:
            #     if item == "":
            #         continue
            #     tag = item.split("/")[-1]
            #     document_id = tag.split(".")[0]

            #     document = ProductUnitAssignmentDocument()
            #     document.assignment_id = assignment_id
            #     document.document_id = document_id
            #     document.path = item
            #     document.created_at = datetime.utcnow()
            #     document.updated_at = datetime.utcnow()
            #     document.insert(conn=conn)

        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))
        finally:
            conn.commit(conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "assignment_id",
            "documents",
        ]
    )
    def update_assignment(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        assignment_id = body.get("assignment_id", None)
        documents = body.get("documents", [])

        conn = ProductAssignment().get_connection()
        assignment = ProductAssignment().where({"assignment_id": assignment_id}).one_or_none(conn=conn)

        if not assignment:
            raise cherrypy.HTTPError(404, "Not Found")

        try:
            conn.begin(conn)

            # remove concepts
            sql = ("""
                    DELETE FROM `{table}`
                    WHERE
                        `assignment_id` = %s
                """).format(table=ProductAssignmentDocument()._TABLE)

            args = [assignment_id]
            conn.execute(sql, *args, connection=None)

            for item in documents:
                if item == "":
                    continue
                tag = item.split("/")[-1]
                document_id = tag.split(".")[0]

                document = ProductAssignmentDocument()
                document.assignment_id = assignment_id
                document.document_id = document_id
                document.path = item
                document.created_at = datetime.utcnow()
                document.updated_at = datetime.utcnow()
                document.insert(conn=conn)

        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))
        finally:
            conn.commit(conn)

        return {}

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @tools.secured()
    # def get_units_services_concepts(self, **kwargs):
    #     result = {}
    #     result["results"] = []
    #     result["total_rows"] = 0

    #     offset = kwargs.get("offset", 0)
    #     limit = kwargs.get("limit", 50)
    #     look_for = kwargs.get("look_for", "")
    #     filters = kwargs.get("filters", "[]")
    #     sort = kwargs.get("sort", ["type", "-code", "name"])

    #     criterias = [_OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"})]

    #     criterias = criterias + Utils().convert_filters(filters, force_status=True)

    #     query = Query(model=UnitServiceConcept())
    #     query.where(*criterias)
    #     query.limit(limit)
    #     query.offset(offset)
    #     query.order_by(sort)

    #     result["results"] = query.all(collection=False)
    #     result["total_rows"] = query.count()

    #     if len(result["results"]) == 0:
    #         cherrypy.response.status = "204 No Content"
    #         return {}

    #     return result

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @tools.secured()
    # def get_unit_service_concept_by_id(self, **kwargs):
    #     # Get body content
    #     service_id = kwargs.get("service_id", None)

    #     concept = UnitServiceConcept().where({"service_id": service_id}).one_or_none()

    #     if concept is None:
    #         raise cherrypy.HTTPError(404, "Not Found")

    #     concept = concept.as_dict()
    #     concept["measures"] = [
    #         {
    #             "measure_id": "0576fb85-8582-43b2-b05b-d6c45ef42d80",
    #             "code": "0010",
    #             "name": "PIEZA",
    #             "external_reference": "0e10f16d-516b-11e8-a542-66d4b3ba2dec",
    #             "weight": 99,
    #             "status": "active",
    #             "created_at": "2022-12-10T02:38:03",
    #             "updated_at": "2022-12-10T02:38:03",
    #             "equivalence": 1,
    #             "default": 0,
    #         },
    #         {
    #             "measure_id": "c8b36f1d-db9c-4389-bd30-38713d1321ea",
    #             "code": "0001",
    #             "name": "SERVICIO",
    #             "external_reference": "0d1f75c0-516b-11e8-a542-66d4b3ba2dec",
    #             "weight": 99,
    #             "status": "active",
    #             "created_at": "2022-12-10T02:38:03",
    #             "updated_at": "2022-12-10T02:38:03",
    #             "equivalence": 1,
    #             "default": 1,
    #         },
    #     ]

    #     return concept

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @cherrypy.tools.json_in()
    # @tools.secured()
    # @tools.validate_body_params(["service_id", "name", "description", "weight", "status"])
    # def save_unit_service_concept(self, **kwargs):
    #     # Get body content
    #     body = cherrypy.request.json
    #     service_id = body.get("service_id", None)

    #     conn = UnitServiceConcept().get_connection()
    #     concept = UnitServiceConcept().where({"service_id": service_id}).one_or_none()

    #     try:
    #         conn.begin(conn)

    #         is_new = False
    #         if concept is None:
    #             is_new = True
    #             body["code"] = Serie.generate(reference="general", key="unit_service_concept", conn=conn)
    #             concept = UnitServiceConcept()
    #             concept.created_at = datetime.utcnow()

    #         concept.set_attrs(body)
    #         concept.updated_at = datetime.utcnow()

    #         if is_new:
    #             concept.insert(conn=conn)
    #         else:
    #             concept.update(conn=conn)
    #         conn.commit(conn)
    #     except pymysql.err.IntegrityError as e:
    #         conn.rollback(conn)
    #         raise cherrypy.HTTPError(409, str(e))
    #     except Exception as e:
    #         # Rollback changes
    #         conn.rollback(conn)
    #         raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

    #     return {}

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @tools.secured()
    # def delete_unit_service_concept(self, **kwargs):
    #     # Get body content
    #     service_id = kwargs.get("service_id", None)

    #     concept = UnitServiceConcept().where({"service_id": service_id}).one_or_none()

    #     if concept is None:
    #         raise cherrypy.HTTPError(404, "Not Found")

    #     concept.status = "inactive"
    #     concept.updated_at = datetime.utcnow()
    #     concept.update()

    #     return {}

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @tools.secured()
    # def get_units_maintenances(self, **kwargs):
    #     result = {}
    #     result["results"] = []
    #     result["total_rows"] = 0

    #     is_cars_related = kwargs.get("is_cars_related", 1)
    #     offset = kwargs.get("offset", 0)
    #     limit = kwargs.get("limit", 50)
    #     look_for = kwargs.get("look_for", "")
    #     filters = kwargs.get("filters", "[]")

    #     criterias = [
    #         _OR({"code": look_for, "op": "like"}, {"notes": look_for, "op": "like"}),
    #         {"is_cars_related": is_cars_related},
    #     ]

    #     criterias = criterias + Utils().convert_filters(filters=filters, ignore=["unit_uid"], force_status=False)

    #     # has "unit_uid"
    #     filter = Utils().get_filter(filters=filters, key="unit_uid")
    #     if filter:
    #         criterias.append(
    #             {
    #                 "unit_id": (
    #                     ProductUnit()
    #                     .fields(["unit_id"])
    #                     .where({"uid": filter["unit_uid"]})
    #                     .sql(remove_offset_limit=True)
    #                 ),
    #                 "op": "in",
    #             }
    #         )

    #     conn = UnitMaintenance().get_connection()
    #     query = Query(model=UnitMaintenance())
    #     query.where(*criterias)
    #     query.limit(limit)
    #     query.offset(offset)
    #     query.order_by(["-code"])

    #     result["results"] = query.all(conn=conn, collection=False)
    #     result["total_rows"] = query.count(conn=conn)

    #     for item in result["results"]:
    #         item["user"] = User().where({"user_id": item["user_id"]}).one_or_none(conn=conn).as_dict()
    #         del item["user"]["password"]

    #         item["employee"] = Employee().where({"employee_id": item["employee_id"]}).one_or_none(conn=conn).as_dict()

    #         item["employee"]["work_area_id"] = item["employee"]["work_area"]
    #         item["employee"]["work_area"] = (
    #             Category().where({"category_id": item["employee"]["work_area"]}).one_or_none(conn=conn).as_dict()
    #         )

    #         item["employee"]["department_id"] = item["employee"]["department"]
    #         item["employee"]["department"] = (
    #             Category().where({"category_id": item["employee"]["department"]}).one_or_none(conn=conn).as_dict()
    #         )

    #         item["supplier"] = Supplier().where({"supplier_id": item["supplier_id"]}).one_or_none(conn=conn).as_dict()

    #         unit = ProductUnit().where({"unit_id": item["unit_id"]}).one_or_none(conn=conn).as_dict()

    #         item["company"] = Company().where({"company_id": unit["company_id"]}).one_or_none(conn=conn).as_dict()

    #         item["product"] = Product().where({"product_id": unit["product_id"]}).one_or_none(conn=conn).as_dict()

    #         item["brand"] = Brand().where({"brand_id": unit["brand_id"]}).one_or_none(conn=conn).as_dict()

    #         item["model"] = (
    #             BrandModel()
    #             .where({"brand_id": unit["brand_id"]}, {"model_id": unit["model_id"]})
    #             .one_or_none(conn=conn)
    #             .as_dict()
    #         )

    #         item["version"] = (
    #             Version()
    #             .where(
    #                 {"brand_id": unit["brand_id"]},
    #                 {"model_id": unit["model_id"]},
    #                 {"version_id": unit["version_id"]},
    #             )
    #             .one_or_none(conn=conn)
    #             .as_dict()
    #         )

    #         item["unit"] = unit

    #         if item["product_id"] in [
    #             # car
    #             "e776a49c-2173-4b21-b69a-fe9a1ff35caa",
    #             "5d7b8a14-23ea-41f4-b7d7-9ddb33b3d964",
    #             "15c6b1ff-6249-4d7b-a5fe-f334da30fecb",
    #         ]:
    #             measurements = (
    #                 ProductUnitCarMeasurement()
    #                 .where({"measurement_id": item["maintenance_id"]})
    #                 .all(collection=False, ignore_limit=True, conn=conn)
    #             )

    #             extra = {}
    #             for entry in measurements:
    #                 extra[entry["reference"]] = entry

    #             item["extra"] = extra

    #         concepts = (
    #             UnitMaintenanceConcept()
    #             .where({"maintenance_id": item["maintenance_id"]})
    #             .all(collection=False, ignore_limit=True, conn=conn)
    #         )

    #         for concept in concepts:
    #             concept.update(
    #                 UnitServiceConcept().where({"service_id": concept["concept_id"]}).one_or_none(conn=conn).as_dict()
    #             )

    #             concept["measure"] = (
    #                 Measure().where({"measure_id": concept["measure_id"]}).one_or_none(conn=conn).as_dict()
    #             )

    #         item["concepts"] = concepts

    #         next_service = (
    #             UnitMaintenanceNextService().where({"maintenance_id": item["maintenance_id"]}).one_or_none(conn=conn)
    #         )

    #         item["next_service"] = next_service.as_dict() if next_service else {}

    #     if len(result["results"]) == 0:
    #         cherrypy.response.status = "204 No Content"
    #         return {}

    #     return result

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @tools.secured()
    # def get_unit_maintenance_by_id(self, **kwargs):
    #     conn = UnitMaintenance().get_connection()
    #     # Get body content
    #     maintenance_id = kwargs.get("maintenance_id", None)
    #     item = UnitMaintenance().where({"maintenance_id": maintenance_id}).one_or_none(conn=conn)

    #     if item is None:
    #         raise cherrypy.HTTPError(404, "Not Found")

    #     user = User().where({"user_id": item.user_id}).one_or_none(conn=conn).as_dict()
    #     del user["password"]

    #     employee = Employee().where({"employee_id": item.employee_id}).one_or_none(conn=conn).as_dict()

    #     supplier = Supplier().where({"supplier_id": item.supplier_id}).one_or_none(conn=conn).as_dict()

    #     # Get Unit
    #     unit = HelperProductUnit.get(product_id=item.product_id, unit_id=item.unit_id, conn=conn)

    #     concepts = (
    #         UnitMaintenanceConcept()
    #         .where({"maintenance_id": item.maintenance_id})
    #         .all(collection=False, ignore_limit=True, conn=conn)
    #     )

    #     for concept in concepts:
    #         concept.update(
    #             UnitServiceConcept().where({"service_id": concept["concept_id"]}).one_or_none(conn=conn).as_dict()
    #         )

    #         concept["measure"] = (
    #             Measure().where({"measure_id": concept["measure_id"]}).one_or_none(conn=conn).as_dict()
    #         )

    #     evidences = (
    #         UnitMaintenanceEvidence()
    #         .where({"maintenance_id": maintenance_id})
    #         .order_by("created_at")
    #         .all(collection=False, ignore_limit=True, conn=conn)
    #     )

    #     measurements = (
    #         ProductUnitCarMeasurement()
    #         .where({"measurement_id": maintenance_id})
    #         .all(collection=False, ignore_limit=True, conn=conn)
    #     )

    #     extra = {}
    #     for entry in measurements:
    #         extra[entry["reference"]] = entry

    #     next_service = UnitMaintenanceNextService().where({"maintenance_id": maintenance_id}).one_or_none(conn=conn)

    #     item = item.as_dict()
    #     item["user"] = user
    #     item["employee"] = employee
    #     item["supplier"] = supplier
    #     item["unit"] = unit
    #     item["concepts"] = concepts
    #     item["evidences"] = evidences
    #     item["next_service"] = next_service.as_dict() if next_service else {}
    #     item["extra"] = extra

    #     return item

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @cherrypy.tools.json_in()
    # @tools.secured()
    # @tools.validate_body_params(
    #     [
    #         "maintenance_id",
    #         "user_id",
    #         "employee_id",
    #         "supplier_id",
    #         "product_id",
    #         "brand_id",
    #         "model_id",
    #         "version_id",
    #         "unit_id",
    #         # 'code',
    #         "appointment_date",
    #         "status",
    #         "subtotal",
    #         "taxes",
    #         "total",
    #         "notes",
    #         "concepts",
    #         "evidences",
    #     ]
    # )
    # def save_unit_maintenance(self, **kwargs):
    #     # Get body content
    #     body = cherrypy.request.json
    #     product_id = body.get("product_id", None)
    #     maintenance_id = body.get("maintenance_id", None)
    #     concepts = body.get("concepts", [])
    #     evidences = body.get("evidences", [])
    #     extra = body.get("extra", {})

    #     conn = UnitMaintenance().get_connection()

    #     previus_status = ""
    #     item = UnitMaintenance().where({"maintenance_id": maintenance_id}).one_or_none(conn=conn)

    #     try:
    #         conn.begin(conn)

    #         is_new = False
    #         if item is None:
    #             is_new = True
    #             body["code"] = Serie.generate(reference="general", key="units-maintenance", zfill=6, conn=conn)

    #             item = UnitMaintenance()
    #             item.status = "todo"
    #             item.created_at = datetime.utcnow()

    #         # Set previus status
    #         previus_status = item.status

    #         item.set_attrs(body, validate_unknown=False)
    #         item.updated_at = datetime.utcnow()

    #         if is_new:
    #             item.insert(conn=conn)
    #         else:
    #             item.update(conn=conn)

    #         # remove concepts
    #         sql = (
    #             """
    #                 DELETE FROM `{table}`
    #                 WHERE
    #                     `maintenance_id` = %s
    #             """
    #         ).format(table=UnitMaintenanceConcept()._TABLE)

    #         args = [maintenance_id]
    #         conn.execute(sql, *args, connection=None)

    #         for entry in concepts:
    #             concept = UnitMaintenanceConcept()
    #             concept.maintenance_id = maintenance_id
    #             concept.concept_id = entry["service_id"]
    #             concept.set_attrs(entry, validate_unknown=False, ignore_restricted=True)
    #             concept.created_at = datetime.utcnow()
    #             concept.updated_at = datetime.utcnow()
    #             concept.insert(conn=conn)

    #         # remove evidences
    #         sql = (
    #             """
    #                 DELETE FROM `{table}`
    #                 WHERE
    #                     `maintenance_id` = %s
    #             """
    #         ).format(table=UnitMaintenanceEvidence()._TABLE)

    #         args = [maintenance_id]
    #         conn.execute(sql, *args, connection=None)

    #         for index, image in enumerate(evidences, start=0):
    #             if image == "":
    #                 continue

    #             tag = image.split("/")[-1]
    #             evidence_id = tag.split(".")[0]

    #             evidence = UnitMaintenanceEvidence()
    #             evidence.maintenance_id = maintenance_id
    #             evidence.evidence_id = evidence_id
    #             evidence.path = image
    #             # evidence.sort = index
    #             evidence.created_at = datetime.utcnow()
    #             evidence.updated_at = datetime.utcnow()
    #             evidence.insert(conn=conn)

    #         if previus_status == "in-progress" and item.type == "preventive":
    #             next_service = UnitMaintenanceNextService()
    #             next_service.set_attrs(body["next_service"], validate_unknown=False)
    #             next_service.maintenance_id = maintenance_id
    #             next_service.product_id = product_id
    #             next_service.unit_id = item.unit_id
    #             next_service.created_at = item.created_at
    #             next_service.updated_at = item.updated_at
    #             next_service.update_or_insert(conn=conn)

    #             config = ProductUnitConfig()
    #             config.set_attrs(body["next_service"], validate_unknown=False)
    #             config.product_id = product_id
    #             config.unit_id = item.unit_id
    #             config.created_at = item.created_at
    #             config.updated_at = item.updated_at
    #             config.update_or_insert(conn=conn)

    #         if product_id in [
    #             # car
    #             "e776a49c-2173-4b21-b69a-fe9a1ff35caa",
    #             "5d7b8a14-23ea-41f4-b7d7-9ddb33b3d964",
    #         ]:
    #             for key, entry in extra.items():
    #                 if (previus_status in ["todo", "in-progress"] and key == "initial") or (
    #                     previus_status == "in-progress" and key == "final"
    #                 ):
    #                     measurement = ProductUnitCarMeasurement()
    #                     measurement.measurement_id = item.maintenance_id
    #                     measurement.product_id = item.product_id
    #                     measurement.unit_id = item.unit_id
    #                     measurement.set_attrs(entry, validate_unknown=False)
    #                     measurement.created_at = item.created_at
    #                     measurement.updated_at = item.updated_at
    #                     measurement.update_or_insert(conn=conn)

    #         conn.commit(conn)
    #     except pymysql.err.IntegrityError as e:
    #         conn.rollback(conn)
    #         raise cherrypy.HTTPError(409, str(e))
    #     except Exception as e:
    #         # Rollback changes
    #         conn.rollback(conn)
    #         raise cherrypy.HTTPError(500, "Problem adding item: {}".format(str(e)))
    #     return {}

    # # @tools.cors
    # # @cherrypy.tools.json_out()
    # # @tools.secured()
    # # def delete_payment_request(self, **kwargs):

    # # 	# Get body content
    # # 	request_id = kwargs.get('request_id', None)

    # # 	conn = RequestForPayment().get_connection()
    # # 	request = (
    # # 		RequestForPayment()
    # # 		.where({'request_id': request_id})
    # # 		.one_or_none(
    # # 			conn = conn
    # # 		)
    # # 	)

    # # 	if request is None:
    # # 		raise cherrypy.HTTPError(
    # # 			404,
    # # 			'Not Found'
    # # 		)

    # # 	if request.is_paid:
    # # 		raise cherrypy.HTTPError(
    # # 			423,
    # # 			'Locked'
    # # 		)

    # # 	request.status = 'inactive'
    # # 	request.updated_at = datetime.utcnow()
    # # 	request.update(
    # # 		conn = conn
    # # 	)

    # # 	return {}

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @tools.secured()
    # def get_product_units_logbook(self, **kwargs):
    #     result = {}
    #     result["results"] = []
    #     result["total_rows"] = 0

    #     offset = kwargs.get("offset", 0)
    #     limit = kwargs.get("limit", 50)
    #     look_for = kwargs.get("look_for", "")
    #     start_date = kwargs.get("start_date", None)
    #     end_date = kwargs.get("end_date", None)
    #     filters = kwargs.get("filters", "[]")

    #     criterias = [
    #         _AND(
    #             {
    #                 "unit_id": (
    #                     ProductUnit()
    #                     .fields(["unit_id"])
    #                     .where({"uid": look_for, "op": "like"})
    #                     .sql(remove_offset_limit=True)
    #                 ),
    #                 "op": "in",
    #             },
    #             {"created_at": start_date, "op": "gte"},
    #             {"created_at": end_date, "op": "lte"},
    #         )
    #     ]

    #     criterias = criterias + Utils().convert_filters(filters, ignore=["uid"], force_status=False)

    #     # has "unit_uid"
    #     filter = Utils().get_filter(filters=filters, key="uid")
    #     if filter:
    #         criterias.append(
    #             {
    #                 "unit_id": (
    #                     ProductUnit().fields(["unit_id"]).where({"uid": filter["uid"]}).sql(remove_offset_limit=True)
    #                 ),
    #                 "op": "in",
    #             }
    #         )

    #     conn = ProductUnitCarMeasurement().get_connection()
    #     query = Query(model=ProductUnitCarMeasurement())
    #     query.where(*criterias)

    #     query.limit(limit)
    #     query.offset(offset)
    #     query.order_by(["-created_at"])

    #     logs = query.all(conn=conn, collection=False)
    #     result["total_rows"] = query.count(conn=conn)

    #     for item in logs:
    #         unit = HelperProductUnit.get(product_id=item["product_id"], unit_id=item["unit_id"], conn=conn)
    #         unit.update(item)
    #         result["results"].append(unit)

    #     if len(result["results"]) == 0:
    #         cherrypy.response.status = "204 No Content"
    #         return {}

    #     return result

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @tools.secured()
    # def get_product_units_notifications(self, **kwargs):
    #     result = {}
    #     result["results"] = []
    #     result["total_rows"] = 0

    #     offset = kwargs.get("offset", 0)
    #     limit = kwargs.get("limit", 50)
    #     look_for = kwargs.get("look_for", "")
    #     start_date = kwargs.get("start_date", None)
    #     end_date = kwargs.get("end_date", None)
    #     filters = kwargs.get("filters", "[]")

    #     criterias = [
    #         _AND(
    #             {
    #                 "unit_id": (
    #                     ProductUnit()
    #                     .fields(["unit_id"])
    #                     .where({"uid": look_for, "op": "like"})
    #                     .sql(remove_offset_limit=True)
    #                 ),
    #                 "op": "in",
    #             },
    #             {"created_at": start_date, "op": "gte"},
    #             {"created_at": end_date, "op": "lte"},
    #         )
    #     ]

    #     criterias = criterias + Utils().convert_filters(
    #         filters,
    #         ignore=["unit_uid", "brand_id", "model_id", "version_id"],
    #         force_status=False,
    #     )

    #     # has "unit_uid"
    #     filter = Utils().get_filter(filters=filters, key="unit_uid")
    #     if filter:
    #         criterias.append(
    #             {
    #                 "unit_id": (
    #                     ProductUnit()
    #                     .fields(["unit_id"])
    #                     .where({"uid": filter["unit_uid"]})
    #                     .sql(remove_offset_limit=True)
    #                 ),
    #                 "op": "in",
    #             }
    #         )

    #     p_criterias = []
    #     # has "brand"
    #     brand = Utils().get_filter(filters=filters, key="brand_id")
    #     if brand:
    #         p_criterias.append({"brand_id": brand["brand_id"]})

    #     model = Utils().get_filter(filters=filters, key="model_id")
    #     if model:
    #         p_criterias.append({"model_id": model["model_id"]})

    #     version = Utils().get_filter(filters=filters, key="version_id")
    #     if version:
    #         p_criterias.append({"version_id": version["version_id"]})

    #     if p_criterias:
    #         criterias.append(
    #             {
    #                 "unit_id": (ProductUnit().fields(["unit_id"]).where(*p_criterias).sql(remove_offset_limit=True)),
    #                 "op": "in",
    #             }
    #         )

    #     conn = CarMaintenanceNotification().get_connection()
    #     query = Query(model=CarMaintenanceNotification())
    #     query.where(*criterias)

    #     query.limit(limit)
    #     query.offset(offset)
    #     query.order_by(["-created_at"])

    #     entries = query.all(conn=conn, collection=False)
    #     result["total_rows"] = query.count(conn=conn)

    #     for item in entries:
    #         unit = HelperProductUnit.get(product_id=item["product_id"], unit_id=item["unit_id"], conn=conn)

    #         if item["type"] == "mileage":
    #             log = (
    #                 ProductUnitCarMeasurement()
    #                 .where(
    #                     {"product_id": item["product_id"]},
    #                     {"unit_id": item["unit_id"]},
    #                     {"source": "logbook"},
    #                 )
    #                 .order_by(["-mileage"])
    #                 .one_or_none(conn=conn)
    #             )

    #             if log:
    #                 item["current_value"] = log.mileage

    #         if item["type"] == "days":
    #             item["current_value"] = Convert().datetime2str(dt=None, tz=None, format="%Y%m%d")

    #         if item["type"] == "hours":
    #             log = (
    #                 ProductUnitCarMeasurement()
    #                 .where(
    #                     {"product_id": item["product_id"]},
    #                     {"unit_id": item["unit_id"]},
    #                     {"source": "logbook"},
    #                 )
    #                 .order_by(["-hours"])
    #                 .one_or_none(conn=conn)
    #             )

    #             if log:
    #                 item["current_value"] = log.hours

    #         unit.update(item)
    #         result["results"].append(unit)

    #     if len(result["results"]) == 0:
    #         cherrypy.response.status = "204 No Content"
    #         return {}

    #     return result
