from models.state import State
from models.municipality import Municipality
from models.locality import Locality
from models.company import Company
from models.branch_office import BranchOffice


class HelperRelation(object):

    def __init__(self):
        pass

    @classmethod
    def get_company(cls, company_id: str):
        conn = Company().get_connection()
        company = Company().where({"company_id": company_id}).one_or_none(conn=conn).as_dict()

        company["state"] = State().where({"state_id": company["state_id"]}).one_or_none(conn=conn).as_dict()

        company["municipality"] = (
            Municipality()
            .where({"state_id": company["state_id"]}, {"municipality_id": company["municipality_id"]})
            .one_or_none(conn=conn)
            .as_dict()
        )

        company["locality"] = (
            Locality()
            .where(
                {"state_id": company["state_id"]},
                {"municipality_id": company["municipality_id"]},
                {"locality_id": company["locality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        return company

    @classmethod
    def get_branch(cls, branch_id: str):
        conn = BranchOffice().get_connection()
        branch = BranchOffice().where({"branch_id": branch_id}).one_or_none(conn=conn).as_dict()

        branch["state"] = State().where({"state_id": branch["state_id"]}).one_or_none(conn=conn).as_dict()

        branch["municipality"] = (
            Municipality()
            .where({"state_id": branch["state_id"]}, {"municipality_id": branch["municipality_id"]})
            .one_or_none(conn=conn)
            .as_dict()
        )

        branch["locality"] = (
            Locality()
            .where(
                {"state_id": branch["state_id"]},
                {"municipality_id": branch["municipality_id"]},
                {"locality_id": branch["locality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        return branch
