from .base import Model


class ShoppingCartItem(Model):

    _TABLE = "shopping_cart_items"

    _IDS = [
        "cart_item_id",
    ]

    _BINARY = []

    _UNIQUE = []

    _REQUIRED = [
        "cart_item_id",
        "cart_id",
        "product_id",
        "measure_id",
        "equivalence",
        "quantity",
        "currency",
        "original_price",
        "unit_price",
        "discount_amount",
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
    def cart_id(self):
        try:
            return self.__cart_id
        except AttributeError:
            return None

    @cart_id.setter
    def cart_id(self, value):
        self.__cart_id = value

    @property
    def product_id(self):
        try:
            return self.__product_id
        except AttributeError:
            return None

    @product_id.setter
    def product_id(self, value):
        self.__product_id = value

    @property
    def measure_id(self):
        try:
            return self.__measure_id
        except AttributeError:
            return None

    @measure_id.setter
    def measure_id(self, value):
        self.__measure_id = value

    @property
    def equivalence(self):
        try:
            return self.__equivalence
        except AttributeError:
            return 1

    @equivalence.setter
    def equivalence(self, value):
        self.__equivalence = value

    @property
    def quantity(self):
        try:
            return self.__quantity
        except AttributeError:
            return 1

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value

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
    def original_price(self):
        try:
            return self.__original_price
        except AttributeError:
            return 0

    @original_price.setter
    def original_price(self, value):
        self.__original_price = value

    @property
    def unit_price(self):
        try:
            return self.__unit_price
        except AttributeError:
            return 0

    @unit_price.setter
    def unit_price(self, value):
        self.__unit_price = value

    @property
    def discount_amount(self):
        try:
            return self.__discount_amount
        except AttributeError:
            return 0

    @discount_amount.setter
    def discount_amount(self, value):
        self.__discount_amount = value

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
        return super().get_attrs(ShoppingCartItem)

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    def __repr__(self):
        return f"ShoppingCartItem('{self.cart_item_id}')"