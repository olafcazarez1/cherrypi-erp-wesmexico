from models.base import Model


class vProductMeasure(Model):
    """Database table name"""

    _TABLE = "v_products_measures"

    """Database primary keys
    """
    _IDS = ["product_id", "measure_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "product_id",
        "measure_id",
        "external_reference",
        "code" "name",
        "equivalence" "default",
        "weight",
        "status",
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
    def product_id(self):
        """Getter product_id

        Args:

        Returns:
            string: id value

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
            product_id(string): id.

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
            string: id value

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
            measure_id(string): id.

        Returns:

        Usage:
            >>> self.measure_id = measure_id
        """
        self.__measure_id = measure_id

    @property
    def code(self):
        """Getter code

        Args:

        Returns:
            string: code value

        Usage:
            >>> code = self.code
        """
        try:
            return self.__code
        except AttributeError:
            return None

    @code.setter
    def code(self, code):
        """Setter code

        Args:
            code(string): code.

        Returns:

        Usage:
            >>> self.code = code
        """
        self.__code = code

    @property
    def name(self):
        """Getter name

        Args:

        Returns:
            string: name value

        Usage:
            >>> name = self.name
        """
        try:
            return self.__name
        except AttributeError:
            return None

    @name.setter
    def name(self, name):
        """Setter name

        Args:
            name(string): name.

        Returns:

        Usage:
            >>> self.name = name
        """
        self.__name = name

    @property
    def external_reference(self):
        """Getter external_reference

        Args:

        Returns:
            string: external_reference value

        Usage:
            >>> external_reference = self.external_reference
        """
        try:
            return self.__external_reference
        except AttributeError:
            return None

    @external_reference.setter
    def external_reference(self, external_reference):
        """Setter external_reference

        Args:
            external_reference(string): external_reference.

        Returns:

        Usage:
            >>> self.external_reference = external_reference
        """
        self.__external_reference = external_reference

    @property
    def equivalence(self):
        """Getter equivalence

        Args:

        Returns:
            int: equivalence value

        Usage:
            >>> equivalence = self.equivalence
        """
        try:
            return self.__equivalence
        except AttributeError:
            return None

    @equivalence.setter
    def equivalence(self, equivalence):
        """Setter equivalence

        Args:
            equivalence(int): equivalence.

        Returns:

        Usage:
            >>> self.equivalence = equivalence
        """
        self.__equivalence = equivalence

    @property
    def default(self):
        """Getter default

        Args:

        Returns:
            bool: default value

        Usage:
            >>> default = self.default
        """
        try:
            return self.__default
        except AttributeError:
            return None

    @default.setter
    def default(self, default):
        """Setter default

        Args:
            default(bool): default.

        Returns:

        Usage:
            >>> self.default = default
        """
        self.__default = default

    @property
    def weight(self):
        """Getter weight

        Args:

        Returns:
            string: weight value

        Usage:
            >>> weight = self.weight
        """
        try:
            return self.__weight
        except AttributeError:
            return None

    @weight.setter
    def weight(self, weight):
        """Setter weight

        Args:
            weight(string): weight.

        Returns:

        Usage:
            >>> self.weight = weight
        """
        self.__weight = weight

    @property
    def status(self):
        """Getter status

        Args:

        Returns:
            string: status value

        Usage:
            >>> status = self.status
        """
        try:
            return self.__status
        except AttributeError:
            return "active"

    @status.setter
    def status(self, status):
        """Setter status

        Args:
            status(string): status.

        Returns:

        Usage:
            >>> self.status = status
        """
        self.__status = status

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
        return super().get_attrs(vProductMeasure)

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
        return f"vProductMeasure('{self.measure_id}')"
