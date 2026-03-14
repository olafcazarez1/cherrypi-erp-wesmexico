import cherrypy
import pymysql

from datetime import datetime
from utils.decorators import tools
from utils.query import _OR, Query
from utils.utils import Utils

from models.state import State
from models.locality import Locality
from models.municipality import Municipality

from models.serie import Serie
from models.company import Company
from models.bank_account import BankAccount
from models.warehouse import Warehouse
from models.branch_office import BranchOffice
from models.branch_office_warehouse import BranchOfficeWarehouse

from views.branch_warehouse import vBranchWarehouse


class MapCompanies(object):
    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_companies",
            "/catalog/companies",
            controller=self,
            action="get_companies",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_company_by_id",
            "/catalog/company/{company_id}",
            controller=self,
            action="get_company_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_company",
            "/catalog/company/{company_id}",
            controller=self,
            action="save_company",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_company",
            "/catalog/company/{company_id}",
            controller=self,
            action="delete_company",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_branch_offices",
            "/catalog/company/{company_id}/branch-offices",
            controller=self,
            action="get_branch_offices",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_branch_offices",
            "/catalog/company/{company_id}/branch-offices",
            controller=self,
            action="get_branch_offices",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_branch_offices",
            "/catalog/branch-offices",
            controller=self,
            action="get_branch_offices",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_branch_office_by_id",
            "/catalog/branch-office/{branch_id}",
            controller=self,
            action="get_branch_office_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_branch_office",
            "/catalog/branch-office/{branch_id}",
            controller=self,
            action="save_branch_office",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_branch_office",
            "/catalog/branch-office/{branch_id}",
            controller=self,
            action="delete_branch_office",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_branch_warehouses",
            "/catalog/branch-office/{branch_id}/warehouses",
            controller=self,
            action="get_branch_warehouses",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_companies(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [
            _OR(
                {"code": look_for, "op": "like"},
                {"legal_name": look_for, "op": "like"},
                {"trade_name": look_for, "op": "like"},
            )
        ]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = Company().get_connection()
        query = Query(model=Company())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code", "legal_name"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_company_by_id(self, **kwargs):
        # Get body content
        company_id = kwargs.get("company_id", None)

        conn = Company().get_connection()
        company = Company().where({"company_id": company_id}).one_or_none(conn=conn)

        if company is None:
            raise cherrypy.HTTPError(404, "Not Found")

        state = State().where({"state_id": company.state_id}).one_or_none(conn=conn)

        municipality = (
            Municipality()
            .where(
                {"state_id": company.state_id},
                {"municipality_id": company.municipality_id},
            )
            .one_or_none(conn=conn)
        )

        locality = (
            Locality()
            .where(
                {"state_id": company.state_id},
                {"municipality_id": company.municipality_id},
                {"locality_id": company.locality_id},
            )
            .one_or_none(conn=conn)
        )

        account = (
            BankAccount()
            .where(
                {"associated_with": "company"},
                {"associated_id": company_id},
                {"is_default": 1},
            )
            .one_or_none(conn=conn)
        )

        company = company.as_dict()
        company["bank_account"] = account.as_dict() if account else None
        company["state"] = state.as_dict()
        company["municipality"] = municipality.as_dict()
        company["locality"] = locality.as_dict()

        return company

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "tax_regime_id",
            "legal_name",
            "trade_name",
            "serie",
            "address_street",
            "address_external_number",
            "-address_internal_number",
            "neighborhood",
            "state_id",
            "municipality_id",
            "locality_id",
            "zip",
            "taxpayer_id",
            "phone",
            "timezone",
            "logo",
            "status",
        ]
    )
    def save_company(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        company_id = body.get("company_id", None)

        conn = Company().get_connection()
        company = Company().where({"company_id": company_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            is_new = False
            if company is None:
                is_new = True
                body["code"] = Serie.generate(reference="general", key="companies", conn=conn)
                company = Company()
                company.created_at = datetime.utcnow()

            company.set_attrs(body)
            company.updated_at = datetime.utcnow()
            company.insert(conn=conn) if is_new else company.update(conn=conn)
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
    def delete_company(self, **kwargs):
        # Get body content
        company_id = kwargs.get("company_id", None)

        conn = Company().get_connection()
        company = Company().where({"company_id": company_id}).one_or_none(conn=conn)

        if company is None:
            raise cherrypy.HTTPError(404, "Not Found")

        company.status = "inactive"
        company.updated_at = datetime.utcnow()
        company.update(conn=conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_branch_offices(self, **kwargs):
        company_id = kwargs.get("company_id", None)

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [_OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"})]

        if company_id:
            criterias.append({"company_id": company_id})

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = BranchOffice().get_connection()
        query = Query(model=BranchOffice())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code", "name"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for branch in result["results"]:
            branch["company"] = Company().where({"company_id": branch["company_id"]}).one_or_none(conn=conn).as_dict()

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_branch_office_by_id(self, **kwargs):
        conn = BranchOffice().get_connection()
        # Get body content
        branch_id = kwargs.get("branch_id", None)
        branch = BranchOffice().where({"branch_id": branch_id}).one_or_none(conn=conn)

        if branch is None:
            raise cherrypy.HTTPError(404, "Not Found")

        company = Company().where({"company_id": branch.company_id}).one_or_none(conn=conn)

        state = State().where({"state_id": branch.state_id}).one_or_none(conn=conn)

        municipality = (
            Municipality()
            .where(
                {"state_id": branch.state_id},
                {"municipality_id": branch.municipality_id},
            )
            .one_or_none(conn=conn)
        )

        locality = (
            Locality()
            .where(
                {"state_id": branch.state_id},
                {"municipality_id": branch.municipality_id},
                {"locality_id": branch.locality_id},
            )
            .one_or_none(conn=conn)
        )

        result = BranchOfficeWarehouse().where({"branch_id": branch_id}, {"status": "active"}).all(conn=conn)

        warehouses = []
        for item in result.all():
            warehouse = Warehouse().where({"warehouse_id": item.warehouse_id}).one_or_none(conn=conn)
            m_data = warehouse.as_dict()
            m_data.update(item.as_dict())
            warehouses.append(m_data)

        branch = branch.as_dict()
        branch["warehouses"] = sorted(warehouses, key=lambda i: i["name"], reverse=True)

        branch["company"] = company.as_dict()
        branch["state"] = state.as_dict()
        branch["municipality"] = municipality.as_dict()
        branch["locality"] = locality.as_dict()
        return branch

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "type",
            "name",
            # 'serie',
            "address_street",
            "address_external_number",
            "-address_internal_number",
            "neighborhood",
            "state_id",
            "municipality_id",
            "locality_id",
            "zip",
            "phone",
            "timezone",
            "status",
            "warehouses",
        ]
    )
    def save_branch_office(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        company_id = body.get("company_id", None)
        branch_id = body.get("branch_id", None)
        warehouses = body.get("warehouses", [])

        conn = BranchOffice().get_connection()
        try:
            conn.begin(conn)

            branch = BranchOffice().where({"branch_id": branch_id}).one_or_none(conn=conn)

            is_new = False if branch else True
            if branch is None:
                body["code"] = Serie.generate(reference="branch_offices", key=company_id)
                branch = BranchOffice()
                branch.status = "active"
                branch.created_at = datetime.utcnow()

            branch.set_attrs(body, validate_unknown=False)
            branch.updated_at = datetime.utcnow()

            if is_new:
                branch.insert(conn=conn)
            else:
                branch.update(conn=conn)

            # disable current warehouses
            result = BranchOfficeWarehouse().where({"branch_id": branch_id}, {"status": "active"}).all(conn=conn)

            for item in result.all():
                item.status = "inactive"
                item.updated_at = datetime.utcnow()
                item.update(conn=conn)

            for item in warehouses:
                warehouse = BranchOfficeWarehouse()
                warehouse.branch_id = branch_id
                warehouse.set_attrs(item, validate_unknown=False, ignore_restricted=True)
                warehouse.status = "active"
                warehouse.created_at = datetime.utcnow()
                warehouse.updated_at = datetime.utcnow()
                warehouse.update_or_insert(conn=conn)

        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem adding item: {}".format(str(e)))
        finally:
            conn.commit(conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_branch_office(self, **kwargs):
        # Get body content
        branch_id = kwargs.get("branch_id", None)

        conn = BranchOffice().get_connection()
        branch = BranchOffice().where({"branch_id": branch_id}).one_or_none(conn=conn)

        if branch is None:
            raise cherrypy.HTTPError(404, "Not Found")

        branch.status = "inactive"
        branch.updated_at = datetime.utcnow()
        branch.update(conn=conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_branch_warehouses(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        branch_id = kwargs.get("branch_id", "")
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")
        sort = kwargs.get("sort", ["weight", "name"])

        conn = BranchOffice().get_connection()
        branch = BranchOffice().where({"branch_id": branch_id}).one_or_none(conn=conn)

        if branch is None:
            raise cherrypy.HTTPError(404, "Branch Not Found")

        criterias = [{"branch_id": branch_id}]
        if look_for:
            criterias.append(
                _OR(
                    {"code": look_for, "op": "like"},
                    {"name": look_for, "op": "like"},
                )
            )

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        query = Query(model=vBranchWarehouse())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(sort)

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result
