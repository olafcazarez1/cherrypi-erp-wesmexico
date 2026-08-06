from .base import Model


class ShoppingCart(Model):

    _TABLE = "shopping_carts"

    _IDS = [
        "cart_id",
    ]

    _BINARY = []

    _UNIQUE = [
        "cart_token",
    ]

    _REQUIRED = [
        "cart_id",
        "cart_token",
        "branch_id",
        "warehouse_id",
        "client_id",
        "user_id",
        "currency",
        "exchange_rate",
        "status",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    _SEARCH_INDEX = []

    _FILTER_LIMIT_DEFAULT = 50
    _FILTER_LIMIT_MAX = 500

    _SQL_GENERATE_ID = "SELECT UUID() as `id`;"

    @property
    def cart_id(self):
        try:
            return self.__cart_id
        except AttributeError:
            return None

    @cart_id.setter
    def cart_id(self, value):
        self.__cart_id = value

    @property
    def cart_token(self):
        try:
            return self.__cart_token
        except AttributeError:
            return None

    @cart_token.setter
    def cart_token(self, value):
        self.__cart_token = value

    @property
    def branch_id(self):
        try:
            return self.__branch_id
        except AttributeError:
            return None

    @branch_id.setter
    def branch_id(self, value):
        self.__branch_id = value

    @property
    def warehouse_id(self):
        try:
            return self.__warehouse_id
        except AttributeError:
            return None

    @warehouse_id.setter
    def warehouse_id(self, value):
        self.__warehouse_id = value

    @property
    def client_id(self):
        try:
            return self.__client_id
        except AttributeError:
            return None

    @client_id.setter
    def client_id(self, value):
        self.__client_id = value

    @property
    def user_id(self):
        try:
            return self.__user_id
        except AttributeError:
            return None

    @user_id.setter
    def user_id(self, value):
        self.__user_id = value

    @property
    def currency(self):
        try:
            return self.__currency
        except AttributeError:
            return "mxn"

    @currency.setter
    def currency(self, value):
        self.__currency = value

    @property
    def exchange_rate(self):
        try:
            return self.__exchange_rate
        except AttributeError:
            return 1

    @exchange_rate.setter
    def exchange_rate(self, value):
        self.__exchange_rate = value

    @property
    def status(self):
        try:
            return self.__status
        except AttributeError:
            return "active"

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def expires_at(self):
        try:
            return self.__expires_at
        except AttributeError:
            return None

    @expires_at.setter
    def expires_at(self, value):
        self.__expires_at = value

    @property
    def created_at(self):
        try:
            return self.__created_at
        except AttributeError:
            return None

    @created_at.setter
    def created_at(self, value):
        self.__created_at = value

    @property
    def updated_at(self):
        try:
            return self.__updated_at
        except AttributeError:
            return None

    @updated_at.setter
    def updated_at(self, value):
        self.__updated_at = value

    def get_attrs(self):
        return super().get_attrs(ShoppingCart)

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    def __repr__(self):
        return f"ShoppingCart('{self.cart_id}')"