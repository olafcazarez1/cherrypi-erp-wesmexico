import json
import cherrypy

from utils.decorators import tools
from models.product_unit import ProductUnit


class MapHelpers(object):
    def __init__(self):
        pass

    def init(self, mapper=None):
        mapper.connect(
            "evaluate_new_product_unit",
            "/helper/evaluate-new-product-unit",
            controller=self,
            action="evaluate_new_product_unit",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "evaluate_product_unit_for_disposal",
            "/helper/evaluate-product-unit-stock-out",
            controller=self,
            action="evaluate_product_unit_for_disposal",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "evaluate_product_unit_for_sell",
            "/helper/evaluate-product-unit-to-sell",
            controller=self,
            action="evaluate_product_unit_for_sell",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["product_id", "uid"])
    def evaluate_new_product_unit(self, **kwargs):
        body = cherrypy.request.json

        unit = ProductUnit().where({"product_id": body["product_id"]}, {"uid": body["uid"]}).one_or_none()

        if not unit:
            return {}

        raise cherrypy.HTTPError(406, json.dumps({"code": 101, "msg": "existing product unit uid"}))

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["product_id", "uid"])
    def evaluate_product_unit_for_disposal(self, **kwargs):
        body = cherrypy.request.json

        unit = ProductUnit().where({"product_id": body["product_id"]}, {"uid": body["uid"]}).one_or_none()

        if not unit:
            raise cherrypy.HTTPError(406, json.dumps({"code": 404, "msg": "existing product unit uid"}))

        if unit.status not in ["active"]:
            raise cherrypy.HTTPError(406, json.dumps({"code": 102, "msg": "existing product unit uid"}))

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["product_id", "uid"])
    def evaluate_product_unit_for_sell(self, **kwargs):
        body = cherrypy.request.json

        unit = ProductUnit().where({"product_id": body["product_id"]}, {"uid": body["uid"]}).one_or_none()

        if not unit:
            raise cherrypy.HTTPError(406, json.dumps({"code": 404, "msg": "existing product unit uid"}))

        if unit.status not in ["active"]:
            raise cherrypy.HTTPError(406, json.dumps({"code": 102, "msg": "existing product unit uid"}))

        return {}
