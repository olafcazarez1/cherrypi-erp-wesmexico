import re
import decimal
import datetime

from utils.convert import Convert
from utils.query import Query
from utils.query import Where
from utils.database import DBConnector
from utils.singleton_meta import MetaConfig
from utils.exceptions import CustomHTTPException


class Model(Query):
    """Columns alias"""

    _ALIAS = {}
    _IDS = []

    def __init__(self):
        """Constructor"""
        super().__init__(self)

    def get_connection(self, conn: str = "database", uses_pool: bool = False) -> DBConnector:
        """Get database connection from the Database Pool

        Args:
            - conn(str): key of the database connection needed

        Returns:
            - DBConnector
        """
        connector = None
        try:
            meta = MetaConfig.instance()

            # ignore replication ?
            settings = meta.get_config("settings", {})
            ignore_log_actions = settings.get("disable-replication", False)
            debug = settings.get("debug", False)

            connector = DBConnector(
                uses_pool=uses_pool,
                debug=Convert().str2bool(debug),
                ignore_log_actions=Convert().str2bool(ignore_log_actions),
                **meta.get_config(conn)
            )
        except TypeError as e:
            msg = "Impossible to connec to to database, review your configurations: {}"
            raise CustomHTTPException(500, msg.format(str(e)))
        except Exception as e:
            msg = "Impossible to connecto to database: {}"
            raise CustomHTTPException(500, msg.format(str(e)))
        else:
            return connector

    def get_attrs(self, cls: object, omitted: list = []) -> list:
        """Get attributes of the model.

        Return:
            list(str): List of fields in the model
        """
        attrs = []
        for k, v in vars(cls).items():
            if k in omitted:
                continue
            if not k.startswith("_") and isinstance(v, property):
                attrs.append(k)
        return attrs

    def set_attrs(
        self,
        kwargs,
        validate_restricted=True,
        validate_properties=True,
        validate_unknown=True,
        ignore_restricted=False,
    ):
        """Set list of properties to the class

        **IMPORTANT: use this carefully, you can easy override data***

        Args:
            - kwargs(dict): Dictionary with properties to save in the model

        """
        unknowns = []
        restricted = []
        for k, v in kwargs.items():
            if k in self.get_attrs():
                if validate_restricted and k in self._RESTRICTED:
                    restricted.append(k)
                else:
                    self.__setattr__(k, v)
            else:
                if validate_properties:
                    unknowns.append(k)
        if not ignore_restricted and len(restricted) > 0:
            msg = "Trying to use restricted properties: {}"
            raise CustomHTTPException(400, msg.format(",".join(restricted)))

        if validate_unknown and len(unknowns) > 0:
            msg = "Unknown properties name: {}"
            raise CustomHTTPException(400, msg.format(",".join(unknowns)))

    def generate_id(self):
        """Generate an Id from database

        This is an inbuilt function which returns a string.

        Args:
            - cls(obj): Method belongs to the class

        Returns:
            - string: Virtual Id

        Raises:
            - CustomHTTPException
                * 500: Problem with database

        """
        conn = self.get_connection()
        row = conn.execute(self._SQL_GENERATE_ID)
        return row[0].get("id", None) if row else None

    def get_ids(self) -> list:
        """Get list of primary IDs defined in the model

        Return:
            list(str): List of IDs
        """
        ids = []
        for id in self._IDS:
            ids.append({"name": id, "value": getattr(self, id)})
        return ids

    def as_dict(self) -> dict:
        """Return the property defined in the model as dictionary

        Return:
            dict
        """
        dict = {}
        for attr, value in self.__dict__.items():
            # Need to be added to avoid
            # https://github.com/swagger-api/swagger-ui/issues/2030
            if re.match(r"[0-9]{18,}", str(value)):
                value = str(value)
            if isinstance(value, self.model.__class__):
                continue
            if isinstance(value, Where):
                continue
            if attr.startswith("_Query__"):
                continue
            attr = attr.replace("_" + self.__class__.__name__ + "__", "")
            if isinstance(value, decimal.Decimal):
                dict[attr] = float(value)
            elif isinstance(value, datetime.datetime):
                dict[attr] = value.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                dict[attr] = value
        return dict

    def __getattr__(self, attr):
        """Allow to "catch" references to attributes that don’t exist
            in this object

        Args:
            - attr(str): Attribute in the object

        Returns:
            For any attribute that does not belongs to the instance return None
        """
        return None
