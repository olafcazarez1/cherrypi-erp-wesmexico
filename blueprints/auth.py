import cherrypy
import hashlib

from datetime import datetime
from utils.decorators import tools
from utils.token.access_token import AccessToken

from models.user import User
from models.user_token import UserToken


class MapAuth(object):
    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "signin",
            "/auth/signin",
            controller=self,
            action="signin",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "signout",
            "/auth/signout",
            controller=self,
            action="signout",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "validate",
            "/auth/validate",
            controller=self,
            action="validate",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def validate(self, **kwargs):
        token = kwargs.get("token")

        t = (
            UserToken()
            .where(
                {"user_id": token.user_id},
                {"token_id": token.token_id},
                {"status": "active"},
            )
            .one_or_none()
        )

        if t is None:
            raise cherrypy.HTTPError(401, "Unauthorized")

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.validate_body_params(["email", "password"])
    def signin(self, **kwargs):
        # Get body content
        body = cherrypy.request.json
        email = body.get("email", None)
        password = body.get("password", None)

        conn = User().get_connection()
        user = User().where({"email": email}).one_or_none(conn=conn)

        if user is None:
            raise cherrypy.HTTPError(404, "Not Found")

        if not user.is_verified:
            raise cherrypy.HTTPError(423, "Not Verified")

        if user.status == "inactive":
            raise cherrypy.HTTPError(403, "Forbidden")

        # encoding password using encode()
        secret = "{salt}-{password}".format(salt=user.user_id, password=password)
        # then sending to md5()
        secret = hashlib.md5(secret.encode())

        if user.password != secret.hexdigest():
            raise cherrypy.HTTPError(401, "Unauthorized")

        token = AccessToken.generate(user_id=user.user_id, level=user.type)

        # disable previus tokens
        sql = (
            """
                DELETE FROM `{table}`
                WHERE
                    `user_id`=%s
            """
        ).format(table=UserToken()._TABLE)

        args = [user.user_id]
        conn.execute(sql, *args, connection=None)

        # Add new token
        t = UserToken()
        t.user_id = token.user_id
        t.token_id = token.token_id
        t.status = "active"
        t.created_at = datetime.utcnow()
        t.updated_at = datetime.utcnow()
        t.insert(conn=conn)

        return {"token": str(token)}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    def signout(self, **kwargs):
        token = kwargs.get("token", None)
        user_id = token.user_id

        conn = User().get_connection()
        user = User().where({"user_id": user_id}).one_or_none(conn=conn)

        if user is None:
            raise cherrypy.HTTPError(404, "Not Found")

        t = (
            UserToken()
            .where(
                {"user_id": token.user_id},
                {"token_id": token.token_id},
                {"status": "active"},
            )
            .one_or_none(conn=conn)
        )

        if t:
            t.delete(hard_delete=True, conn=conn)

        cherrypy.response.status = "205 Reset Content"
        return {}
