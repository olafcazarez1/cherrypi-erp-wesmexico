import cherrypy

from models.category import Category
from models.company import Company
from models.employee import Employee
from models.employee_product_unit import EmployeeProductUnit
from models.brand import Brand
from models.brand_model import BrandModel
from models.version import Version
from models.product import Product
from models.product_unit import ProductUnit
from models.product_unit_spec import ProductUnitSpec
from models.product_unit_config import ProductUnitConfig
from models.product_unit_invoice import ProductUnitInvoice

from models.product_unit_car import ProductUnitCar
from models.product_unit_car_insurance import ProductUnitCarInsurance
from models.product_unit_car_circulation_card import ProductUnitCarCirculationCard
from models.product_unit_car_measurement import ProductUnitCarMeasurement

from utils.query import _OR, _AND


class HelperProductUnit(object):
    def __init__(self):
        pass

    @classmethod
    def get(cls, product_id: str, unit_id: str, conn: any = None):
        unit = (
            ProductUnit()
            .where(
                _OR(
                    _AND({"product_id": product_id}, {"unit_id": unit_id}),
                    {"uid": unit_id},
                )
            )
            .one_or_none(conn=conn)
        )

        if unit is None:
            raise cherrypy.HTTPError(404, "Not Found")

        unit = unit.as_dict()

        unit["company"] = Company().where({"company_id": unit["company_id"]}).one_or_none(conn=conn).as_dict()

        unit["department"] = Category().where({"category_id": unit["department_id"]}).one_or_none(conn=conn).as_dict()

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

        unit["specs"] = (
            ProductUnitSpec()
            .where({"product_id": unit["product_id"]}, {"unit_id": unit["unit_id"]})
            .order_by(["+index"])
            .all(collection=False, conn=conn)
        )
        # Fix ids
        product_id = unit["product_id"]
        unit_id = unit["unit_id"]

        invoice = ProductUnitInvoice().where({"unit_id": unit_id}).one_or_none(conn=conn)
        unit["invoice"] = invoice.as_dict() if invoice else {}

        config = ProductUnitConfig().where({"unit_id": unit_id}).one_or_none(conn=conn)
        unit["config"] = config.as_dict() if config else {}

        if product_id in [
            # car
            "e776a49c-2173-4b21-b69a-fe9a1ff35caa",
            "5d7b8a14-23ea-41f4-b7d7-9ddb33b3d964",
            "15c6b1ff-6249-4d7b-a5fe-f334da30fecb",
        ]:
            car = ProductUnitCar().where({"unit_id": unit_id}).one_or_none(conn=conn)

            unit.update(car.as_dict() if car else {})

            insurance = ProductUnitCarInsurance().where({"unit_id": unit_id}).one_or_none(conn=conn)

            circulation_card = ProductUnitCarCirculationCard().where({"unit_id": unit_id}).one_or_none(conn=conn)

            unit["insurance"] = insurance.as_dict() if insurance else {}
            unit["circulation_card"] = circulation_card.as_dict() if circulation_card else {}

            unit["logbook"] = (
                ProductUnitCarMeasurement()
                .where({"unit_id": unit_id})
                .order_by(["-created_at"])
                .limit(10)
                .all(conn=conn, collection=False)
            )

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
                .one_or_none(conn=conn)
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

        return unit
