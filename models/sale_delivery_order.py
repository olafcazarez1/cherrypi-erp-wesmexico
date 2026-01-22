from .base import Model


class SaleDeliveryOrder(Model):
    """Database table name"""

    _TABLE = "sales_deliveries_orders"

    """Database primary keys
    """
    _IDS = ["order_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database unique fields
    """
    _UNIQUE = ["code"]

    """Required fields for INSERT statement
    """
    _REQUIRED = [
        "order_id",
        "document_id",
        "company_id",
        "branch_id",
        "warehouse_id",
        "client_id",
        "user_id",
        "worker_id",
        "code",
        "transaction_date",
        "notes",
        "status",
    ]

    """Fields should not be overridden for set_attrs method
    """
    _RESTRICTED = ["created_at", "updated_at"]

    """Global search index fields (q parameter in filter method)
    """
    _SEARCH_INDEX = []

    """Filter limit default (Used in filters())
    """
    _FILTER_LIMIT_DEFAULT = 50

    """Maximum limit value allowed (Used in filters())
    """
    _FILTER_LIMIT_MAX = 500

    """SQL function to generate a virtual project id
    """
    _SQL_GENERATE_ID = "SELECT UUID() as `id`;"

    @property
    def order_id(self):
        try:
            return self.__order_id
        except AttributeError:
            return None

    @order_id.setter
    def order_id(self, order_id):
        self.__order_id = order_id

    @property
    def document_id(self):
        try:
            return self.__document_id
        except AttributeError:
            return None

    @document_id.setter
    def document_id(self, document_id):
        self.__document_id = document_id

    @property
    def company_id(self):
        try:
            return self.__company_id
        except AttributeError:
            return None

    @company_id.setter
    def company_id(self, company_id):
        self.__company_id = company_id

    @property
    def branch_id(self):
        try:
            return self.__branch_id
        except AttributeError:
            return None

    @branch_id.setter
    def branch_id(self, branch_id):
        self.__branch_id = branch_id

    @property
    def warehouse_id(self):
        try:
            return self.__warehouse_id
        except AttributeError:
            return None

    @warehouse_id.setter
    def warehouse_id(self, warehouse_id):
        self.__warehouse_id = warehouse_id

    @property
    def client_id(self):
        try:
            return self.__client_id
        except AttributeError:
            return None

    @client_id.setter
    def client_id(self, client_id):
        self.__client_id = client_id

    @property
    def user_id(self):
        try:
            return self.__user_id
        except AttributeError:
            return None

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def worker_id(self):
        """Warehouse employee that handled the delivery"""
        try:
            return self.__worker_id
        except AttributeError:
            return None

    @worker_id.setter
    def worker_id(self, worker_id):
        self.__worker_id = worker_id

    @property
    def code(self):
        try:
            return self.__code
        except AttributeError:
            return None

    @code.setter
    def code(self, code):
        self.__code = code

    @property
    def transaction_date(self):
        try:
            return self.__transaction_date
        except AttributeError:
            return None

    @transaction_date.setter
    def transaction_date(self, transaction_date):
        self.__transaction_date = transaction_date

    @property
    def notes(self):
        try:
            return self.__notes
        except AttributeError:
            return ""

    @notes.setter
    def notes(self, notes):
        self.__notes = notes

    @property
    def status(self):
        try:
            return self.__status
        except AttributeError:
            return "active"

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def created_at(self):
        try:
            return self.__created_at
        except AttributeError:
            return None

    @created_at.setter
    def created_at(self, created_at):
        self.__created_at = created_at

    @property
    def updated_at(self):
        try:
            return self.__updated_at
        except AttributeError:
            return None

    @updated_at.setter
    def updated_at(self, updated_at):
        self.__updated_at = updated_at

    def get_attrs(self):
        return super().get_attrs(SaleDeliveryOrder)

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    def __repr__(self):
        return f"SaleDeliveryOrder('{self.order_id}')"
