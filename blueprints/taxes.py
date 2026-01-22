import cherrypy
import pymysql

from models.serie import Serie
from models.tax import Tax

from utils.query import _OR, Query
from utils.decorators import tools
from utils.utils import Utils

from datetime import datetime


class MapTaxes(object):

    def __init__(self):
        pass

    def init(self, mapper=None):
        mapper.connect(
            "get_taxes",
            "/catalog/taxes",
            controller=self,
            action="get_taxes",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_tax_by_id",
            "/catalog/tax/{tax_id}",
            controller=self,
            action="get_tax_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_tax",
            "/catalog/tax/{tax_id}",
            controller=self,
            action="save_tax",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_tax",
            "/catalog/tax/{tax_id}",
            controller=self,
            action="delete_tax",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_taxes(self, **kwargs):
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

        query = Query(model=Tax())
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
    def get_tax_by_id(self, **kwargs):
        # Get body content
        tax_id = kwargs.get("tax_id", None)

        tax = Tax().where({"tax_id": tax_id}).one_or_none()

        if tax is None:
            raise cherrypy.HTTPError(404, "Not Found")

        return tax.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["tax_id", "name", "percent", "status"])
    def save_tax(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        tax_id = body.get("tax_id", None)

        conn = Tax().get_connection()
        tax = Tax().where({"tax_id": tax_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            is_new = False
            if tax is None:
                is_new = True

                body["code"] = Serie.generate(reference="general", key="tax", conn=conn)
                tax = Tax()
                tax.created_at = datetime.utcnow()

            tax.set_attrs(body)
            tax.updated_at = datetime.utcnow()
            if is_new:
                tax.insert(conn=conn)
            else:
                tax.update(conn=conn)
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
    def delete_tax(self, **kwargs):
        # Get body content
        tax_id = kwargs.get("tax_id", None)

        tax = Tax().where({"tax_id": tax_id}).one_or_none()

        if tax is None:
            raise cherrypy.HTTPError(404, "Not Found")

        tax.status = "inactive"
        tax.updated_at = datetime.utcnow()
        tax.update()

        return {}
