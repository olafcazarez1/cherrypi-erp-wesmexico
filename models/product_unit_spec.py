from .base import Model


class ProductUnitSpec(Model):
    """Database table name"""

    _TABLE = "products_units_specs"

    """Database primary keys
    """
    _IDS = ["product_id", "unit_id", "spec_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = ["product_id", "unit_id", "index", "reference", "value"]

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
    def product_id(self):
        """Getter product_id

        Args:

        Returns:
            string: product id value

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
            product_id(string): product id.

        Returns:

        Usage:
            >>> self.product_id = product_id
        """
        self.__product_id = product_id

    @property
    def unit_id(self):
        """Getter unit_id

        Args:

        Returns:
            string: unit id value

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
            unit_id(string): unit id.

        Returns:

        Usage:
            >>> self.unit_id = unit_id
        """
        self.__unit_id = unit_id

    @property
    def spec_id(self):
        """Getter spec_id

        Args:

        Returns:
            string: spec id value

        Usage:
            >>> spec_id = self.spec_id
        """
        try:
            return self.__spec_id
        except AttributeError:
            return None

    @spec_id.setter
    def spec_id(self, spec_id):
        """Setter spec_id

        Args:
            spec_id(string): spec id.

        Returns:

        Usage:
            >>> self.spec_id = spec_id
        """
        self.__spec_id = spec_id

    @property
    def index(self):
        """Getter index

        Args:

        Returns:
            int: index value

        Usage:
            >>> index = self.index
        """
        try:
            return self.__index
        except AttributeError:
            return 0

    @index.setter
    def index(self, index):
        """Setter index

        Args:
            index(int): index.

        Returns:

        Usage:
            >>> self.index = index
        """
        self.__index = index

    @property
    def reference(self):
        """Getter reference

        Args:

        Returns:
            string: reference label value

        Usage:
            >>> reference = self.reference
        """
        try:
            return self.__reference
        except AttributeError:
            return None

    @reference.setter
    def reference(self, reference):
        """Setter reference

        Args:
            reference(string): reference label.

        Returns:

        Usage:
            >>> self.reference = reference
        """
        self.__reference = reference

    @property
    def value(self):
        """Getter value

        Args:

        Returns:
            string: description value

        Usage:
            >>> value = self.value
        """
        try:
            return self.__value
        except AttributeError:
            return None

    @value.setter
    def value(self, value):
        """Setter value

        Args:
            value(string): description value.

        Returns:

        Usage:
            >>> self.value = value
        """
        self.__value = value

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
        return super().get_attrs(ProductUnitSpec)

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
        return f"ProductUnitSpec('{self.unit_id}')"
