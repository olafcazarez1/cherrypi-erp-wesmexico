import re
import copy
import typing
from sqlescapy import sqlescape
from .collection import Collection
from .exceptions import CustomHTTPException
from .database import DBConnector
from .utils import Utils
from .validator import Validator


class Query:
    def __init__(self, model: object) -> None:
        """Constructor

        Args:
            - model(object): Parent model class

        Returns:
            None

        Usage:
            >>> q = Query(model=Model())
            >>> q = Query(Model())
        """
        self.model = model

    @property
    def model(self) -> typing.Type:
        """Getter model attribute

        Args:
            None

        Returns:
            object: Model

        Usage:
            >>> q = Query(model=Model())
            >>> q = Query(Model())
        """
        try:
            self.__model
        except AttributeError:
            msg = "Model was not initialized in model base," " please contact the administrator"
            raise CustomHTTPException(500, msg)

        if not isinstance(self.__model, object):
            msg = "Model was not initialized correcly," " please contact the administrator"
            raise CustomHTTPException(500, msg)
        return self.__model

    @model.setter
    def model(self, model: object) -> None:
        """Setter model attribute

        Args:
            - model(object): Parent model class

        Returns:
            None

        Usage:
            >>> self.model = Application()
        """
        self.__model = model

    @property
    def _offset(self) -> int:
        """Getter offset

        Args:
            None

        Returns:
            int: offset value

        Usage:
            >>> offset = self._offset
        """
        try:
            if not self.__offset:
                self.__offset = 0
        except AttributeError:
            self.__offset = 0
        return self.__offset

    @_offset.setter
    def _offset(self, offset: int) -> None:
        """Setter offset

        Args:
            - offset(int): Offset

        Returns:
            None

        Usage:
            >>> self._offset = offset
        """
        regex = re.compile("^[0-9]+$", re.I)
        if not regex.match(str(offset)):
            msg = "offset must be under a realistic range"
            raise CustomHTTPException(400, msg)
        self.__offset = int(offset)

    def offset(self, offset: int) -> typing.Type:
        """Add offset value into query object

        Args:
            - offset(int): Offset value

        Returns:
            Query: Return self class

        Usage:
            >>> Query(model=Model()).offset(100)
        """
        self._offset = offset
        return self

    @property
    def _limit(self) -> None:
        """Getter limit

        Args:
            - limit(int): Limit value

        Returns:
            int: limit value

        Usage:
            >>> limit = self._limit
        """
        try:
            if not self.__limit:
                self.__limit = self.model._FILTER_LIMIT_DEFAULT
        except AttributeError:
            self.__limit = self.model._FILTER_LIMIT_DEFAULT
        return self.__limit

    @_limit.setter
    def _limit(self, limit: int) -> None:
        """Setter limit

        Args:
            - limit(int): limit value

        Returns:
            int: limit value

        Usage:
            >>> self._limit = 100
        """
        regex = re.compile("^[0-9]+$", re.I)
        if not regex.match(str(limit)):
            msg = "limit must be under a realistic range"
            raise CustomHTTPException(400, msg)
        self.__limit = int(limit)

    def limit(self, limit: int) -> typing.Type:
        """Apply a LIMIT to the query

        Args:
            - limit(int): limit value

        Returns:
            Query: Return self class

        Usage:
            >>> Query(model=Model()).limit(100)
        """
        self._limit = limit
        return self

    def __offset_limit_sql(self):
        """Create LIMIT SQL statement

        Args:
            None

        Returns:
            string: Limit statement
        """
        return "LIMIT {}, {}".format(self._offset, self._limit)

    @property
    def _fields(self):
        """Getter fields

        Args:
            None

        Returns:
            string: Limit statement
        """
        try:
            return self.__fields
        except AttributeError:
            return None

    @_fields.setter
    def _fields(self, fields: list):
        """Setter fields

        Args:
            - fields(list|str): List of fields

        Returns:
            None
        """
        self.__fields = fields

    def fields(self, fields: typing.Union[list, str]) -> typing.Type:
        """Apply fields into Query

        Args:
            - fields(list|str): List of fields, comma separated string or list

        Returns:
            Query: Return self class

        # TODO change count(*) string
        """
        complement_fields = []
        if isinstance(fields, str):
            if fields is True:
                fields = "1"
            elif fields.lower() == "count(*)":
                fields = fields.lower()
            elif len(fields) > 0:
                fields = fields.split(",")
            else:
                fields = self.model.get_attrs()
        if isinstance(fields, list):
            for field in fields:
                if isinstance(field, tuple):
                    complement_fields.append(field[0])
            if len(fields) > 0:
                fields = list(set(fields) & set(self.model.get_attrs()))
            else:
                fields = self.model.get_attrs()
        else:
            if not isinstance(fields, str):
                msg = "Fields are not well formatted: {}"
                raise CustomHTTPException(400, msg.format(fields))
            if fields and len(fields) > 0:
                fields = [f.strip() for f in fields.split(",")]
                fields = list(set(fields) & set(self.model.get_attrs()))
            else:
                fields = self.model.get_attrs()
        for _field in complement_fields:
            fields.append(_field)
        self._fields = fields
        return self

    def __fields_sql(self):
        """Create fields SQL statement

        Args:
            None

        Returns:
            str: sql statement for SELECT <fields>
        """
        fields = self._fields if self._fields else self.model.get_attrs()
        if fields is True:
            return "1"
        elif isinstance(fields, str):
            if fields.startswith("count("):
                return "{} as counter".format(fields)

        _fields = []
        for item in fields:
            if re.match(r"\w+\.\*$", str(item)):
                _fields.append(item)
            elif item in self.model._BINARY:
                _fields.append("HEX(`" + self.model._TABLE + "`.`" + item + "`) as " + item)
            elif re.match(r"\w+\.\w+", str(item)):
                _fields.append(item)
            elif item in self.model._ALIAS:
                if self.model._ALIAS[item].lower().strip().startswith("concat"):
                    _fields.append("{} AS `{}` ".format(self.model._ALIAS[item], item))
                elif self.model._ALIAS[item].lower().strip().startswith("cast"):
                    _fields.append("{} AS `{}` ".format(self.model._ALIAS[item], item))
                else:
                    _fields.append("`{}`.`{}` AS `{}` ".format(self.model._TABLE, self.model._ALIAS[item], item))
            else:
                _fields.append("`{}`.`{}`".format(self.model._TABLE, item))

        return ",".join(_fields)

    @property
    def _where(self) -> typing.Type:
        """Getter instance of class Where
        Args:
            None

        Returns:
            object: Where class instance
        """
        try:
            return self.__where
        except AttributeError:
            return None

    @_where.setter
    def _where(self, where: object) -> None:
        """Setter object Where that handle Query's filter conditions

        Args:
            - where(Where): Instance of Where class to handle Query's
                filter conditions.

        Returns:
            None
        """
        self.__where = where

    def where(self, *filters):
        """Apply the given filtering criterias to the table linked to the model.

        Args:
            - *filters(list): List of search criterias as dictionary;
                The syntax is:
                `{field_name: field_value, op='XX'}` where:
                    * `field_name` MUST be the name property of the object.
                    * `field_value` the value to apply in the search criteria
                    * `op` with some of the values: `eq`, `lt`, `gt`,
                        `lte`, `like` or `gte`, default value for `op` is `eq`
                        This is optional.

                All criterion are going to be treated with the AND operator.
                E.g.
                    {'client_id': 'CLIENT_ID', 'op':'eq'}
                    {'user_id': 12345}
                    {'created': '2019-10-10 20:00:00', 'op':'lt'}

                For multi criteria rules, exist the ability to group with
                specific operators like AND & OR; The syntax is:
                    _OR(
                        {'name': 'test', 'op':'like'},
                        {'description': 'data', 'op':'like'}
                    )
                    _AND(
                        {'name': 'test', 'op':'like'},
                        {'description': 'data', 'op':'like'}
                    )

                    The grouping condition will determine the evaluation rule,
                    for example:
                    * ( `name` LIKE "%test%" OR `description` LIKE "%data%" )
                    * ( `name` LIKE "%test%" AND `description` LIKE "%data%" )

        Returns:
            Query: Return self class

        Raises:
            - CustomHTTPException
                * 400: Missing filters as arguments
                * 500: Problem with database

        Usage:
            >>> Application().filter_by({
                    'created_at': "2019-12-31 23:59:59",
                    'op': 'lt',
                    'cls': Application
                })
            >>> Classe().filter_by({
                    'id': 1000,
                    'op': 'lt',
                    'id': 100,
                    'op': 'gt'
                })

        # TODO: Request cls to create join statements
        """
        where = Where(self.model)
        where.filter_by(*filters)
        self._where = where
        return self

    def where_or(self, *filters):
        """Apply the given filtering criterias to the table linked to the model.

        Args:
            - *filters(list): List of search criterias as dictionary;
                The syntax is:
                `{field_name: field_value, op='XX'}` where:
                    * `field_name` MUST be the name property of the object.
                    * `field_value` the value to apply in the search criteria
                    * `op` with some of the values: `eq`, `lt`, `gt`,
                        `lte`, `like` or `gte`, default value for `op` is `eq`
                        This is optional.

                All criterion are going to be treated with the OR operator.
                E.g.
                    {'client_id': 'CLIENT_ID', 'op':'eq'}
                    {'user_id': 12345}
                    {'created': '2019-10-10 20:00:00', 'op':'lt'}

                For multi criteria rules, exist the ability to group with specific
                operators like AND & OR; The syntax is:
                    _OR(
                        {'name': 'test', 'op':'like'},
                        {'description': 'data', 'op':'like'}
                    )
                    _AND(
                        {'name': 'test', 'op':'like'},
                        {'description': 'data', 'op':'like'}
                    )

                    The grouping condition will determine the evaluation rule,
                    for example:
                    * ( `name` LIKE "%test%" OR `description` LIKE "%data%" )
                    * ( `name` LIKE "%test%" AND `description` LIKE "%data%" )

        Returns:
            Query: Return self class

        Raises:
            - CustomHTTPException
                * 400: Missing filters as arguments
                * 500: Problem with database
        Usage:
            >>> Application().filter_by({
                    'created_at': "2019-12-31 23:59:59",
                    'op': 'lt',
                    'cls': Application
                })
            >>> Classe().filter_by({
                    'id': 1000, 'op': 'lt', 'id': 100, 'op': 'gt'
                })
        # TODO: Request cls to create join statements
        """
        where = WhereOr(self.model)
        where.filter_by(*filters)
        self._where = where
        return self

    def filter_by(self, *filters):
        """Apply the given filtering criterias to the table linked to the model.

        Args:
            - *filters(list): List of search criterias as dictionary;
                The syntax is:
                `{field_name: field_value, op='XX'}` where:
                    * `field_name` MUST be the name property of the object.
                    * `field_value` the value to apply in the search criteria
                    * `op` with some of the values: `eq`, `lt`, `gt`,
                        `lte`, `like` or `gte`, default value for `op` is `eq`
                        This is optional.

                All criterion are going to be treated with the AND operator.
                E.g.
                    {'client_id': 'CLIENT_ID', 'op':'eq'}
                    {'user_id': 12345}
                    {'created': '2019-10-10 20:00:00', 'op':'lt'}

                For multi criteria rules, exist the ability to group with
                specific operators like AND & OR; The syntax is:
                    _OR(
                        {'name': 'test', 'op':'like'},
                        {'description': 'data', 'op':'like'}
                    )
                    _AND(
                        {'name': 'test', 'op':'like'},
                        {'description': 'data', 'op':'like'}
                    )

                    The grouping condition will determine the evaluation rule,
                    for example:
                    * ( `name` LIKE "%test%" OR `description` LIKE "%data%" )
                    * ( `name` LIKE "%test%" AND `description` LIKE "%data%" )

        Returns:
            Query: Return self class

        Raises:
            - CustomHTTPException
                * 400: Missing filters as arguments
                * 500: Problem with database

        Usage:
            >>> Application().filter_by({
                    'created_at': "2019-12-31 23:59:59",
                    'op': 'lt', 'cls': Application
                })
            >>> Classe().filter_by({
                    'id': 1000,
                    'op': 'lt',
                    'id': 100,
                    'op': 'gt'
                })

        # TODO: Request cls to create join statements
        """
        return self.where(*filters)

    def __where_sql(self):
        """Return filter SQL statement

        Args:
            None

        Returns:
            str: sql WHERE statement
        """
        sql = self._where.sql()

        if len(sql) > 0:
            return "{} {}".format("WHERE", sql)

        return ""

    @property
    def _order_by(self) -> list:
        """Getter order_by

        Args:
            None

        Returns:
            list: list of fields to order results
        """
        try:
            if not self.__order_by:
                self.__order_by = []
        except AttributeError:
            self.__order_by = []
        return self.__order_by

    @_order_by.setter
    def _order_by(self, order_by: list) -> None:
        """Setter order_by

        Args:
            - order_by(dict): List of fields to order

        Returns:
            None
        """
        try:
            if not self.__order_by:
                self.__order_by = []
        except AttributeError:
            self.__order_by = []
        finally:
            self.__order_by.append(order_by)

    def order_by(self, order_by: typing.Union[list, str], cls: list = []) -> typing.Type:
        """Apply one or more ORDER BY criterion to the query

        Args:
            order_by(dict): List of fields to order
            cls (list, optional): Receive a list of model instances where is
                going to be applied the search. Defaults to [].

        Returns:
            Query: Return self class
        """

        def _cleanup_sort_fields(order_by: str, model: any):
            _order_by = []
            for v in order_by:
                val = v
                ord = ""
                if val[0] in ["+", "-"]:
                    val = val[1:]
                    ord = v[0]

                if val in model.get_attrs():
                    _order_by.append(v)
                    continue

                if val in model._ALIAS:
                    _order_by.append(ord + model._ALIAS[val])
                    continue

            return _order_by

        def build_sort_values(order_by: str, model):
            order_by = _cleanup_sort_fields(order_by, model)
            for item in order_by:
                if item[0] == "-":
                    self._order_by.append(
                        {
                            "ord": "DESC",
                            "val": "`{}`.`{}`".format(model._TABLE, item[1:]),
                        }
                    )
                elif item[0] == "+":
                    self._order_by.append(
                        {
                            "ord": "ASC",
                            "val": "`{}`.`{}`".format(model._TABLE, item[1:]),
                        }
                    )
                else:
                    self._order_by.append({"ord": "ASC", "val": "`{}`.`{}`".format(model._TABLE, item)})

        if isinstance(order_by, str):
            order_by = order_by.split(",")
            order_by = list(filter(None, order_by))

        if not isinstance(order_by, list):
            msg = "Wrong parameter received for sort: {}"
            raise CustomHTTPException(400, msg.format(str(order_by)))

        if len(cls) > 0:
            for instance in cls:
                build_sort_values(order_by, instance)
        else:
            build_sort_values(order_by, self.model)

        return self

    def order_by_raw(self, order_by: typing.Union[list, str], cls: list = []) -> typing.Type:
        """Apply one or more ORDER BY criterion to the query

        Args:
            order_by(dict): List of fields to order
            cls (list, optional): Receive a list of model instances where is
                going to be applied the search. Defaults to [].

        Returns:
            Query: Return self class
        """

        if isinstance(order_by, str):
            order_by = order_by.split(",")
            order_by = list(filter(None, order_by))

        if not isinstance(order_by, list):
            msg = "Wrong parameter received for sort: {}"
            raise CustomHTTPException(400, msg.format(str(order_by)))

        for item in order_by:
            if item[0] == "-":
                self._order_by.append(
                    {
                        "ord": "DESC",
                        "val": "`{}`".format(item[1:]),
                    }
                )
            elif item[0] == "+":
                self._order_by.append({"ord": "ASC", "val": "`{}`".format(item[1:])})
            else:
                self._order_by.append({"ord": "ASC", "val": "`{}`".format(item)})

        return self

    def __order_by_sql(self) -> str:
        """Create order by SQL statement

        Args:
            None

        Returns:
            str: partial SQL statement
        """
        order_by = []
        if not self._order_by:
            return ""
        for _order_by in self._order_by:
            order_by.append("{} {}".format(_order_by.get("val"), _order_by.get("ord")))

        if len(order_by) <= 0:
            order_by = ""
        else:
            order_by = "{} {}".format("ORDER BY", ", ".join(order_by))
        return order_by

    def join(self, instance, *filters):
        try:
            if self._joins is None:
                self._joins = []
        except Exception:
            self._joins = []
        self._joins.append({"table": instance._TABLE, "filters": filters})
        return self

    def _join_sql(self):
        try:
            sql = ""
            if self._joins:
                for join in self._joins:
                    sql += "JOIN {} ON ({})".format(join.get("table"), " AND ".join(join.get("filters")))
        except Exception:
            sql = ""
        return sql

    def leftjoin(self, instance, *filters):
        try:
            if self._leftjoins is None:
                self._leftjoins = []
        except Exception:
            self._leftjoins = []
        self._leftjoins.append({"table": instance._TABLE, "filters": filters})
        return self

    def _leftjoin_sql(self):
        sql = ""
        try:
            if self._leftjoins:
                for join in self._leftjoins:
                    sql += "LEFT JOIN {} ON ({})".format(join.get("table"), " AND ".join(join.get("filters")))
        except Exception:
            sql = ""
        return sql

    def sql(self, remove_offset_limit=False):
        """Create SELECT SQL statement

        Args:
            None

        Returns:
            str: SQL statement
        """
        fields = self.__fields_sql()
        where = self.__where_sql()
        order_by = self.__order_by_sql()

        offset_limit = self.__offset_limit_sql()
        if remove_offset_limit:
            offset_limit = ""

        join = self._join_sql()
        leftjoin = self._leftjoin_sql()
        sql = "SELECT {} FROM `{}` {} {} {} {} {}".format(
            fields, self.model._TABLE, join, leftjoin, where, order_by, offset_limit
        )
        return sql

    def __execute(self, sql: str, *args, conn: DBConnector = None, affect_data=False, **kwargs) -> list:
        """Execute query SQL statement (Used only for SELECT)

        Args:
            - sql(str): SQL statement to be executed
            - conn(DBConnector, optional):DB Connector object

        Returns:
            list|tuple: List of records that match with the SQL statement
        """
        connection = None
        if conn is None:
            conn = self.model.get_connection()
        else:
            connection = conn.get_connection()

        return conn.execute(sql, *args, connection=connection, affect_data=affect_data, **kwargs)

    def all(self, ignore_limit=False, conn: DBConnector = None, collection=True) -> list:
        """Return the results represented by this Query as a list

        Args:
            - ignore_limit(bool): Remove default limits from SQL Statement
            - conn(DBConnector, optional): DB Connector object
            - collection(bool): Return collection or list.

        Returns:
            Collection: Collection of instances
        """
        items = self.__execute(sql=self.sql(remove_offset_limit=ignore_limit), conn=conn)

        if collection:
            objs = Collection(self.model.__class__)
            for item in items:
                obj = self.model.__class__()
                for k, v in item.items():
                    if k == "pass":
                        k = "_pass"
                    obj.__setattr__(k, v)
                objs.add(obj)
            else:
                return objs
        return items

    def search(
        self,
        query: str,
        op: str = "like",
        conn: DBConnector = None,
        collection=True,
        cls: list = [],
    ) -> list:
        """Search a string in _SEARCH_INDEX fields; If this method is
        used then automatically is going to ignore filter_by method

        Args:
            query (str): String to search
            op (str, optional): Operator to search, default is 'like'.
                Defaults to "like".
            conn (DBConnector, optional): DB connector. Defaults to None.
            collection (bool, optional): True if a collection of objects is
                returned, otherwise a simple list of dicts. Defaults to True.
            cls (list, optional): Receive a list of model instances where is
                going to be applied the search. Defaults to [].

        Raises:
            CustomHTTPException:
                - 500: Invalid _SEARCH_INDEX type

        Returns:
            list: Colletion of results

        Usage:
            >>> Application().search(query="zoomcatalog")
            >>> Application().search(query="zoom", op="like", collection=True)
            >>> User().search(query="john.doe", op="like", collection=False)
            >>> User().search(query="john.doe@fakemail.com", op="eq")
        """
        try:
            if not self._SEARCH_INDEX:
                return []
        except AttributeError:
            return []

        if not isinstance(self._SEARCH_INDEX, list):
            msg = "Invalid _SEARCH_INDEX type"
            raise CustomHTTPException(500, msg)

        if not query:
            return self.all(collection=collection)

        filters = []
        for field in self._SEARCH_INDEX:
            filters.append({field: query, "op": op})

        if len(cls) > 0:
            for instance in cls:
                try:
                    for field in instance._SEARCH_INDEX:
                        filters.append({field: query, "op": op, "cls": instance})
                except Exception:
                    pass
        # Add hack to not lost original filters set in the model instance in
        # the blueprints
        _filters = []
        for f in self._where._filter:
            if isinstance(f, _OR) or isinstance(f, _AND):
                _filters.append(f)
            else:
                _filters.append(
                    {
                        f.get("field"): f.get("value"),
                        "op": f.get("op"),
                        "cls": f.get("cls"),
                    }
                )
        return self.filter_by(_OR(*filters), *_filters).all(collection=collection)

    def first(self, conn: DBConnector = None) -> typing.Union[object, None]:
        """Return the first result of this Query or None if the result does
        not contain any row.

        Args:
            - conn(str, optional): String of the DB Connector
            - uses_pool(bool, optional): If the execution should use
                or not a mysql pool

        Returns:
            object: if found the instance otherwise None
        """
        return self.one_or_none(conn=conn)

    def one_or_none(self, exception: bool = False, conn: DBConnector = None) -> typing.Union[object, None]:
        """Return one result of this Query or None if the result does
        not contain any row.

        Args:
            - uses_pool(bool, optional): If the execution should use or
                not a mysql pool
            - conn(str, optional): String of the DB Connector
            - exception(bool, optional): If True raise an exception if no
                records found

        Returns:
            object: if found the instance otherwise None
        """
        self._limit = 1
        objs = self.all(conn=conn)
        if exception and not objs:
            msg = "Not found"
            raise CustomHTTPException(404, msg)
        return objs.one_or_none()

    def count(self, conn: DBConnector = None):
        """Return a count of rows this the SQL formed by this
            Query would return

        Args:
            - conn(str, optional): String of the DB Connector
            - uses_pool(bool, optional): If the execution should use
                or not a mysql pool

        Returns:
            int: Number of rows
        """
        fields = self._fields
        limit = self._limit
        offset = self._offset

        self._fields = "count( distinct " + ",".join("`" + item + "`" for item in self.model._IDS) + ")"
        self._limit = 1
        self._offset = 0
        items = self.__execute(sql=self.sql(), conn=conn)

        self._fields = fields
        self._limit = limit
        self._offset = offset

        return items[0].get("counter", 0)

    def column_descriptions(self, conn: DBConnector = None, uses_pool: bool = None):
        """Return metadata about the columns in the TABLE

        Args:
            - conn(str, optional): String of the DB Connector
            - uses_pool(bool, optional): If the execution should use or not a mysql pool

        Returns:
            list(dict): List of columns metadata
        """
        sql = "DESC {}".format(self.model._TABLE)
        items = self.__execute(sql=sql, conn=conn, uses_pool=uses_pool)
        return items if items else []

    def __insert_sql(self, conn: DBConnector = None, ignore=False):
        """ """
        sql = "INSERT INTO `{}` SET {}"
        if ignore:
            sql = "INSERT IGNORE INTO `{}` SET {}"
        self.__validate_valid_properties()
        required = copy.deepcopy(self.model._REQUIRED)
        fields = []
        for f in [(k, v) for k, v in self.model.as_dict().items() if v is not None]:
            try:
                required.remove(f[0])
            except Exception:
                pass
            finally:
                if f[0] in self.model.get_attrs():
                    if f[0] in self.model._BINARY:
                        _sql = "`{}` = x%s"
                        if not Validator().is_binary(f[1]):
                            msg = "Wrong format for BINARY field {}"
                            raise CustomHTTPException(400, msg.format(f[0]))
                    else:
                        _sql = "`{}` = %s"

                    field = f[0]
                    if field in self.model._ALIAS:
                        field = self.model._ALIAS[field]

                    fields.append({"sql": _sql.format(field), "val": f[1]})
        if len(required) > 0:
            msg = "{} are required in insert method"
            raise CustomHTTPException(400, msg.format(",".join(required)))
        if len(fields) <= 0:
            msg = "There are not valid fields to insert"
            raise CustomHTTPException(400, msg)

        return (
            sql.format(self._TABLE, ",".join([field.get("sql") for field in fields])),
            fields,
        )

    def insert(self, conn: DBConnector = None, last_row_id=False, ignore=False):
        """Execute a DataBase Insert using the Model properties as fields

        Args:
            conn(DBConnector): DataBase connector object
            last_row_id(bool): Return or not the last row id
                True: Return the last row id
                False: Return the num of affected data
        """
        sql, fields = self.__insert_sql(ignore=ignore)
        result = self.__execute(
            sql,
            *[field.get("val") for field in fields],
            conn=conn,
            affect_data=not last_row_id,
        )
        return result

    def __replace_sql(self) -> tuple:
        """ """
        sql = "REPLACE INTO `{}` SET {}"
        self.__validate_valid_properties()

        fields = []
        for f in [(k, v) for k, v in self.model.as_dict().items() if v is not None]:
            if f[0] in self._BINARY:
                _sql = "`{}` = x%s"
                if not Validator().is_binary(f[1]):
                    msg = "Wrong format for BINARY field {}"
                    raise CustomHTTPException(400, msg.format(f[0]))
            else:
                _sql = "`{}` = %s"
            fields.append({"sql": _sql.format(f[0]), "val": f[1]})

        sql = sql.format(self._TABLE, ",".join([field.get("sql") for field in fields]))
        values = [field.get("val") for field in fields]

        return sql, values

    def replace(self, conn: DBConnector = None):
        """ """
        sql, values = self.__replace_sql()
        return self.__execute(
            sql,
            *values,
            conn=conn,
            affect_data=True,
        )

    def __update_or_insert_sql(self) -> tuple:
        """ """
        sql = "INSERT INTO `{}` SET {} ON DUPLICATE KEY UPDATE {}"
        self.__validate_valid_properties()

        fields = []
        updates = []
        for f in [(k, v) for k, v in self.model.as_dict().items() if v is not None]:
            if f[0] in self._BINARY:
                _sql = "`{}` = x%s"
                if not Validator().is_binary(f[1]):
                    msg = "Wrong format for BINARY field {}"
                    raise CustomHTTPException(400, msg.format(f[0]))
            else:
                _sql = "`{}` = %s"
            fields.append({"sql": _sql.format(f[0]), "val": f[1]})

            if f[0] not in self.model._IDS:
                updates.append({"sql": "`{}` = VALUES(`{}`)".format(f[0], f[0])})

        sql = sql.format(
            self._TABLE,
            ",".join([field.get("sql") for field in fields]),
            ",".join([field.get("sql") for field in updates]),
        )
        values = [field.get("val") for field in fields]

        return sql, values

    def update_or_insert(self, conn: DBConnector = None):
        """ """
        sql, values = self.__update_or_insert_sql()
        return self.__execute(
            sql,
            *values,
            conn=conn,
            affect_data=True,
        )

    def __update_sql(self) -> tuple:
        """ """
        ids = []
        for id in self.model.get_ids():
            if id.get("name") in self._BINARY:
                _sql = "`{}` = x%s"
            else:
                _sql = "`{}` = %s"
            ids.append({"sql": _sql.format(id.get("name")), "val": id.get("value")})
        if len(ids) <= 0:
            msg = "Not primary ids are in the model, contact the administrator"
            raise CustomHTTPException(500, msg)

        sql = "UPDATE `{}` SET {} WHERE {}"
        self.__validate_valid_properties()

        fields = []
        for f in [(k, v) for k, v in self.model.as_dict().items() if v is not None]:
            if f[0] in self.model._ALIAS:
                continue
            if f[0] in self._BINARY:
                _sql = "`{}` = x%s"
                if not Validator().is_binary(f[1]):
                    msg = "Wrong format for BINARY field {}"
                    raise CustomHTTPException(400, msg.format(f[0]))
            else:
                _sql = "`{}` = %s"
            fields.append({"sql": _sql.format(f[0]), "val": f[1]})

        sql = sql.format(
            self._TABLE,
            ",".join([field.get("sql") for field in fields]),
            " AND ".join([id.get("sql") for id in ids]),
        )
        values = [field.get("val") for field in fields]
        values.extend([id.get("val") for id in ids])

        return sql, values

    def update(self, conn: DBConnector = None):
        """ """
        sql, values = self.__update_sql()
        return self.__execute(
            sql,
            *values,
            conn=conn,
            affect_data=True,
        )

    def __delete_sql(self):
        """Not implemented yet"""
        ids = []
        for id in self.model.get_ids():
            if id.get("name") in self._BINARY:
                _sql = "`{}` = x%s"
            else:
                _sql = "`{}` = %s"
            ids.append({"sql": _sql.format(id.get("name")), "val": id.get("value")})
        if len(ids) <= 0:
            msg = "Not primary ids are in the model, contact the administrator"
            raise CustomHTTPException(500, msg)

        sql = "DELETE FROM `{}` WHERE {}"

        sql = sql.format(self._TABLE, " AND ".join([id.get("sql") for id in ids]))
        values = [id.get("val") for id in ids]
        return sql, values

    def delete(self, hard_delete: bool = False, conn: DBConnector = None):
        """ """
        if not hard_delete:
            self.status = "inactive"
            res = self.update(conn=conn)
        else:
            sql, values = self.__delete_sql()
            res = self.__execute(
                sql,
                *values,
                conn=conn,
                affect_data=True,
            )
        return res

    def exists(self, conn: DBConnector = None):
        """ """
        self._fields = True
        self._limit = 1
        sql = "SELECT EXISTS({}) as is_exists".format(self.sql())
        res = self.__execute(sql=sql, conn=conn)
        return bool(res[0].get("is_exists"))

    def __validate_valid_properties(self):
        """ """
        unknowns = []
        for f in [(k, v) for k, v in self.model.as_dict().items() if v is not None]:
            if f[0] not in self.model.get_attrs():
                unknowns.append(f[0])
        if len(unknowns) > 0:
            msg = "Unknown properties name: {}"
            raise CustomHTTPException(400, msg.format(",".join(unknowns)))


