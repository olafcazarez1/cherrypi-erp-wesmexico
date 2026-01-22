from .base import Model


class Division(Model):
    """Database table name"""

    _TABLE = "divisions"

    """Database primary keys
    """
    _IDS = ["division_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = ["division_id", "code", "name", "weight", "value", "is_global", "is_fixed", "status"]

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
    def division_id(self):
        """Getter division_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> division_id = self.division_id
        """
        try:
            return self.__division_id
        except AttributeError:
            return None

    @division_id.setter
    def division_id(self, division_id):
        """Setter division_id

        Args:
            division_id(string): id.

        Returns:

        Usage:
            >>> self.division_id = division_id
        """
        self.__division_id = division_id

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
    def is_global(self):
        """Getter is_global

        Args:

        Returns:
            bool: is_global value

        Usage:
            >>> is_global = self.is_global
        """
        try:
            return self.__is_global
        except AttributeError:
            return False

    @is_global.setter
    def is_global(self, is_global):
        """Setter is_global

        Args:
            is_global(bool): is_global.

        Returns:

        Usage:
            >>> self.is_global = is_global
        """
        self.__is_global = is_global

    @property
    def is_fixed(self):
        """Getter is_fixed

        Args:

        Returns:
            bool: is_fixed value

        Usage:
            >>> is_fixed = self.is_fixed
        """
        try:
            return self.__is_fixed
        except AttributeError:
            return False

    @is_fixed.setter
    def is_fixed(self, is_fixed):
        """Setter is_fixed

        Args:
            is_fixed(bool): is_fixed.

        Returns:

        Usage:
            >>> self.is_fixed = is_fixed
        """
        self.__is_fixed = is_fixed

    @property
    def value(self):
        """Getter value

        Args:

        Returns:
            double: value value

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
            value(double): value.

        Returns:

        Usage:
            >>> self.value = value
        """
        self.__value = value

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
        return super().get_attrs(Division)

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
        return f"Division('{self.division_id}')"
