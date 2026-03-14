import cherrypy

from utils.decorators import tools
from utils.query import Query

from models.state import State
from models.locality import Locality
from models.municipality import Municipality


class MapLocations(object):

    def __init__(self):
        pass

    def init(self, mapper):

        mapper.connect(
            "get_states",
            "/catalog/states",
            controller=self,
            action="get_states",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_municipalities",
            "/catalog/state/{state_id}/municipalities",
            controller=self,
            action="get_municipalities",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_localities",
            "/catalog/state/{state_id}/municipality/{municipality_id}/localities",
            controller=self,
            action="get_localities",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_states(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")

        query = Query(model=State())
        query.where({"name": look_for, "op": "like"})
        query.limit(limit)
        query.offset(offset)
        query.order_by(["name"])

        result["results"] = query.all(collection=False)
        result["total_rows"] = query.count()

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_municipalities(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        state_id = kwargs.get("state_id", None)
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")

        query = Query(model=Municipality())
        query.where({"state_id": state_id}, {"name": look_for, "op": "like"})
        query.limit(limit)
        query.offset(offset)
        query.order_by(["name"])

        result["results"] = query.all(collection=False)
        result["total_rows"] = query.count()

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_localities(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        state_id = kwargs.get("state_id", None)
        municipality_id = kwargs.get("municipality_id", None)
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")

        query = Query(model=Locality())
        query.where({"state_id": state_id}, {"municipality_id": municipality_id}, {"name": look_for, "op": "like"})
        query.limit(limit)
        query.offset(offset)
        query.order_by(["name"])

        result["results"] = query.all(collection=False)
        result["total_rows"] = query.count()

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result