class Filter:
    @property
    def field(self):
        return self.__field

    @field.setter
    def field(self, field):
        self.__field = field

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def op(self):
        return Filter.get_operators()[self.__op]

    @op.setter
    def op(self, op):
        self.__op = op

    def __init__(self, field, value, op, cls=None):
        """Constructor

        Args:
            - field(str): Field name
            - value(str): Field value
            - op(str): Operator used between field name and value
        """
        self.__field = field
        self.__value = value
        self.__op = op
        self.__cls = cls

    @staticmethod
    def get_operators():
        """Get a list of valid operators

        Returns:
            - list
        """
        return list(Utils().operators().keys())

    def get_operator(self):
        """Get a dictionary of valid operators

        Returns:
            - dict
        """
        return Utils().operators(op=self.__op)


class Where:
    def __init__(self, model: object) -> None:
        """Constructor

        Args:
            - model(object): Parent model class

        Returns:
            None

        Usage:
            >>> q = Where(model=Model())
            >>> q = Where(Model())
        """
        self.model = model

    @property
    def model(self) -> typing.Type:
        """Getter model attribute

        Args:
            None

        Returns:
            object: Model

        Usage:
            >>> q = Query(model=Model())
            >>> q = Query(Model())
        """
        try:
            self.__model
        except AttributeError:
            msg = "Model was not initialized in model base," " please contact the administrator"
            raise CustomHTTPException(500, msg)

        if not isinstance(self.__model, object):
            msg = "Model was not initialized correcly," " please contact the administrator"
            raise CustomHTTPException(500, msg)
        return self.__model

    @model.setter
    def model(self, model: object) -> None:
        """Setter model attribute

        Args:
            - model(object): Parent model class

        Returns:
            None

        Usage:
            >>> self.model = Application()
        """
        self.__model = model

    @property
    def _filter(self) -> list:
        """Geter filters

        Args:
            None

        Returns:
            list: List of filters
        """
        try:
            return self.__filter
        except AttributeError:
            return None

    @_filter.setter
    def _filter(self, filter: dict) -> list:
        """Setter filters

        Args:
            - filter(dict): Dict of fields

        Returns:
            list: List of dict of filters
        """
        if not self._filter:
            self.__filter = []
        self.__filter.append(filter)

    def filter_by(self, *filters):
        """Apply the given filtering criterion to the table linked to the model.

        Args:
            - *filters(list): List of search criterion as dctionary; The syntax is:
                `{field_name: field_value, op='XX'}` where:
                    * `field_name` MUST be the name property of the object.
                    * `field_value` the value to apply in the search criteria
                    * `op` with some of the values: `eq`, `lt`, `gt`, `lte`
                        or `gte`, default value for `op` is `eq`.
                        This is optional.

                All criterion are going to be treated with the AND operator.
                E.g.
                    {'client_id': 'CLIENT_ID', 'op':'eq'}
                    {'user_id': 12345}
                    {'created': '2019-10-10 20:00:00', 'op':'lt'}

                For multi criteria rules, exist the ability to group with specific
                operators like AND & OR; The syntax is:
                    _OR({
                        'name': 'test', 'op':'like'},
                        {'description': 'data', 'op':'like'}
                    )
                    _AND(
                        {'name': 'test', 'op':'like'},
                        {'description': 'data', 'op':'like'}
                    )

                    The grouping condition will determine the evaluation rule, for example:
                    * ( `name` LIKE "%test%" OR `description` LIKE "%data%" )
                    * ( `name` LIKE "%test%" AND `description` LIKE "%data%" )

        Returns:
            Query: Return self class

        Raises:
            - CustomHTTPException
                * 400: Missing filters as arguments
                * 500: Problem with database

        Usage:
            >>> Application().filter_by({
                    'created_at': "2019-12-31 23:59:59",
                    'op': 'lt',
                    'cls': Application()
                })
            >>> Classe().filter_by({
                    'id': 1000, 'op': 'lt', 'id': 100, 'op': 'gt'
                })

        # TODO: Request cls to create join statements
        """

        def _split_argument(filter):
            """Split main arguments by = symbol"""
            if len(filter.split(":")) != 3:
                msg = "Wrong parameter received: {}"
                raise CustomHTTPException(400, msg.format(str(filter)))
            return filter.split(":")

        def _split_operator(value):
            """Split operator and value by : symbol"""
            ops = "|".join(list(Utils().operators().keys()))
            regex = re.compile("^({}):(.*)+$".format(ops), re.I)
            op = "eq"
            if regex.match(value):
                op, value = value.split(":", 1)
            return value, op

        def _clean_filter(filter):
            """Create the filter structure"""
            key, operator, value = _split_argument(filter)
            # value, operator = _split_operator(value)
            dict = {key: value, "op": operator}
            return dict

        if not filters:
            return self

        if not isinstance(filters, tuple):
            msg = "Filters are not well formatted 1: {}"
            raise CustomHTTPException(400, msg.format(filters))

        if isinstance(filters[0], list):
            criterias = []
            filters = list(filter(None, filters[0]))
            for criteria in filters:
                if isinstance(criteria, _OR) or isinstance(criteria, _AND):
                    criterias.append(criteria)
                else:
                    criterias.append(_clean_filter(criteria))
            filters = criterias
        else:
            filters = list(filters)
        for criteria in filters:
            if isinstance(criteria, str):
                criteria = criteria.split(":")
                if len(criteria) == 3:
                    criteria = {criteria[0]: criteria[2], "op": criteria[1]}
            if isinstance(criteria, _OR) or isinstance(criteria, _AND):
                criteria.model = self.model
                criteria.process()
                self._filter = criteria
                continue
            if not isinstance(criteria, dict):
                msg = "Filters are not well formatted 2: {}"
                raise CustomHTTPException(400, msg.format(criteria))
            criteria["op"] = criteria.get("op", "eq")
            criteria["cls"] = criteria.get("cls", self.model)
            for k, v in criteria.items():
                if k == "op":
                    if v not in Filter.get_operators():
                        msg = "Filters are not well formatted, invalid" " operator: {} in {}"
                        raise CustomHTTPException(400, msg.format(v, criteria))
                elif k == "cls":
                    if not hasattr(v, "__class__") or not isinstance(v, object):
                        msg = "Filters are not well formatted, cls is" " invalid instance: {} in {}"
                        raise CustomHTTPException(400, msg.format(v, criteria))
                elif k not in criteria["cls"].get_attrs():
                    msg = "Unknown field in filter criteria: {}"
                    raise CustomHTTPException(400, msg.format(k))

            op = criteria.pop("op")
            field, value = list(criteria.items())[0]
            self._filter = {
                "field": field,
                "value": value,
                "op": op,
                "cls": criteria["cls"],
            }
        return self

    def get_filters(self):
        """Return SELECT SQL CONDITONS statements

        Args:
            None

        Returns:
            list: list of string's SQL statement
        """
        filters = []

        if not self._filter:
            return filters

        for filter in self._filter:
            if isinstance(filter, _OR) or isinstance(filter, _AND):
                filters.append(filter.sql())
                continue

            try:
                filter["value"] = filter.get("value").replace('"', '"')
            except Exception:
                pass

            if filter.get("op").lower() == "like":
                filter["value"] = sqlescape(filter.get("value"))
                sql = '`{}`.`{}` {} "%%{}%%"'
            elif filter.get("op").lower() in ["in", "not in"]:
                if isinstance(filter.get("value"), list):
                    filter["value"] = '"{}"'.format('", "'.join(filter.get("value")))
                else:
                    filter["value"] = filter.get("value")
                sql = "`{}`.`{}` {} ({})"
            elif filter.get("field") in filter.get("cls")._BINARY:
                if not Validator().is_binary(filter.get("value")):
                    msg = "Wrong format for BINARY field {}"
                    raise CustomHTTPException(400, msg.format(filter.get("field")))
                sql = "`{}`.`{}` {} x'{}'"
            else:
                sql = "`{}`.`{}` {} '{}'"

            field = filter.get("field")
            if field in self.model._ALIAS:
                field = self.model._ALIAS[field]
                if field.lower().strip().startswith("concat"):
                    sql = sql.replace("`{}`.`{}`", "{}")
                    filters.append(
                        sql.format(
                            field,
                            Utils().operators(op=filter.get("op")),
                            filter.get("value"),
                        )
                    )
                    continue

            filters.append(
                sql.format(
                    filter.get("cls")._TABLE,
                    field,
                    Utils().operators(op=filter.get("op")),
                    filter.get("value"),
                )
            )
        return filters

    def sql(self):
        """Create SELECT SQL statement

        Args:
            None

        Returns:
            str: SQL statement
        """
        filters = self.get_filters()
        if len(filters) > 0:
            return "{}".format(" AND ".join(filters))

        return "TRUE"


