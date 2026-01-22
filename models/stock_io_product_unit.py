from .base import Model


class StockInOutProductUnit(Model):
    """Database table name"""

    _TABLE = "stocks_io_products_units"

    """Database primary keys
    """
    _IDS = ["stock_io_id", "product_id", "unit_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = ["stock_io_id", "product_id", "measure_id", "unit_id", "uid"]

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
    def unit_id(self):
        """Getter unit_id

        Args:

        Returns:
                str: unit_id value

        Usage:
                >>> unit_id = self.unit_id
        """
        try:
            return self.__unit_id
        except AttributeError:
            return None

    @unit_id.setter
    def unit_id(self, unit_id):
        """Setter unit_id

        Args:
                unit_id(str): unit_id.

        Returns:

        Usage:
                >>> self.unit_id = unit_id
        """
        self.__unit_id = unit_id

    @property
    def uid(self):
        """Getter uid

        Args:

        Returns:
                double: uid value

        Usage:
                >>> uid = self.uid
        """
        try:
            return self.__uid
        except AttributeError:
            return None

    @uid.setter
    def uid(self, uid):
        """Setter uid

        Args:
                uid(double): uid.

        Returns:

        Usage:
                >>> self.uid = uid
        """
        self.__uid = uid

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
        return super().get_attrs(StockInOutProductUnit)

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
        return f"StockInOutProductUnit('{self.stock_io_id}')"
