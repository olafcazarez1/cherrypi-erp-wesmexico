import cherrypy
import pymysql

from datetime import datetime
from utils.decorators import tools
from utils.query import _OR, Query
from utils.utils import Utils

from models.serie import Serie
from models.category import Category
from models.subcategory import SubCategory


class MapCategories(object):
    def __init__(self):
        pass

    def init(self, mapper=None):
        mapper.connect(
            "get_categories",
            "/catalog/categories",
            controller=self,
            action="get_categories",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_category_by_id",
            "/catalog/category/{category_id}",
            controller=self,
            action="get_category_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_category",
            "/catalog/category/{category_id}",
            controller=self,
            action="save_category",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_category",
            "/catalog/category/{category_id}",
            controller=self,
            action="delete_category",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_subcategories",
            "/catalog/category/{category_id}/subcategories",
            controller=self,
            action="get_subcategories",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_subcategory_by_id",
            "/catalog/category/{category_id}/subcategory/{subcategory_id}",
            controller=self,
            action="get_subcategory_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_subcategory",
            "/catalog/category/{category_id}/subcategory/{subcategory_id}",
            controller=self,
            action="save_subcategory",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_subcategory",
            "/catalog/category/{category_id}/subcategory/{subcategory_id}",
            controller=self,
            action="delete_subcategory",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_categories(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        typ = kwargs.get("type", None)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")
        sort = kwargs.get("sort", ["type", "-code", "name"])

        criterias = [_OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"})]

        if typ:
            criterias.append({"type": typ})

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        query = Query(model=Category())
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
    def get_category_by_id(self, **kwargs):
        # Get body content
        category_id = kwargs.get("category_id", None)

        category = Category().where({"category_id": category_id}).one_or_none()

        if category is None:
            raise cherrypy.HTTPError(404, "Not Found")

        return category.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["category_id", "name", "type", "weight", "status"])
    def save_category(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        category_id = body.get("category_id", None)

        conn = Category().get_connection()
        category = Category().where({"category_id": category_id}).one_or_none()

        try:
            conn.begin(conn)

            is_new = False
            if category is None:
                is_new = True
                body["code"] = Serie.generate(
                    reference="general",
                    key="category_of_{}".format(body.get("type")),
                    conn=conn,
                )
                category = Category()
                category.created_at = datetime.utcnow()

            category.set_attrs(body)
            category.updated_at = datetime.utcnow()

            if is_new:
                category.insert(conn=conn)
            else:
                category.update(conn=conn)

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
    def delete_category(self, **kwargs):
        # Get body content
        category_id = kwargs.get("category_id", None)

        category = Category().where({"category_id": category_id}).one_or_none()

        if category is None:
            raise cherrypy.HTTPError(404, "Not Found")

        category.status = "inactive"
        category.updated_at = datetime.utcnow()
        category.update()

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_subcategories(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        category_id = kwargs.get("category_id", None)
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")

        query = Query(model=SubCategory())
        query.where(
            {"category_id": category_id},
            _OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"}),
            {"status": "active"},
        )
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
    def get_subcategory_by_id(self, **kwargs):
        # Get body content
        category_id = kwargs.get("category_id", None)
        subcategory_id = kwargs.get("subcategory_id", None)

        subcategory = (
            SubCategory().where({"category_id": category_id}, {"subcategory_id": subcategory_id}).one_or_none()
        )

        if subcategory is None:
            raise cherrypy.HTTPError(404, "Not Found")

        category = Category().where({"category_id": subcategory.category_id}).one_or_none()

        subcategory = subcategory.as_dict()
        subcategory["category"] = category.as_dict()

        return subcategory

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["category_id", "subcategory_id", "name"])
    def save_subcategory(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        category_id = body.get("category_id", None)
        subcategory_id = body.get("subcategory_id", None)

        category = Category().where({"category_id": category_id}).one_or_none()

        if category is None:
            raise cherrypy.HTTPError(404, "Not Found Category")

        subcategory = (
            SubCategory().where({"category_id": category_id}, {"subcategory_id": subcategory_id}).one_or_none()
        )

        if subcategory is None:
            body["code"] = Serie.generate(reference="category_{}".format(category_id), key="subcategory")
            subcategory = SubCategory()
            subcategory.created_at = datetime.utcnow()

        subcategory.set_attrs(body)
        subcategory.updated_at = datetime.utcnow()
        subcategory.update_or_insert()
        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_subcategory(self, **kwargs):
        # Get body content
        category_id = kwargs.get("category_id", None)
        subcategory_id = kwargs.get("subcategory_id", None)

        subcategory = (
            SubCategory().where({"category_id": category_id}, {"subcategory_id": subcategory_id}).one_or_none()
        )

        if subcategory is None:
            raise cherrypy.HTTPError(404, "Not Found")

        subcategory.status = "inactive"
        subcategory.updated_at = datetime.utcnow()
        subcategory.update()

        return {}