class WhereOr(Where):
    def __init__(self, model: object) -> None:
        """Constructor

        Args:
            - model(object): Parent model class

        Returns:
            None

        Usage:
            >>> q = Where(model=Model())
            >>> q = Where(Model())
        """
        self.model = model

    def sql(self):
        """Create SELECT SQL statement

        Args:
            None

        Returns:
            str: SQL statement
        """
        filters = self.get_filters()
        if len(filters) > 0:
            return "{}".format(" OR ".join(filters))

        return "TRUE"


class _OR(Where):
    def __init__(self, *criterias) -> None:
        """Constructor the given filtering criterias to the table linked
            to the model.

        Args:
            - *criterias(list): List of search criterion as dictionary;
                The syntax is:
                `{field_name: field_value, op='XX'}` where:
                    * `field_name` MUST be the name property of the object.
                    * `field_value` the value to apply in the search criteria
                    * `op` with some of the values: `eq`, `lt`, `gt`, `lte`
                        or `gte`, default value for `op` is `eq`.
                        This is optional.

                All criterion are going to be treated with the AND operator.
                E.g.
                    _OR(
                        {'client_id': 'CLIENT_ID', 'op':'eq'},
                        {'user_id': 12345}
                    )
        """
        self._criterias = criterias

    @property
    def _criterias(self) -> list:
        """Geter filters

        Args:
            None

        Returns:
            list: List of filters
        """
        try:
            return self.__criterias
        except AttributeError:
            return None

    @_criterias.setter
    def _criterias(self, criterias: dict) -> list:
        """Setter criterias

        Args:
            - criterias(dict): Dict of fields

        Returns:
        """
        self.__criterias = criterias

    def process(self) -> None:
        self.filter_by(*self._criterias)

    def sql(self) -> None:
        """Create SELECT SQL statement

        Args:
            None

        Returns:
            str: SQL statement
        """
        filters = self.get_filters()
        if len(filters) > 0:
            return "({})".format(" OR ".join(filters))

        return "TRUE"


class _AND(_OR):
    def __init__(self, *criterias) -> None:
        """Constructor the given filtering criterias to the table
            linked to the model.

        Args:
            - *criterias(list): List of search criterion as dctionary;
                The syntax is:
                `{field_name: field_value, op='XX'}` where:
                    * `field_name` MUST be the name property of the object.
                    * `field_value` the value to apply in the search criteria
                    * `op` with some of the values: `eq`, `lt`, `gt`, `lte`
                        or `gte`, default value for `op` is `eq`.
                        This is optional.

                All criterion are going to be treated with the AND operator.
                E.g.
                    _OR(
                        {'client_id': 'CLIENT_ID', 'op':'eq'},
                        {'user_id': 12345}
                    )
        """
        self._criterias = criterias

    def sql(self) -> str:
        """Create SELECT SQL statement

        Args:
            None

        Returns:
            str: SQL statement
        """
        filters = self.get_filters()
        if len(filters) > 0:
            return "({})".format(" AND ".join(filters))

        return "TRUE"
