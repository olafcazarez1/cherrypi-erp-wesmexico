from utils.query import _OR

from models.company import Company
from models.employee import Employee
from models.client import Client

# from models.supplier import Supplier
# from models.contractor import Contractor
# from models.project import Project


class HelperAccountRelation(object):

    def __init__(self):
        pass

    @classmethod
    def get(cls, type: str, id: str, as_dict: bool = False, conn: any = None):

        relation = None

        # if type == "project":
        #     relation = Project().where({"project_id": id}).one_or_none(conn=conn)

        if type == "company":
            relation = Company().where({"company_id": id}).one_or_none(conn=conn)

        if type == "client":
            relation = Client().where({"client_id": id}).one_or_none(conn=conn)

        # if type == "contractor":
        #     relation = Contractor().where({"contractor_id": id}).one_or_none(conn=conn)

        # if type in ["admin", "supplier"]:
        #     relation = Supplier().where({"supplier_id": id}).one_or_none(conn=conn)

        if type == "employee":
            relation = Employee().where({"employee_id": id}).one_or_none(conn=conn)

        if relation and as_dict is True:
            relation = relation.as_dict()

        return relation

    @classmethod
    def get_subquery_sql(cls, type: str, look_for: str):

        relation = None

        # if type == "project":
        #     relation = (
        #         Project()
        #         .fields(["project_id"])
        #         .where(_OR({"trade_name": look_for, "op": "like"}, {"legal_name": look_for, "op": "like"}))
        #         .sql(remove_offset_limit=True)
        #     )

        if type == "company":
            relation = (
                Company()
                .fields(["company_id"])
                .where(_OR({"trade_name": look_for, "op": "like"}, {"legal_name": look_for, "op": "like"}))
                .sql(remove_offset_limit=True)
            )

        if type == "client":
            relation = (
                Client()
                .fields(["client_id"])
                .where(_OR({"trade_name": look_for, "op": "like"}, {"legal_name": look_for, "op": "like"}))
                .sql(remove_offset_limit=True)
            )

        # if type == "contractor":
        #     relation = (
        #         Contractor()
        #         .fields(["contractor_id"])
        #         .where(_OR({"trade_name": look_for, "op": "like"}, {"legal_name": look_for, "op": "like"}))
        #         .sql(remove_offset_limit=True)
        #     )

        # if type == "supplier":
        #     relation = (
        #         Supplier()
        #         .fields(["supplier_id"])
        #         .where(_OR({"trade_name": look_for, "op": "like"}, {"legal_name": look_for, "op": "like"}))
        #         .sql(remove_offset_limit=True)
        #     )

        if type == "employee":
            relation = (
                Employee()
                .fields(["employee_id"])
                .where({"full_name": look_for, "op": "like"})
                .sql(remove_offset_limit=True)
            )

        return relation
