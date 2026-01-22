from .base import Model


class SubCategory(Model):
    """Database table name"""

    _TABLE = "subcategories"

    """Database primary keys
    """
    _IDS = ["subcategory_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = ["category_id", "subcategory_id", "code", "name", "weight", "status"]

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
    def category_id(self):
        """Getter category_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> category_id = self.category_id
        """
        try:
            return self.__category_id
        except AttributeError:
            return None

    @category_id.setter
    def category_id(self, category_id):
        """Setter category_id

        Args:
            category_id(string): id.

        Returns:

        Usage:
            >>> self.category_id = category_id
        """
        self.__category_id = category_id

    @property
    def subcategory_id(self):
        """Getter subcategory_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> subcategory_id = self.subcategory_id
        """
        try:
            return self.__subcategory_id
        except AttributeError:
            return None

    @subcategory_id.setter
    def subcategory_id(self, subcategory_id):
        """Setter subcategory_id

        Args:
            subcategory_id(string): id.

        Returns:

        Usage:
            >>> self.subcategory_id = subcategory_id
        """
        self.__subcategory_id = subcategory_id

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
        return super().get_attrs(SubCategory)

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
        return f"SubCategory('{self.category_id}')"
