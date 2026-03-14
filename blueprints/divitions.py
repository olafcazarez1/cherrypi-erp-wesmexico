import cherrypy
import pymysql

from datetime import datetime
from utils.decorators import tools
from utils.query import _OR, Query
from utils.utils import Utils

from models.serie import Serie
from models.division import Division
from models.subdivision import SubDivision


class MapDivisions(object):
    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_divisions",
            "/catalog/divisions",
            controller=self,
            action="get_divisions",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_division_by_id",
            "/catalog/division/{division_id}",
            controller=self,
            action="get_division_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_division",
            "/catalog/division/{division_id}",
            controller=self,
            action="save_division",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_division",
            "/catalog/division/{division_id}",
            controller=self,
            action="delete_division",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_subdivisions",
            "/catalog/division/{division_id}/subdivisions",
            controller=self,
            action="get_subdivisions",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_subdivision_by_id",
            "/catalog/division/{division_id}/subdivision/{subdivision_id}",
            controller=self,
            action="get_subdivision_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_subdivision",
            "/catalog/division/{division_id}/subdivision/{subdivision_id}",
            controller=self,
            action="save_subdivision",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_subdivision",
            "/catalog/division/{division_id}/subdivision/{subdivision_id}",
            controller=self,
            action="delete_subdivision",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_divisions(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")
        sort = kwargs.get("sort", ["-weight"])

        criterias = [_OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"})]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        query = Query(model=Division())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(sort)

        result["results"] = query.all(collection=False)
        result["total_rows"] = query.count()

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_division_by_id(self, **kwargs):
        # Get body content
        division_id = kwargs.get("division_id", None)

        division = Division().where({"division_id": division_id}).one_or_none()

        if division is None:
            raise cherrypy.HTTPError(404, "Not Found")

        return division.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["division_id", "name", "weight", "value", "is_global", "status"])
    def save_division(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        division_id = body.get("division_id", None)

        conn = Division().get_connection()
        division = Division().where({"division_id": division_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            is_new = False
            if division is None:
                is_new = True
                body["code"] = Serie.generate(reference="general", key="divisions", conn=conn)
                division = Division()
                division.created_at = datetime.utcnow()

            division.set_attrs(body)
            division.updated_at = datetime.utcnow()
            division.insert(conn=conn) if is_new else division.update(conn=conn)

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
    def delete_division(self, **kwargs):
        # Get body content
        division_id = kwargs.get("division_id", None)

        division = Division().where({"division_id": division_id}).one_or_none()

        if division is None:
            raise cherrypy.HTTPError(404, "Not Found")

        division.status = "inactive"
        division.updated_at = datetime.utcnow()
        division.update()

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_subdivisions(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        division_id = kwargs.get("division_id", None)
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")
        sort = kwargs.get("sort", ["-weight"])

        criterias = [
            {"division_id": division_id},
            _OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"}),
        ]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = SubDivision().get_connection()
        query = Query(model=SubDivision())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(sort)

        result["results"] = query.all(collection=False, conn=conn)
        result["total_rows"] = query.count(conn=conn)

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        for subdivision in result["results"]:
            subdivision["division"] = (
                Division().where({"division_id": subdivision["division_id"]}).one_or_none(conn=conn).as_dict()
            )

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_subdivision_by_id(self, **kwargs):
        # Get body content
        division_id = kwargs.get("division_id", None)
        subdivision_id = kwargs.get("subdivision_id", None)

        subdivision = (
            SubDivision().where({"division_id": division_id}, {"subdivision_id": subdivision_id}).one_or_none()
        )

        if subdivision is None:
            raise cherrypy.HTTPError(404, "Not Found")

        division = Division().where({"division_id": subdivision.division_id}).one_or_none()

        subdivision = subdivision.as_dict()
        subdivision["division"] = division.as_dict()

        return subdivision

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["division_id", "subdivision_id", "name", "weight", "value", "status"])
    def save_subdivision(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        division_id = body.get("division_id", None)
        subdivision_id = body.get("subdivision_id", None)

        division = Division().where({"division_id": division_id}).one_or_none()

        if division is None:
            raise cherrypy.HTTPError(404, "Not Found Division")

        subdivision = (
            SubDivision().where({"division_id": division_id}, {"subdivision_id": subdivision_id}).one_or_none()
        )

        if subdivision is None:
            body["code"] = Serie.generate(reference="division_{}".format(division_id), key="subdivision")
            subdivision = SubDivision()
            subdivision.created_at = datetime.utcnow()

        subdivision.set_attrs(body)
        subdivision.updated_at = datetime.utcnow()
        subdivision.update_or_insert()
        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_subdivision(self, **kwargs):
        # Get body content
        division_id = kwargs.get("division_id", None)
        subdivision_id = kwargs.get("subdivision_id", None)

        subdivision = (
            SubDivision().where({"division_id": division_id}, {"subdivision_id": subdivision_id}).one_or_none()
        )

        if subdivision is None:
            raise cherrypy.HTTPError(404, "Not Found")

        subdivision.status = "inactive"
        subdivision.updated_at = datetime.utcnow()
        subdivision.update()

        return {}
