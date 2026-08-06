from .base import Model


class ShoppingCartItemTax(Model):

    _TABLE = "shopping_cart_item_taxes"

    _IDS = [
        "cart_item_id",
        "tax_id",
    ]

    _BINARY = []

    _UNIQUE = []

    _REQUIRED = [
        "cart_item_id",
        "tax_id",
        "percent",
        "tax_amount",
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
    def cart_item_id(self):
        try:
            return self.__cart_item_id
        except AttributeError:
            return None

    @cart_item_id.setter
    def cart_item_id(self, value):
        self.__cart_item_id = value

    @property
    def tax_id(self):
        try:
            return self.__tax_id
        except AttributeError:
            return None

    @tax_id.setter
    def tax_id(self, value):
        self.__tax_id = value

    @property
    def percent(self):
        try:
            return self.__percent
        except AttributeError:
            return 0

    @percent.setter
    def percent(self, value):
        self.__percent = value

    @property
    def tax_amount(self):
        try:
            return self.__tax_amount
        except AttributeError:
            return 0

    @tax_amount.setter
    def tax_amount(self, value):
        self.__tax_amount = value

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
        return super().get_attrs(ShoppingCartItemTax)

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    def __repr__(self):
        return (
            f"ShoppingCartItemTax("
            f"'{self.cart_item_id}', '{self.tax_id}'"
            f")"
        )