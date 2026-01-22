from .base import Model


class Version(Model):
    """Database table name"""

    _TABLE = "versions"

    """Database primary keys
    """
    _IDS = ["version_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "brand_id",
        "model_id",
        "version_id",
        "code",
        "name",
        # 'weight',
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
    def brand_id(self):
        """Getter brand_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> brand_id = self.brand_id
        """
        try:
            return self.__brand_id
        except AttributeError:
            return None

    @brand_id.setter
    def brand_id(self, brand_id):
        """Setter brand_id

        Args:
            brand_id(string): id.

        Returns:

        Usage:
            >>> self.brand_id = brand_id
        """
        self.__brand_id = brand_id

    @property
    def model_id(self):
        """Getter model_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> model_id = self.model_id
        """
        try:
            return self.__model_id
        except AttributeError:
            return None

    @model_id.setter
    def model_id(self, model_id):
        """Setter model_id

        Args:
            model_id(string): id.

        Returns:

        Usage:
            >>> self.model_id = model_id
        """
        self.__model_id = model_id

    @property
    def version_id(self):
        """Getter version_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> version_id = self.version_id
        """
        try:
            return self.__version_id
        except AttributeError:
            return None

    @version_id.setter
    def version_id(self, version_id):
        """Setter version_id

        Args:
            version_id(string): id.

        Returns:

        Usage:
            >>> self.version_id = version_id
        """
        self.__version_id = version_id

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

    # @property
    # def weight(self):
    # 	"""Getter weight

    # 	Args:

    # 	Returns:
    # 		string: weight value

    # 	Usage:
    # 		>>> weight = self.weight
    # 	"""
    # 	try:
    # 		return self.__weight
    # 	except AttributeError:
    # 		return None

    # @weight.setter
    # def weight(self, weight):
    # 	"""Setter weight

    # 	Args:
    # 		weight(string): weight.

    # 	Returns:

    # 	Usage:
    # 		>>> self.weight = weight
    # 	"""
    # 	self.__weight = weight

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
        return super().get_attrs(Version)

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
        return f"Version('{self.brand_id}')"
