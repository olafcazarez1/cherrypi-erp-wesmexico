import cherrypy

from utils.decorators import tools
from utils.query import _OR, Query
from utils.utils import Utils

from models.custom import CustomOffice


class MapCustoms(object):

    def __init__(self):
        pass

    def init(self, mapper):

        mapper.connect(
            "get_customs",
            "/catalog/customs",
            controller=self,
            action="get_customs",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_custom_by_id",
            "/catalog/custom/{custom_id}",
            controller=self,
            action="get_custom_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_customs(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 100)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [_OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"})]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        query = Query(model=CustomOffice())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["code"])

        result["results"] = query.all(collection=False)
        result["total_rows"] = query.count()

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_custom_by_id(self, **kwargs):

        # Get body content
        custom_id = kwargs.get("custom_id", None)

        custom = CustomOffice().where({"custom_id": custom_id}).one_or_none()

        if custom is None:
            raise cherrypy.HTTPError(404, "Not Found")

        return custom.as_dict()
