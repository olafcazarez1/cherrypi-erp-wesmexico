from .base import Model


class InvoiceDocumentProduct(Model):
    """Database table name"""

    _TABLE = "invoiced_documents_products"

    """Database primary keys
    """
    _IDS = ["invoice_id", "product_id", "measure_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "invoice_id",
        "product_id",
        "measure_id",
        "currency",
        "quantity",
        "original_price",
        "discount_factor",
        "price",
        "amount",
        "subtotal",
        "discount",
        "taxes",
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
    def invoice_id(self):
        """Getter invoice_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> invoice_id = self.invoice_id
        """
        try:
            return self.__invoice_id
        except AttributeError:
            return None

    @invoice_id.setter
    def invoice_id(self, invoice_id):
        """Setter invoice_id

        Args:
            invoice_id(string): id.

        Returns:

        Usage:
            >>> self.invoice_id = invoice_id
        """
        self.__invoice_id = invoice_id

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
    def original_price(self):
        """Getter original_price

        Args:

        Returns:
            double: original_price value

        Usage:
            >>> original_price = self.original_price
        """
        try:
            return self.__original_price
        except AttributeError:
            return None

    @original_price.setter
    def original_price(self, original_price):
        """Setter original_price

        Args:
            original_price(double): original_price.

        Returns:

        Usage:
            >>> self.original_price = original_price
        """
        self.__original_price = original_price

    @property
    def discount_factor(self):
        """Getter discount_factor

        Args:

        Returns:
            double: discount_factor value

        Usage:
            >>> discount_factor = self.discount_factor
        """
        try:
            return self.__discount_factor
        except AttributeError:
            return None

    @discount_factor.setter
    def discount_factor(self, discount_factor):
        """Setter discount_factor

        Args:
            discount_factor(double): discount_factor.

        Returns:

        Usage:
            >>> self.discount_factor = discount_factor
        """
        self.__discount_factor = discount_factor

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
    def amount(self):
        """Getter amount

        Args:

        Returns:
            double: amount value

        Usage:
            >>> amount = self.amount
        """
        try:
            return self.__amount
        except AttributeError:
            return None

    @amount.setter
    def amount(self, amount):
        """Setter amount

        Args:
            amount(double): amount.

        Returns:

        Usage:
            >>> self.amount = amount
        """
        self.__amount = amount

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
    def taxes(self):
        """Getter taxes

        Args:

        Returns:
            double: taxes value

        Usage:
            >>> taxes = self.taxes
        """
        try:
            return self.__taxes
        except AttributeError:
            return None

    @taxes.setter
    def taxes(self, taxes):
        """Setter taxes

        Args:
            taxes(double): taxes.

        Returns:

        Usage:
            >>> self.taxes = taxes
        """
        self.__taxes = taxes

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
        return super().get_attrs(InvoiceDocumentProduct)

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
        return f"InvoiceDocumentProduct('{self.invoice_id}')"
