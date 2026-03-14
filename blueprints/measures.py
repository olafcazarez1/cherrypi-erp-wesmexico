import cherrypy
import pymysql

from models.serie import Serie
from models.measure import Measure

from utils.query import _OR, Query
from utils.decorators import tools
from utils.utils import Utils

from datetime import datetime


class MapMeasures(object):

    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_measures",
            "/catalog/measures",
            controller=self,
            action="get_measures",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_measure_by_id",
            "/catalog/measure/{measure_id}",
            controller=self,
            action="get_measure_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_measure",
            "/catalog/measure/{measure_id}",
            controller=self,
            action="save_measure",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_measure",
            "/catalog/measure/{measure_id}",
            controller=self,
            action="delete_measure",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_measures(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")
        sort = kwargs.get("sort", ["-code", "name"])

        criterias = []
        if look_for:
            criterias = [
                _OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"}),
            ]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        query = Query(model=Measure())
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
    def get_measure_by_id(self, **kwargs):
        # Get body content
        measure_id = kwargs.get("measure_id", None)

        measure = Measure().where({"measure_id": measure_id}).one_or_none()

        if measure is None:
            raise cherrypy.HTTPError(404, "Not Found")

        return measure.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["measure_id", "name", "external_reference", "weight", "status"])
    def save_measure(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        measure_id = body.get("measure_id", None)

        conn = Measure().get_connection()
        measure = Measure().where({"measure_id": measure_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            is_new = False
            if measure is None:
                is_new = True
                body["code"] = Serie.generate(reference="general", key="measure", conn=conn)
                measure = Measure()
                measure.created_at = datetime.utcnow()

            measure.set_attrs(body)
            measure.updated_at = datetime.utcnow()

            if is_new:
                measure.insert(conn=conn)
            else:
                measure.update(conn=conn)
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
    def delete_measure(self, **kwargs):
        # Get body content
        measure_id = kwargs.get("measure_id", None)

        measure = Measure().where({"measure_id": measure_id}).one_or_none()

        if measure is None:
            raise cherrypy.HTTPError(404, "Not Found")

        measure.status = "inactive"
        measure.updated_at = datetime.utcnow()
        measure.update()

        return {}
