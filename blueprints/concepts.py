import cherrypy
import pymysql

from datetime import datetime
from utils.decorators import tools
from utils.query import _OR, Query
from utils.utils import Utils

from models.serie import Serie
from models.tax import Tax
from models.division import Division
from models.subdivision import SubDivision
from models.concept import Concept
from models.subconcept import SubConcept
from models.subconcept_tax import SubConceptTax


class MapConcepts(object):
    def __init__(self):
        pass

    def init(self, mapper):

        mapper.connect(
            "get_concepts",
            "/catalog/concepts",
            controller=self,
            action="get_concepts",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_concept_by_id",
            "/catalog/concept/{concept_id}",
            controller=self,
            action="get_concept_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_concept",
            "/catalog/concept/{concept_id}",
            controller=self,
            action="save_concept",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_concept",
            "/catalog/concept/{concept_id}",
            controller=self,
            action="delete_concept",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_subconcepts",
            "/catalog/concept/{concept_id}/subconcepts",
            controller=self,
            action="get_subconcepts",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_subconcept_by_id",
            "/catalog/concept/{concept_id}/subconcept/{subconcept_id}",
            controller=self,
            action="get_subconcept_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_subconcept",
            "/catalog/concept/{concept_id}/subconcept/{subconcept_id}",
            controller=self,
            action="save_subconcept",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_subconcept",
            "/catalog/concept/{concept_id}/subconcept/{subconcept_id}",
            controller=self,
            action="delete_subconcept",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_concepts(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [_OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"})]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = Concept().get_connection()
        query = Query(model=Concept())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code", "name"])

        result["results"] = query.all(collection=False, conn=conn)
        result["total_rows"] = query.count(conn=conn)

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        for concept in result["results"]:
            concept["division"] = (
                Division().where({"division_id": concept["division_id"]}).one_or_none(conn=conn).as_dict()
            )

            concept["subdivision"] = (
                SubDivision().where({"subdivision_id": concept["subdivision_id"]}).one_or_none(conn=conn).as_dict()
            )

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_concept_by_id(self, **kwargs):
        # Get body content
        concept_id = kwargs.get("concept_id", None)

        conn = Concept().get_connection()
        concept = Concept().where({"concept_id": concept_id}).one_or_none(conn=conn)

        if concept is None:
            raise cherrypy.HTTPError(404, "Not Found")

        division = Division().where({"division_id": concept.division_id}).one_or_none(conn=conn)

        subdivision = SubDivision().where({"subdivision_id": concept.subdivision_id}).one_or_none(conn=conn)

        concept = concept.as_dict()
        concept["division"] = division.as_dict()
        concept["subdivision"] = subdivision.as_dict()
        return concept

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["concept_id", "division_id", "subdivision_id", "name"])
    def save_concept(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        concept_id = body.get("concept_id", None)

        conn = Concept().get_connection()
        concept = Concept().where({"concept_id": concept_id}).one_or_none()

        try:
            conn.begin(conn)

            is_new = False
            if concept is None:
                is_new = True
                body["code"] = Serie.generate(reference="general", key="concepts", conn=conn)
                concept = Concept()
                concept.created_at = datetime.utcnow()

            concept.set_attrs(body)
            concept.updated_at = datetime.utcnow()
            concept.insert(conn=conn) if is_new else concept.update(conn=conn)
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
    def delete_concept(self, **kwargs):
        # Get body content
        concept_id = kwargs.get("concept_id", None)

        concept = Concept().where({"concept_id": concept_id}).one_or_none()

        if concept is None:
            raise cherrypy.HTTPError(404, "Not Found")

        concept.status = "inactive"
        concept.updated_at = datetime.utcnow()
        concept.update()

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_subconcepts(self, **kwargs):
        result = {}
        result["results"] = []
        result["total_rows"] = 0

        concept_id = kwargs.get("concept_id", None)
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        criterias = [
            {"concept_id": concept_id},
            _OR({"code": look_for, "op": "like"}, {"name": look_for, "op": "like"}),
        ]

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = SubConcept().get_connection()
        query = Query(model=SubConcept())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)

        result["results"] = query.all(collection=False, conn=conn)
        result["total_rows"] = query.count(conn=conn)

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        for subconcept in result["results"]:
            subconcept["concept"] = (
                Concept().where({"concept_id": subconcept["concept_id"]}).one_or_none(conn=conn).as_dict()
            )

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_subconcept_by_id(self, **kwargs):
        # Get body content
        concept_id = kwargs.get("concept_id", None)
        subconcept_id = kwargs.get("subconcept_id", None)

        conn = SubConcept().get_connection()
        subconcept = (
            SubConcept().where({"concept_id": concept_id}, {"subconcept_id": subconcept_id}).one_or_none(conn=conn)
        )

        if subconcept is None:
            raise cherrypy.HTTPError(404, "Not Found")

        concept = Concept().where({"concept_id": subconcept.concept_id}).one_or_none(conn=conn)

        division = Division().where({"division_id": concept.division_id}).one_or_none(conn=conn)

        subdivision = SubDivision().where({"subdivision_id": concept.subdivision_id}).one_or_none(conn=conn)

        result = SubConceptTax().where({"subconcept_id": subconcept_id}, {"status": "active"}).all(conn=conn)

        taxes = []
        for item in result.all():
            tax = Tax().where({"tax_id": item.tax_id}).one_or_none(conn=conn)
            m_data = tax.as_dict()
            m_data.update(item.as_dict())
            taxes.append(m_data)

        subconcept = subconcept.as_dict()
        subconcept["division"] = division.as_dict()
        subconcept["subdivision"] = subdivision.as_dict()
        subconcept["concept"] = concept.as_dict()
        subconcept["taxes"] = taxes

        return subconcept

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["concept_id", "subconcept_id", "name", "status", "taxes"])
    def save_subconcept(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        concept_id = body.get("concept_id", None)
        subconcept_id = body.get("subconcept_id", None)
        taxes = body.get("taxes", [])

        conn = Concept().get_connection()
        concept = Concept().where({"concept_id": concept_id}).one_or_none(conn=conn)

        if concept is None:
            raise cherrypy.HTTPError(404, "Not Found concept")

        try:
            conn.begin(conn)

            subconcept = (
                SubConcept().where({"concept_id": concept_id}, {"subconcept_id": subconcept_id}).one_or_none(conn=conn)
            )

            is_new = False
            if subconcept is None:
                is_new = True
                body["code"] = Serie.generate(reference="concept_{}".format(concept_id), key="subconcept")
                subconcept = SubConcept()
                subconcept.created_at = datetime.utcnow()

            subconcept.set_attrs(body, validate_unknown=False)
            subconcept.updated_at = datetime.utcnow()

            if is_new:
                subconcept.insert(conn=conn)
            else:
                subconcept.update(conn=conn)

                # disable current taxes
                result = SubConceptTax().where({"subconcept_id": subconcept_id}, {"status": "active"}).all(conn=conn)

                for item in result.all():
                    item.status = "inactive"
                    item.updated_at = datetime.utcnow()
                    item.update(conn=conn)

                # add new taxes
                for item in taxes:
                    tax = SubConceptTax()
                    tax.subconcept_id = subconcept_id
                    tax.set_attrs(item, validate_unknown=False, ignore_restricted=True)
                    tax.status = "active"
                    tax.created_at = datetime.utcnow()
                    tax.updated_at = datetime.utcnow()
                    tax.update_or_insert(conn=conn)

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
    def delete_subconcept(self, **kwargs):
        # Get body content
        concept_id = kwargs.get("concept_id", None)
        subconcept_id = kwargs.get("subconcept_id", None)

        subconcept = SubConcept().where({"concept_id": concept_id}, {"subconcept_id": subconcept_id}).one_or_none()

        if subconcept is None:
            raise cherrypy.HTTPError(404, "Not Found")

        subconcept.status = "inactive"
        subconcept.updated_at = datetime.utcnow()
        subconcept.update()

        return {}
