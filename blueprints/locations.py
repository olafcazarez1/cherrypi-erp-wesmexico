import cherrypy

from utils.decorators import tools
from utils.query import Query

from models.state import State
from models.locality import Locality
from models.municipality import Municipality
from models.neighborhood import Neighborhood
from models.postal_code import PostalCode


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

        mapper.connect(
            "get_postal_code",
            "/catalog/postal-code/{zip}",
            controller=self,
            action="get_postal_code",
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



    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_postal_code(self, **kwargs):

        zip_code = str(kwargs.get("zip", "")).strip()

        if len(zip_code) != 5 or not zip_code.isdigit():
            raise cherrypy.HTTPError(
                400,
                "Invalid postal code",
            )

        conn = PostalCode().get_connection()

        postal = (
            PostalCode()
            .where({"zip": zip_code})
            .one_or_none(conn=conn)
        )

        if postal is None:
            raise cherrypy.HTTPError(
                404,
                "Postal code not found",
            )

        postal = postal.as_dict()

        state = (
            State()
            .where({
                "state_id": postal["state_id"],
            })
            .one_or_none(conn=conn)
        )

        municipality = (
            Municipality()
            .where(
                {
                    "state_id": postal["state_id"],
                },
                {
                    "municipality_id":
                        postal["municipality_id"],
                },
            )
            .one_or_none(conn=conn)
        )

        locality = (
            Locality()
            .where(
                {
                    "state_id": postal["state_id"],
                },
                {
                    "municipality_id":
                        postal["municipality_id"],
                },
                {
                    "locality_id":
                        postal["locality_id"],
                },
            )
            .one_or_none(conn=conn)
        )

        neighborhoods = (
            Neighborhood()
            .where({"zip": zip_code})
            .all(conn=conn, collection=False)
        )

        unique_neighborhoods = {}

        for item in neighborhoods:
            name = str(item.get("name", "")).strip()

            if not name:
                continue

            key = name.lower()

            if key not in unique_neighborhoods:
                unique_neighborhoods[key] = item

        neighborhoods = sorted(
            unique_neighborhoods.values(),
            key=lambda item: item["name"],
        )

        return {
            "zip": zip_code,

            "border_zone": bool(
                postal.get("border_zone", 0)
            ),

            "state": (
                state.as_dict()
                if state is not None
                else None
            ),

            "municipality": (
                municipality.as_dict()
                if municipality is not None
                else None
            ),

            "locality": (
                locality.as_dict()
                if locality is not None
                else None
            ),

            "neighborhoods": neighborhoods,
        }
