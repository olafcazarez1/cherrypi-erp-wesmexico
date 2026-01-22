from .base import Model


class StockInOutProduct(Model):
    """Database table name"""

    _TABLE = "stocks_io_details"

    """Database primary keys
    """
    _IDS = ["stock_io_id", "product_id", "measure_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "stock_io_id",
        "product_id",
        "measure_id",
        "quantity",
        "currency",
        "price",
        "subtotal",
        "discount",
        "tax",
        "total",
    ]

    """Fields should not been overrided for set_attrs method
    """
    _RESTRICTED = ["created_at", "updated_at"]

    """While the global search index is available on this fields the global
    search is going to work for q parameter in filter method
    """
    _SEARCH_INDEX = []

    """Filter limit default (Used in filters())
    """
    _FILTER_LIMIT_DEFAULT = 50

    """Maximum limit value allowed (Used in filters())
    """
    _FILTER_LIMIT_MAX = 500

    """SQL funtion to generate a virtual project id
    """
    _SQL_GENERATE_ID = "SELECT UUID() as `id`;"

    @property
    def stock_io_id(self):
        """Getter stock_io_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> stock_io_id = self.stock_io_id
        """
        try:
            return self.__stock_io_id
        except AttributeError:
            return None

    @stock_io_id.setter
    def stock_io_id(self, stock_io_id):
        """Setter stock_io_id

        Args:
                stock_io_id(string): id.

        Returns:

        Usage:
                >>> self.stock_io_id = stock_io_id
        """
        self.__stock_io_id = stock_io_id

    @property
    def product_id(self):
        """Getter product_id

        Args:

        Returns:
                string: product_id value

        Usage:
                >>> product_id = self.product_id
        """
        try:
            return self.__product_id
        except AttributeError:
            return None

    @product_id.setter
    def product_id(self, product_id):
        """Setter product_id

        Args:
                product_id(string): product_id.

        Returns:

        Usage:
                >>> self.product_id = product_id
        """
        self.__product_id = product_id

    @property
    def measure_id(self):
        """Getter measure_id

        Args:

        Returns:
                string: measure_id value

        Usage:
                >>> measure_id = self.measure_id
        """
        try:
            return self.__measure_id
        except AttributeError:
            return None

    @measure_id.setter
    def measure_id(self, measure_id):
        """Setter measure_id

        Args:
                measure_id(string): measure_id.

        Returns:

        Usage:
                >>> self.measure_id = measure_id
        """
        self.__measure_id = measure_id

    @property
    def currency(self):
        """Getter currency

        Args:

        Returns:
                double: currency value

        Usage:
                >>> currency = self.currency
        """
        try:
            return self.__currency
        except AttributeError:
            return None

    @currency.setter
    def currency(self, currency):
        """Setter currency

        Args:
                currency(double): currency.

        Returns:

        Usage:
                >>> self.currency = currency
        """
        self.__currency = currency

    @property
    def quantity(self):
        """Getter quantity

        Args:

        Returns:
                double: quantity value

        Usage:
                >>> quantity = self.quantity
        """
        try:
            return self.__quantity
        except AttributeError:
            return None

    @quantity.setter
    def quantity(self, quantity):
        """Setter quantity

        Args:
                quantity(double): quantity.

        Returns:

        Usage:
                >>> self.quantity = quantity
        """
        self.__quantity = quantity

    @property
    def price(self):
        """Getter price

        Args:

        Returns:
                double: price value

        Usage:
                >>> price = self.price
        """
        try:
            return self.__price
        except AttributeError:
            return None

    @price.setter
    def price(self, price):
        """Setter price

        Args:
                price(double): price.

        Returns:

        Usage:
                >>> self.price = price
        """
        self.__price = price

    @property
    def subtotal(self):
        """Getter subtotal

        Args:

        Returns:
                double: subtotal value

        Usage:
                >>> subtotal = self.subtotal
        """
        try:
            return self.__subtotal
        except AttributeError:
            return None

    @subtotal.setter
    def subtotal(self, subtotal):
        """Setter subtotal

        Args:
                subtotal(double): subtotal.

        Returns:

        Usage:
                >>> self.subtotal = subtotal
        """
        self.__subtotal = subtotal

    @property
    def discount(self):
        """Getter discount

        Args:

        Returns:
                double: discount value

        Usage:
                >>> discount = self.discount
        """
        try:
            return self.__discount
        except AttributeError:
            return None

    @discount.setter
    def discount(self, discount):
        """Setter discount

        Args:
                discount(double): discount.

        Returns:

        Usage:
                >>> self.discount = discount
        """
        self.__discount = discount

    @property
    def tax(self):
        """Getter tax

        Args:

        Returns:
                double: tax value

        Usage:
                >>> tax = self.tax
        """
        try:
            return self.__tax
        except AttributeError:
            return None

    @tax.setter
    def tax(self, tax):
        """Setter tax

        Args:
                tax(double): tax.

        Returns:

        Usage:
                >>> self.tax = tax
        """
        self.__tax = tax

    @property
    def total(self):
        """Getter total

        Args:

        Returns:
                double: total value

        Usage:
                >>> total = self.total
        """
        try:
            return self.__total
        except AttributeError:
            return None

    @total.setter
    def total(self, total):
        """Setter total

        Args:
                total(double): total.

        Returns:

        Usage:
                >>> self.total = total
        """
        self.__total = total

    @property
    def created_at(self):
        """Getter created_at

        Args:

        Returns:
                string: created_at value

        Usage:
                >>> created_at = self.created_at
        """
        try:
            return self.__created_at
        except AttributeError:
            return None

    @created_at.setter
    def created_at(self, created_at):
        """Setter created_at

        Args:
                created_at(string): created_at.

        Returns:

        Usage:
                >>> self.created_at = created_at
        """
        self.__created_at = created_at

    @property
    def updated_at(self):
        """Getter updated_at

        Args:

        Returns:
                string: updated_at value

        Usage:
                >>> updated_at = self.updated_at
        """
        try:
            return self.__updated_at
        except AttributeError:
            return None

    @updated_at.setter
    def updated_at(self, updated_at):
        """Setter updated_at

        Args:
                updated_at(string): updated_at.

        Returns:

        Usage:
                >>> self.updated_at = updated_at
        """
        self.__updated_at = updated_at

    def get_attrs(self):
        """Get the list of properties that belongs to this class

        Returns:
                list: List of attributes in the Model
        """
        return super().get_attrs(StockInOutProduct)

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    def __repr__(self):
        """Built-in function used to return the object representation

        Args:
                None

        Returns:
                str: A string with the object representation
        """
        return f"StockInOutProduct('{self.stock_io_id}')"
