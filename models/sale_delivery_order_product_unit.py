from .base import Model


class SaleDeliveryOrderProductUnit(Model):
    """Database table name"""

    _TABLE = "sales_deliveries_orders_products_units"

    """Database primary keys
    """
    _IDS = ["order_id", "product_id", "measure_id", "unit_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database unique fields
    """
    _UNIQUE = []

    """Required fields for INSERT statement
    """
    _REQUIRED = ["order_id", "product_id", "measure_id", "unit_id", "uid"]

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
    def product_id(self):
        try:
            return self.__product_id
        except AttributeError:
            return None

    @product_id.setter
    def product_id(self, product_id):
        self.__product_id = product_id

    @property
    def measure_id(self):
        try:
            return self.__measure_id
        except AttributeError:
            return None

    @measure_id.setter
    def measure_id(self, measure_id):
        self.__measure_id = measure_id

    @property
    def unit_id(self):
        try:
            return self.__unit_id
        except AttributeError:
            return None

    @unit_id.setter
    def unit_id(self, unit_id):
        self.__unit_id = unit_id

    @property
    def uid(self):
        try:
            return self.__uid
        except AttributeError:
            return None

    @uid.setter
    def uid(self, uid):
        self.__uid = uid

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
        return super().get_attrs(SaleDeliveryOrderProductUnit)

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    def __repr__(self):
        return f"SaleDeliveryOrderProductUnit('{self.order_id}', " f"'{self.product_id}', '{self.unit_id}')"
