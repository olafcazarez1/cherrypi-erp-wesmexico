from .base import Model


class QuoteDocumentTax(Model):
    """Database table name"""

    _TABLE = "quotes_documents_products_taxes"

    """Database primary keys
    """
    _IDS = ["quote_id", "product_id", "tax_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "quote_id",
        "product_id",
        "tax_id",
        "percent",
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
    def quote_id(self):
        """Getter quote_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> quote_id = self.quote_id
        """
        try:
            return self.__quote_id
        except AttributeError:
            return None

    @quote_id.setter
    def quote_id(self, quote_id):
        """Setter quote_id

        Args:
                quote_id(string): id.

        Returns:

        Usage:
                >>> self.quote_id = quote_id
        """
        self.__quote_id = quote_id

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
    def tax_id(self):
        """Getter tax_id

        Args:

        Returns:
                string: tax_id value

        Usage:
                >>> tax_id = self.tax_id
        """
        try:
            return self.__tax_id
        except AttributeError:
            return None

    @tax_id.setter
    def tax_id(self, tax_id):
        """Setter tax_id

        Args:
                tax_id(string): tax_id.

        Returns:

        Usage:
                >>> self.tax_id = tax_id
        """
        self.__tax_id = tax_id

    @property
    def percent(self):
        """Getter percent

        Args:

        Returns:
                double: percent value

        Usage:
                >>> percent = self.percent
        """
        try:
            return self.__percent
        except AttributeError:
            return None

    @percent.setter
    def percent(self, percent):
        """Setter percent

        Args:
                percent(double): percent.

        Returns:

        Usage:
                >>> self.percent = percent
        """
        self.__percent = percent

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
        return super().get_attrs(QuoteDocumentTax)

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
        return f"QuoteDocumentTax('{self.quote_id}')"
