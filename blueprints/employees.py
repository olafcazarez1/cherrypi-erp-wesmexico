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
from models.company import Company
from models.branch_office import BranchOffice
from models.measure import Measure
from models.product import Product
from models.employee import Employee
from models.employee_driver_license import EmployeeDriverLicense
from models.employee_medical_insurance import EmployeeMedicalInsurance
from models.employee_infonavit_credit import EmployeeInfonavitCredit
from models.employee_fonacot_credit import EmployeeFonacotCredit
from models.employee_relative import EmployeeRelative

from models.employee_product import EmployeeProduct
from models.employee_product_unit import EmployeeProductUnit

from helpers.helper_product_unit import HelperProductUnit


class MapEmployees(object):
    def __init__(self):
        pass

    def init(self, mapper=None):
        mapper.connect(
            "get_employees",
            "/catalog/employees",
            controller=self,
            action="get_employees",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_employee_by_id",
            "/catalog/employee/{employee_id}",
            controller=self,
            action="get_employee_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_employee_calendar",
            "/catalog/employee/{employee_id}/calendar",
            controller=self,
            action="get_employee_calendar",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_employee",
            "/catalog/employee/{employee_id}",
            controller=self,
            action="save_employee",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_employee",
            "/catalog/employee/{employee_id}",
            controller=self,
            action="delete_employee",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_employees(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")
        sort = kwargs.get("sort", ["code", "names", "first_last_name", "second_last_name"])

        criterias = [
            _OR(
                {"code": look_for, "op": "like"},
                {"full_name": look_for, "op": "like"},
                {"email": look_for, "op": "like"},
            )
        ]

        criterias = criterias + Utils().convert_filters(filters, ignore=["is_free"], force_status=True)

        # is_free = Utils().get_filter(filters, "is_free")
        # if is_free:
        #     criterias.append(
        #         {
        #             "employee_id": (
        #                 RequestForServiceTaskVisitStaff()
        #                 .fields(["employee_id"])
        #                 .where(
        #                     {
        #                         "visit_id": (
        #                             RequestForServiceTaskVisit()
        #                             .fields(["visit_id"])
        #                             .where(
        #                                 _OR(
        #                                     _AND(
        #                                         {
        #                                             "initial_execution_date": is_free["is_free"]["start_date"],
        #                                             "op": "lt",
        #                                         },
        #                                         {
        #                                             "final_execution_date": is_free["is_free"]["start_date"],
        #                                             "op": "gt",
        #                                         },
        #                                     ),
        #                                     _AND(
        #                                         {
        #                                             "initial_execution_date": is_free["is_free"]["end_date"],
        #                                             "op": "lt",
        #                                         },
        #                                         {
        #                                             "final_execution_date": is_free["is_free"]["end_date"],
        #                                             "op": "gt",
        #                                         },
        #                                     ),
        #                                     _AND(
        #                                         {
        #                                             "initial_execution_date": is_free["is_free"]["start_date"],
        #                                             "op": "gte",
        #                                         },
        #                                         {
        #                                             "final_execution_date": is_free["is_free"]["end_date"],
        #                                             "op": "lte",
        #                                         },
        #                                     ),
        #                                 ),
        #                                 {
        #                                     "status": ["done", "cancelled"],
        #                                     "op": "not in",
        #                                 },
        #                             )
        #                             .sql(remove_offset_limit=True)
        #                         ),
        #                         "op": "in",
        #                     },
        #                     {"status": "active"},
        #                 )
        #                 .sql(remove_offset_limit=True)
        #             ),
        #             "op": "not in",
        #         }
        #     )

        conn = Employee().get_connection()
        query = Query(model=Employee())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(sort)

        result["results"] = query.all(conn=conn, collection=False)

        # add positon
        for employee in result["results"]:
            employee["position"] = (
                Category().where({"category_id": employee["work_position_id"]}).one_or_none(conn=conn).as_dict()
            )

        result["total_rows"] = query.count(conn=conn)

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_employee_by_id(self, **kwargs):
        # Get body content
        employee_id = kwargs.get("employee_id", None)
        include_assigments = kwargs.get("include_assigments", False)

        conn = Employee().get_connection()
        employee = Employee().where({"employee_id": employee_id}).one_or_none(conn=conn)

        if employee is None:
            raise cherrypy.HTTPError(404, "Not Found")

        company = Company().where({"company_id": employee.company_id}).one_or_none(conn=conn)

        branch = (
            BranchOffice()
            .where({"company_id": employee.company_id}, {"branch_id": employee.branch_id})
            .one_or_none(conn=conn)
        )

        department = Category().where({"category_id": employee.department_id}).one_or_none(conn=conn)

        work_area = Category().where({"category_id": employee.work_area_id}).one_or_none(conn=conn)

        work_position = Category().where({"category_id": employee.work_position_id}).one_or_none(conn=conn)

        license = EmployeeDriverLicense().where({"employee_id": employee_id}).one_or_none(conn=conn)
        medical_insurance = EmployeeMedicalInsurance().where({"employee_id": employee_id}).one_or_none(conn=conn)
        infonavit_credit = EmployeeInfonavitCredit().where({"employee_id": employee_id}).one_or_none(conn=conn)
        fonacot_credit = EmployeeFonacotCredit().where({"employee_id": employee_id}).one_or_none(conn=conn)

        state = State().where({"state_id": employee.state_id}).one_or_none(conn=conn)

        state = State().where({"state_id": employee.state_id}).one_or_none(conn=conn)

        municipality = (
            Municipality()
            .where(
                {"state_id": employee.state_id},
                {"municipality_id": employee.municipality_id},
            )
            .one_or_none(conn=conn)
        )

        locality = (
            Locality()
            .where(
                {"state_id": employee.state_id},
                {"municipality_id": employee.municipality_id},
                {"locality_id": employee.locality_id},
            )
            .one_or_none(conn=conn)
        )

        if include_assigments:
            assignments = (
                EmployeeProductUnit()
                .where({"employee_id": employee_id})
                .order_by(["-created_at"])
                .all(collection=False, conn=conn)
            )

            for assignment in assignments:
                assignment.update(
                    HelperProductUnit.get(
                        product_id=assignment["product_id"],
                        unit_id=assignment["unit_id"],
                        conn=conn,
                    )
                )

        relatives = (
            EmployeeRelative()
            .where({"employee_id": employee_id})
            .all(
                conn=conn,
                collection=False,
                ignore_limit=True,
            )
        )

        documents = (
            ImageDocument()
            .where({"transaction_id": employee_id}, {"origin": "employee-document"})
            .order_by(["index"])
            .all(collection=False, ignore_limit=True, conn=conn)
        )

        equipment = (
            EmployeeProductUnit()
            .where({"employee_id": employee_id}, {"status": "assigned"})
            .all(collection=False, conn=conn)
        )

        for unit in equipment:
            unit.update(HelperProductUnit.get(product_id=unit["product_id"], unit_id=unit["unit_id"], conn=conn))

        items = (
            EmployeeProduct()
            .where({"employee_id": employee_id}, {"quantity": 0, "op": "gt"})
            .all(conn=conn, collection=False)
        )

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

        employee = employee.as_dict()
        employee["company"] = company.as_dict()
        employee["branch"] = branch.as_dict()
        employee["department"] = department.as_dict()
        employee["work_area"] = work_area.as_dict()
        employee["work_position"] = work_position.as_dict()
        employee["license"] = license.as_dict() if license else {}
        employee["medical_insurance"] = medical_insurance.as_dict() if medical_insurance else {}
        employee["infonavit_credit"] = infonavit_credit.as_dict() if infonavit_credit else {}
        employee["fonacot_credit"] = fonacot_credit.as_dict() if fonacot_credit else {}
        employee["state"] = state.as_dict()
        employee["municipality"] = municipality.as_dict()
        employee["locality"] = locality.as_dict()

        employee["relatives"] = sorted(relatives, key=lambda i: i["full_name"])
        employee["equipment"] = equipment
        employee["products"] = sorted(products, key=lambda i: i["name"])
        employee["documents"] = documents

        if include_assigments:
            employee["assignments"] = assignments

        return employee

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @tools.secured()
    # def get_employee_calendar(self, **kwargs):
    #     # Get body content
    #     employee_id = kwargs.get("employee_id", None)
    #     start_date = kwargs.get("start_date", None)
    #     end_date = kwargs.get("end_date", None)

    #     conn = Employee().get_connection()

    #     visits = (
    #         RequestForServiceTaskVisitStaff()
    #         .where(
    #             {"employee_id": employee_id},
    #             {
    #                 "visit_id": (
    #                     RequestForServiceTaskVisit()
    #                     .fields(["visit_id"])
    #                     .where(
    #                         {"initial_execution_date": start_date, "op": "gt"},
    #                         {"final_execution_date": end_date, "op": "lt"},
    #                     )
    #                     .sql(remove_offset_limit=True)
    #                 ),
    #                 "op": "in",
    #             },
    #             {"status": "active"},
    #         )
    #         .all(ignore_limit=True, conn=conn)
    #     )

    #     events = []
    #     for visit in visits.all():
    #         task = RequestForServiceTaskVisit().where({"visit_id": visit.visit_id}).one_or_none(conn=conn)

    #         service = Product().where({"product_id": visit.service_id}).one_or_none(conn=conn)

    #         request = (RequestForService().where({"request_id": visit.request_id}).one_or_none(conn=conn)).as_dict()

    #         request["client"] = (Client().where({"client_id": request["client_id"]}).one_or_none(conn=conn)).as_dict()

    #         events.append(
    #             {
    #                 "task_id": visit.task_id,
    #                 "visit_id": visit.visit_id,
    #                 "start_date": task.initial_execution_date,
    #                 "end_date": task.final_execution_date,
    #                 "hours": task.hours,
    #                 "name": service.name,
    #                 "request": request,
    #                 "status": task.status,
    #             }
    #         )

    #     events = sorted(events, key=lambda i: i["start_date"])

    #     return events

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "company_id",
            "branch_id",
            # "code",
            "names",
            "first_last_name",
            "second_last_name",
            "birthday",
            "gender",
            "blood_type",
            "taxpayer_id",
            "federal_id",
            # "ssn",  # Social Security Number
            "department_id",
            "work_area_id",
            "work_position_id",
            "email",
            "phone",
            "cell_phone",
            "address_street",
            "address_external_number",
            "address_internal_number",
            "neighborhood",
            "state_id",
            "municipality_id",
            "locality_id",
            "zip",
            "license",
            "medical_insurance",
            "infonavit_credit",
            "fonacot_credit",
            "relatives",
            "status",
        ]
    )
    def save_employee(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        employee_id = body.get("employee_id", None)

        conn = Employee().get_connection()
        employee = Employee().where({"employee_id": employee_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            is_new = False
            if employee is None:
                is_new = True
                body["code"] = Serie.generate(reference="general", key="employees", conn=conn)
                employee = Employee()
                employee.created_at = datetime.utcnow()

            employee.set_attrs(body, validate_unknown=False)
            employee.updated_at = datetime.utcnow()
            if is_new:
                employee.insert(conn=conn)
            else:
                employee.update(conn=conn)

            if employee.has_license:
                license = EmployeeDriverLicense()
                license.created_at = datetime.utcnow()
                license.set_attrs(body["license"], validate_unknown=False)
                license.updated_at = datetime.utcnow()
                license.update_or_insert(conn=conn)

            else:
                # Disable current license
                license = EmployeeDriverLicense().where({"employee_id": employee_id}).one_or_none(conn=conn)

                if license:
                    license.status = "inactive"
                    license.updated_at = datetime.utcnow()
                    license.update(conn=conn)

            if employee.has_medical_insurance:
                medical = EmployeeMedicalInsurance()
                medical.created_at = datetime.utcnow()
                medical.set_attrs(body["medical_insurance"], validate_unknown=False)
                medical.updated_at = datetime.utcnow()
                medical.update_or_insert(conn=conn)

            else:
                # Disable current medical
                medical = EmployeeMedicalInsurance().where({"employee_id": employee_id}).one_or_none(conn=conn)

                if medical:
                    medical.status = "inactive"
                    medical.updated_at = datetime.utcnow()
                    medical.update(conn=conn)

            if employee.has_infonavit_credit:
                credit = EmployeeInfonavitCredit()
                credit.created_at = datetime.utcnow()
                credit.set_attrs(body["infonavit_credit"], validate_unknown=False)
                credit.updated_at = datetime.utcnow()
                credit.update_or_insert(conn=conn)

            else:
                # Disable current credit
                credit = EmployeeInfonavitCredit().where({"employee_id": employee_id}).one_or_none(conn=conn)

                if credit:
                    credit.status = "inactive"
                    credit.updated_at = datetime.utcnow()
                    credit.update(conn=conn)

            if employee.has_fonacot_credit:
                credit = EmployeeFonacotCredit()
                credit.created_at = datetime.utcnow()
                credit.set_attrs(body["fonacot_credit"], validate_unknown=False)
                credit.updated_at = datetime.utcnow()
                credit.update_or_insert(conn=conn)

            else:
                # Disable current credit
                credit = EmployeeFonacotCredit().where({"employee_id": employee_id}).one_or_none(conn=conn)

                if credit:
                    credit.status = "inactive"
                    credit.updated_at = datetime.utcnow()
                    credit.update(conn=conn)

            sql = (
                """
                    DELETE FROM `{table}`
                    WHERE
                        `employee_id` = %s
                """
            ).format(table=EmployeeRelative()._TABLE)

            args = [employee_id]
            conn.execute(sql, *args, connection=None)

            for item in body["relatives"]:
                relative = EmployeeRelative()
                relative.employee_id = employee_id
                relative.set_attrs(item, validate_unknown=False, ignore_restricted=True)
                relative.status = "active"
                relative.created_at = datetime.utcnow()
                relative.updated_at = datetime.utcnow()
                relative.update_or_insert(conn=conn)

            sql = (
                """
                    DELETE FROM `{table}`
                    WHERE
                        `transaction_id` = %s
                """
            ).format(table=ImageDocument()._TABLE)

            args = [employee_id]
            conn.execute(sql, *args, connection=None)

            for index, item in enumerate(body["documents"]):
                document = ImageDocument()
                document.transaction_id = employee_id
                document.document_id = f"{employee_id}-{index}"
                document.index = index
                document.origin = "employee-document"
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
    def delete_employee(self, **kwargs):
        # Get body content
        employee_id = kwargs.get("employee_id", None)

        conn = Employee().get_connection()
        employee = Employee().where({"employee_id": employee_id}).one_or_none(conn=conn)

        if employee is None:
            raise cherrypy.HTTPError(404, "Not Found")

        employee.status = "inactive"
        employee.updated_at = datetime.utcnow()
        employee.update(conn=conn)

        return {}
