import os
import pymysql
import logging
from pymysqlpool.pool import Pool


class DBConnector:
    """Creates connections to database and provides a way to execute statements.

    Examples of usage:

    db = DBConnector(
            host='localhost',
            db = 'exmaple',
            user = 'username',
            passwd = 'secure_pass',
            idle_seconds = 5
    )

    1. Executing a statement that doesn't affect data and uses named parameters

    db.execute(
            'SELECT * FROM example WHERE example_id=%(example_id)s',
            example_id=1
    )

    Output:
            [{'example_id':1, 'example_name':'example'}]

    2. Executing a statement that affect data and uses positional parameters

    db.execute(
            affect_data=True,
            'DELETE FROM example WHERE example_id=%s AND example_name=%s',
            1, 'exmaple'
    )

    Output (number of rows affected):
            1

    3. Using an existing connection object

    conn = db.get_connection()
    db.execute('SELECT * FROM example', connection=conn)

    Ouput:
            [
                    {'exmaple_id':1, 'example_name': 'Example1'},
                    {'exmaple_id':2, 'example_name': 'Example2'},
                    {'exmaple_id':3, 'example_name': 'Example3'},
            ]

    4. Executing a transaction

    with db.begin() as conn:
            try:
                    db.execute(stmt1, connection=conn, affect_data=True)
                    db.execute(stmt2, connection=conn, affect_data=True)
                    db.execute(stmt3, connection=conn, affect_data=True, example_name='example')
                    conn.commit()
            except Exception as e:
                    conn.rollback()

    5. Calling a stored procedure with parameters

    db.procedure('proc_name', in_param=2, out_param=0, in_out_param=1)

    Output:
            {
                    'rowcount':23,
                    'data': None,
                    'params': {'in_param':2, 'out_param': 34, 'in_out_param': 2}
            }

    Note: parameters in stored procedure are optional (it depends if the store
    procedure need them) also checke that out an in/out params change their value
    after execution.

    Attributes:
            pool (ConnectionPool) : a object that holds a specific number of database
                    connections.

    Methods:
            execute(statement, *args, transaction=False, procedure=False, **kwargs):
                    Executes a database statement and returns an object with the result of the
                    execution.
    """

    __is_transaction = False
    __ignore_log_actions = False

    def __init__(self, uses_pool: bool = True, debug: bool = False, ignore_log_actions: bool = False, **settings):
        """Creates the connection pool to database.

        Recibes a list of keyword arguments that are in settings argument, also
        recibes a cursorclass parameter to produce a database response as a
        dictionary object.

        Parameters:
                settings (dict): keyword arguments that contains the database settings
                        to stabish a connection, the expected settings are:
                        host = Host of database server
                        user = Database user
                        passwd = Databse password
                        db = Database name
                        max_connections = Max number of open connections that pool will hold
                        idle_seconds = Time that a connection will stay idle before closes
        """
        self.uses_pool = uses_pool
        if uses_pool:
            self.pool = Pool(**settings)
            self.pool.init()
        else:
            self._settings = settings
            self._connection = pymysql.connect(**self._settings)

        # Disable Replication ?
        self.__ignore_log_actions = ignore_log_actions
        self.__debug = debug

    def __save_action(self, query: str = "", connection=None):

        sql = query.strip().lower()
        if sql == "" or sql.startswith("select"):
            return

        # Avoid duplicate actions
        if "sync_actions" in sql:
            return

        # Ignore user tokens
        if "users_tokens" in sql:
            return

        logging.info("DataBase: {}".format(query))

        sql = """
            INSERT INTO `sync_actions`.`actions`
            SET `query` = %s, `created_at` = NOW()
            """
        if connection is None:
            connection = self.get_connection()

        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, query)

        connection.commit()
        self.release(connection)

    def execute(self, sql, *args, connection=None, affect_data=False, log_actions=True, **kwargs):
        """Executes a database statement and returns the result

        This method could execute a SELECT, INSERT, DELETE, UPDATE statements

        Parameters:
                statement (str): The database statement to execute.
                args (tuple): contains positional parameters of the statment.
                connection (Connection): Contains a connection that is used to execute
                        the database operation (default id None).
                affect_data (bool): A flag to know if the statement to execute will affect
                        data (i.e INSERT, DELETE, UPDATE) or not (i.e SELECT) (default False).
                kwargs (dict): contains named parameters of the statement.

        Returns:
                int or list: A integer with the number of affected rows or a list of dict
                elements where each one represents a row obtained from the response.
        """
        query = ""

        if os.environ.get("ENVIRONMENT", None) in ["alpha", "local"]:
            print(sql % args)

        relese_connection = not connection
        if connection is None:
            connection = self.get_connection()

        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, args if args else kwargs)

        # Save action query
        query = cursor._executed

        if affect_data:
            result = cursor.rowcount
        else:
            sql = sql.strip().lower()
            if sql.startswith("insert"):
                result = cursor.lastrowid
            else:
                result = cursor.fetchall()

        if not self.__is_transaction:
            connection.commit()

        if relese_connection and not self.__is_transaction:
            self.release(connection)

        if self.__debug:
            print(query)

        if log_actions and not self.__ignore_log_actions:
            self.__save_action(query=query)
        return result

    def release(self, connection=None):
        """
        Release the connection
        """
        self.__is_transaction = False
        if self.uses_pool:
            self.pool.release(connection)
        elif self._connection.open:
            self._connection.close()

    def begin(self, conn=None):
        """Begin a transaction

        Get a connection from connection pool and begin a transaction with that
        connection

        Returns:
                Connection: A connection object tha would be use to perfom a transaction

        """
        self.__is_transaction = True
        if isinstance(conn, DBConnector):
            self.get_connection().begin()
        else:
            conn.begin()

    def commit(self, conn=None):
        """Begin a transaction

        Get a connection from connection pool and begin a transaction with that
        connection

        Returns:
                Connection: A connection object tha would be use to perfom a transaction

        """
        self.__is_transaction = False
        if isinstance(conn, DBConnector):
            self.get_connection().commit()
        else:
            conn.commit()

    def rollback(self, conn=None):
        """Begin a transaction

        Get a connection from connection pool and begin a transaction with that
        connection

        Returns:
                Connection: A connection object tha would be use to perfom a transaction

        """
        if isinstance(conn, DBConnector):
            self.get_connection().rollback()
        else:
            conn.rollback()

    def get_connection(self):
        """Get a connection from connection pool

        Returns:
                Connection: A connection object
        """
        if not self.uses_pool and not self._connection.open:
            self._connection = pymysql.connect(**self._settings)
        return self.pool.get_conn() if self.uses_pool else self._connection
