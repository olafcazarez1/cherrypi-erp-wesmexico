import cherrypy
import hashlib
import uuid
import pymysql

from models.user import User
from models.employee import Employee
from models.user_employee import UserEmployee
from models.verification_code import VerificationCode
from helpers.notification import Notification

from utils.query import _OR, Query
from utils.decorators import tools

from datetime import datetime
from utils.utils import Utils


class MapUsers(object):

    def __init__(self):
        pass

    def init(self, mapper=None):

        mapper.connect(
            "get_user_info",
            "/user",
            controller=self,
            action="get_user_info",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "create_account",
            "/user/create-account",
            controller=self,
            action="create_account",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "verify_account",
            "/user/verify-account",
            controller=self,
            action="verify_account",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        mapper.connect(
            "forgot_password",
            "/user/forgot-password",
            controller=self,
            action="forgot_password",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "update_password",
            "/user/update-password",
            controller=self,
            action="update_password",
            conditions=dict(method=["PUT", "OPTIONS"]),
        )

        mapper.connect(
            "get_users",
            "/catalog/users",
            controller=self,
            action="get_users",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_user_by_id",
            "/catalog/user/{user_id}",
            controller=self,
            action="get_user_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "patch_user",
            "/catalog/user/{user_id}",
            controller=self,
            action="patch_user",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        mapper.connect(
            "delete_user",
            "/catalog/user/{user_id}",
            controller=self,
            action="delete_user",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_user_info(self, **kwargs):
        token = kwargs.get("token", None)
        user_id = token.user_id

        user = User().where({"user_id": user_id}).one_or_none()

        if user is None:
            raise cherrypy.HTTPError(404, "Not Found")

        user = user.as_dict()
        del user["password"]

        employee = (
            Employee()
            .where(
                {
                    "employee_id": (
                        UserEmployee()
                        .fields(["employee_id"])
                        .where({"user_id": user_id})
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )
            .one_or_none()
        )

        if employee:
            user["employee"] = employee.as_dict()

        return user

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.validate_body_params(["name", "email", "password"])
    def create_account(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        user_id = str(uuid.uuid4())
        name = body.get("name", None)
        email = body.get("email", None)
        password = body.get("password", None)
        typ = body.get("type", "undefined")

        user = User().where({"email": email}).one_or_none()

        if user is None:
            user = User()
            user.user_id = user_id
            user.type = typ
            user.status = "inactive"
            user.created_at = datetime.utcnow()

        # encoding password using encode()
        secret = "{salt}-{password}".format(salt=user.user_id, password=password)
        # then sending to md5()
        secret = hashlib.md5(secret.encode())

        user.name = name
        user.email = email
        user.password = secret.hexdigest()
        user.is_verified = False
        user.updated_at = datetime.utcnow()
        user.update_or_insert()

        secure = VerificationCode.generate(reference=user.user_id)

        notification = Notification()
        notification.send_welcome_message(
            {
                "domain": cherrypy.request.headers.get("Referer"),
                "email": user.email,
                "name": user.name,
                "user_id": user.user_id,
                "secure_id": secure,
            }
        )

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.validate_body_params(["user_id", "secure_id"])
    def verify_account(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        user_id = body.get("user_id", None)
        secure_id = body.get("secure_id", None)

        user = User().where({"user_id": user_id}).one_or_none()

        if user is None:
            raise cherrypy.HTTPError(404, "Not Found")

        code = (
            VerificationCode()
            .where({"user_id": user_id}, {"secure_id": secure_id}, {"status": "active"})
            .one_or_none()
        )

        if code is None:
            raise cherrypy.HTTPError(403, "Forbidden")

        user.is_verified = True
        user.update()
        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.validate_body_params(["email"])
    def forgot_password(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        email = body.get("email", None)

        user = User().where({"email": email}).one_or_none()

        if user is None:
            raise cherrypy.HTTPError(404, "Not Found")

        secure = VerificationCode.generate(reference=user.user_id)

        notification = Notification()
        notification.send_restore_password(
            {
                "domain": cherrypy.request.headers.get("Referer"),
                "email": user.email,
                "name": user.name,
                "user_id": user.user_id,
                "secure_id": secure,
            }
        )

        cherrypy.response.status = "201 Accepted"
        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.validate_body_params(["user_id", "secure_id", "password"])
    def update_password(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        user_id = body.get("user_id", None)
        secure_id = body.get("secure_id", None)
        password = body.get("password", None)

        user = User().where({"user_id": user_id}).one_or_none()

        if user is None:
            raise cherrypy.HTTPError(404, "Not Found")

        code = (
            VerificationCode()
            .where({"user_id": user_id}, {"secure_id": secure_id}, {"status": "active"})
            .one_or_none()
        )

        if code is None:
            raise cherrypy.HTTPError(403, "Forbidden")

        code.status = "inactive"
        code.updated_at = datetime.utcnow()
        code.update()

        # encoding password using encode()
        secret = "{salt}-{password}".format(salt=user_id, password=password)
        # then sending to md5()
        secret = hashlib.md5(secret.encode())
        user.password = secret.hexdigest()
        user.updated_at = datetime.utcnow()
        user.update()

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_users(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")

        filters = kwargs.get("filters", "[]")

        criterias = [_OR({"name": look_for, "op": "like"}, {"email": look_for, "op": "like"})]

        criterias = criterias + Utils().convert_filters(filters=filters, force_status=True)

        query = Query(model=User())
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
    def get_user_by_id(self, **kwargs):

        # Get body content
        user_id = kwargs.get("user_id", None)

        user = User().where({"user_id": user_id}).one_or_none()

        if user is None:
            raise cherrypy.HTTPError(404, "Not Found")

        user = user.as_dict()
        del user["password"]

        employee = (
            Employee()
            .where(
                {
                    "employee_id": (
                        UserEmployee()
                        .fields(["employee_id"])
                        .where({"user_id": user_id})
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )
            .one_or_none()
        )

        if employee:
            user["employee"] = employee.as_dict()

        return user

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(["user_id", "name", "type", "employee_id", "status"])
    def patch_user(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        user_id = body.get("user_id", None)

        conn = User().get_connection()
        user = User().where({"user_id": user_id}).one_or_none(conn=conn)

        if user is None:
            raise cherrypy.HTTPError(404, "Not Found")

        try:
            conn.begin(conn)

            user.set_attrs(body, validate_unknown=False)
            user.updated_at = datetime.utcnow()
            user.update(conn=conn)

            relation = UserEmployee()
            relation.set_attrs(body, validate_unknown=False)
            relation.created_at = datetime.utcnow()
            relation.updated_at = datetime.utcnow()
            relation.replace(conn=conn)

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
    def delete_user(self, **kwargs):

        # Get body content
        user_id = kwargs.get("user_id", None)

        user = User().where({"user_id": user_id}).one_or_none()

        if user is None:
            raise cherrypy.HTTPError(404, "Not Found")

        user.status = "inactive"
        user.updated_at = datetime.utcnow()
        user.update()

        return {}
