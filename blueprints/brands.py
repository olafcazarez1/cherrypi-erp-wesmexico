import cherrypy

from utils.decorators import tools
from utils.query import _OR, Query
from utils.utils import Utils

from datetime import datetime
from models.serie import Serie
from models.brand import Brand
from models.brand_model import BrandModel
from models.version import Version

from models.employee_product_unit import EmployeeProductUnit
from models.product_unit import ProductUnit


class MapBrands(object):

    def __init__(self):
        pass

    def init(self, mapper=None):

        mapper.connect(
            "get_brands",
            "/catalog/brands",
            controller=self,
            action="get_brands",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_brand_by_id",
            "/catalog/brand/{brand_id}",
            controller=self,
            action="get_brand_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_brand",
            "/catalog/brand/{brand_id}",
            controller=self,
            action="save_brand",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_brand",
            "/catalog/brand/{brand_id}",
            controller=self,
            action="delete_brand",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_models",
            "/catalog/brand/{brand_id}/models",
            controller=self,
            action="get_models",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_model_by_id",
            "/catalog/brand/{brand_id}/model/{model_id}",
            controller=self,
            action="get_model_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_model",
            "/catalog/brand/{brand_id}/model/{model_id}",
            controller=self,
            action="save_model",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_model",
            "/catalog/brand/{brand_id}/model/{model_id}",
            controller=self,
            action="delete_model",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_versions",
            "/catalog/brand/{brand_id}/model/{model_id}/versions",
            controller=self,
            action="get_versions",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_version_by_id",
            "/catalog/brand/{brand_id}/model/{model_id}/version/{version_id}",
            controller=self,
            action="get_version_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_version",
            "/catalog/brand/{brand_id}/model/{model_id}/version/{version_id}",
            controller=self,
            action="save_version",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_version",
            "/catalog/brand/{brand_id}/model/{model_id}/version/{version_id}",
            controller=self,
            action="delete_version",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_brands(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [_OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"})]

        criterias = criterias + Utils().convert_filters(
            filters, ignore=["related-to-product-unit", "related-to-employee-equipment"], force_status=True
        )

        # has "related-to-product"
        filter = Utils().get_filter(filters=filters, key="related-to-product-unit")

        if filter:
            criterias.append(
                {
                    "brand_id": (
                        ProductUnit()
                        .fields(["brand_id"])
                        .where({"product_id": filter["related-to-product-unit"]})
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "related-to-employee-equipment"
        filter = Utils().get_filter(filters=filters, key="related-to-employee-equipment")
        if filter:
            criterias.append(
                {
                    "brand_id": (
                        ProductUnit()
                        .fields(["brand_id"])
                        .where(
                            {
                                "unit_id": (
                                    EmployeeProductUnit()
                                    .fields(["unit_id"])
                                    .where(
                                        {"employee_id": filter["related-to-employee-equipment"], "status": "assigned"}
                                    )
                                    .sql(remove_offset_limit=True)
                                ),
                                "op": "in",
                            },
                            {"status": "assigned"},
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        query = Query(model=Brand())
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
    def get_brand_by_id(self, **kwargs):

        # Get body content
        brand_id = kwargs.get("brand_id", None)

        brand = Brand().where({"brand_id": brand_id}).one_or_none()

        if brand is None:
            raise cherrypy.HTTPError(404, "Not Found")

        return brand.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["brand_id", "name", "type", "status"])
    def save_brand(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        brand_id = body.get("brand_id", None)

        conn = Brand().get_connection()
        brand = Brand().where({"brand_id": brand_id}).one_or_none()

        is_new = False
        if brand is None:
            is_new = True
            body["code"] = Serie.generate(
                reference="general",
                key=f"brand_{body['type']}",
                conn=conn,
            )
            brand = Brand()
            brand.created_at = datetime.utcnow()

        brand.set_attrs(body)
        brand.updated_at = datetime.utcnow()

        if is_new:
            brand.insert(conn=conn)
        else:
            brand.update(conn=conn)
        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_brand(self, **kwargs):

        # Get body content
        brand_id = kwargs.get("brand_id", None)

        brand = Brand().where({"brand_id": brand_id}).one_or_none()

        if brand is None:
            raise cherrypy.HTTPError(404, "Not Found")

        brand.status = "inactive"
        brand.updated_at = datetime.utcnow()
        brand.update()

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_models(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        brand_id = kwargs.get("brand_id", None)
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [{"brand_id": brand_id}, _OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"})]

        criterias = criterias + Utils().convert_filters(
            filters, ignore=["related-to-product-unit", "related-to-employee-equipment"], force_status=True
        )

        # has "related-to-product"
        filter = Utils().get_filter(filters=filters, key="related-to-product-unit")

        if filter:
            criterias.append(
                {
                    "model_id": (
                        ProductUnit()
                        .fields(["model_id"])
                        .where({"product_id": filter["related-to-product-unit"]})
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "related-to-employee-equipment"
        filter = Utils().get_filter(filters=filters, key="related-to-employee-equipment")
        if filter:
            criterias.append(
                {
                    "model_id": (
                        ProductUnit()
                        .fields(["model_id"])
                        .where(
                            {
                                "unit_id": (
                                    EmployeeProductUnit()
                                    .fields(["unit_id"])
                                    .where(
                                        {"employee_id": filter["related-to-employee-equipment"], "status": "assigned"}
                                    )
                                    .sql(remove_offset_limit=True)
                                ),
                                "op": "in",
                            },
                            {"status": "assigned"},
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        query = Query(model=BrandModel())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code", "name"])

        result["results"] = query.all(collection=False)
        result["total_rows"] = query.count()

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_model_by_id(self, **kwargs):

        # Get body content
        brand_id = kwargs.get("brand_id", None)
        model_id = kwargs.get("model_id", None)

        model = BrandModel().where({"brand_id": brand_id}, {"model_id": model_id}).one_or_none()

        if model is None:
            raise cherrypy.HTTPError(404, "Not Found")

        brand = Brand().where({"brand_id": model.brand_id}).one_or_none()

        model = model.as_dict()
        model["brand"] = brand.as_dict()

        return model

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["brand_id", "model_id", "name"])
    def save_model(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        brand_id = body.get("brand_id", None)
        model_id = body.get("model_id", None)

        brand = Brand().where({"brand_id": brand_id}).one_or_none()

        if brand is None:
            raise cherrypy.HTTPError(404, "Not Found Brand")

        model = BrandModel().where({"brand_id": brand_id}, {"model_id": model_id}).one_or_none()

        is_new = False
        if model is None:
            is_new = True
            body["code"] = Serie.generate(reference="brand_{}".format(brand_id), key="model")
            model = BrandModel()
            model.created_at = datetime.utcnow()

        model.set_attrs(body)
        model.updated_at = datetime.utcnow()
        if is_new:
            model.insert()
        else:
            model.update()

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_model(self, **kwargs):

        # Get body content
        brand_id = kwargs.get("brand_id", None)
        model_id = kwargs.get("model_id", None)

        model = BrandModel().where({"brand_id": brand_id}, {"model_id": model_id}).one_or_none()

        if model is None:
            raise cherrypy.HTTPError(404, "Not Found")

        model.status = "inactive"
        model.updated_at = datetime.utcnow()
        model.update()

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_versions(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        brand_id = kwargs.get("brand_id", None)
        model_id = kwargs.get("model_id", None)
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [
            {"brand_id": brand_id},
            {"model_id": model_id},
            _OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"}),
        ]

        criterias = criterias + Utils().convert_filters(
            filters, ignore=["related-to-product-unit", "related-to-employee-equipment"], force_status=True
        )

        # has "related-to-product"
        filter = Utils().get_filter(filters=filters, key="related-to-product-unit")

        if filter:
            criterias.append(
                {
                    "version_id": (
                        ProductUnit()
                        .fields(["version_id"])
                        .where({"product_id": filter["related-to-product-unit"]})
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        # has "related-to-employee-equipment"
        filter = Utils().get_filter(filters=filters, key="related-to-employee-equipment")
        if filter:
            criterias.append(
                {
                    "version_id": (
                        ProductUnit()
                        .fields(["version_id"])
                        .where(
                            {
                                "unit_id": (
                                    EmployeeProductUnit()
                                    .fields(["unit_id"])
                                    .where(
                                        {"employee_id": filter["related-to-employee-equipment"], "status": "assigned"}
                                    )
                                    .sql(remove_offset_limit=True)
                                ),
                                "op": "in",
                            },
                            {"status": "assigned"},
                        )
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )

        query = Query(model=Version())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code", "name"])

        result["results"] = query.all(collection=False)
        result["total_rows"] = query.count()

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_version_by_id(self, **kwargs):

        # Get body content
        brand_id = kwargs.get("brand_id", None)
        model_id = kwargs.get("model_id", None)
        version_id = kwargs.get("version_id", None)

        version = (
            Version().where({"brand_id": brand_id}, {"model_id": model_id}, {"version_id": version_id}).one_or_none()
        )

        if version is None:
            raise cherrypy.HTTPError(404, "Not Found")

        brand = Brand().where({"brand_id": version.brand_id}).one_or_none()

        model = BrandModel().where({"brand_id": version.brand_id}, {"model_id": version.model_id}).one_or_none()

        version = version.as_dict()
        version["brand"] = brand.as_dict()
        version["model"] = model.as_dict()

        return version

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["brand_id", "model_id", "version_id", "name"])
    def save_version(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        brand_id = body.get("brand_id", None)
        model_id = body.get("model_id", None)
        version_id = body.get("version_id", None)

        model = BrandModel().where({"brand_id": brand_id}, {"model_id": model_id}).one_or_none()

        if model is None:
            raise cherrypy.HTTPError(404, "Not Found Brand Model")

        version = (
            Version().where({"brand_id": brand_id}, {"model_id": model_id}, {"version_id": version_id}).one_or_none()
        )

        is_new = False
        if version is None:
            is_new = True
            body["code"] = Serie.generate(reference="brand_{}_model_{}".format(brand_id, model_id), key="version")
            version = Version()
            version.created_at = datetime.utcnow()

        version.set_attrs(body)
        version.updated_at = datetime.utcnow()

        if is_new:
            version.insert()
        else:
            version.update()

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_version(self, **kwargs):

        # Get body content
        brand_id = kwargs.get("brand_id", None)
        model_id = kwargs.get("model_id", None)
        version_id = kwargs.get("version_id", None)

        version = (
            Version().where({"brand_id": brand_id}, {"model_id": model_id}, {"version_id": version_id}).one_or_none()
        )

        if version is None:
            raise cherrypy.HTTPError(404, "Not Found")

        version.status = "inactive"
        version.updated_at = datetime.utcnow()
        version.update()

        return {}
