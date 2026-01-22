from .base import Model


class Asset(Model):
    """Database table name"""

    _TABLE = "assets"

    """Database primary keys
    """
    _IDS = ["asset_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = ["asset_id", "name", "path", "type", "height", "width", "size"]

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
    def asset_id(self):
        """Getter asset_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> asset_id = self.asset_id
        """
        try:
            return self.__asset_id
        except AttributeError:
            return None

    @asset_id.setter
    def asset_id(self, asset_id):
        """Setter asset_id

        Args:
            asset_id(string): id.

        Returns:

        Usage:
            >>> self.asset_id = asset_id
        """
        self.__asset_id = asset_id

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
    def caption(self):
        """Getter caption

        Args:

        Returns:
            string: caption value

        Usage:
            >>> caption = self.caption
        """
        try:
            return self.__caption
        except AttributeError:
            return None

    @caption.setter
    def caption(self, caption):
        """Setter caption

        Args:
            caption(string): caption.

        Returns:

        Usage:
            >>> self.caption = caption
        """
        self.__caption = caption

    @property
    def path(self):
        """Getter path

        Args:

        Returns:
            string: path value

        Usage:
            >>> path = self.path
        """
        try:
            return self.__path
        except AttributeError:
            return None

    @path.setter
    def path(self, path):
        """Setter path

        Args:
            path(string): path.

        Returns:

        Usage:
            >>> self.path = path
        """
        self.__path = path

    @property
    def type(self):
        """Getter type

        Args:

        Returns:
            string: type value

        Usage:
            >>> type = self.type
        """
        try:
            return self.__type
        except AttributeError:
            return None

    @type.setter
    def type(self, type):
        """Setter type

        Args:
            type(string): type.

        Returns:

        Usage:
            >>> self.type = type
        """
        self.__type = type

    @property
    def height(self):
        """Getter height

        Args:

        Returns:
            int: height value

        Usage:
            >>> height = self.height
        """
        try:
            return self.__height
        except AttributeError:
            return None

    @height.setter
    def height(self, height):
        """Setter height

        Args:
            height(int): height.

        Returns:

        Usage:
            >>> self.height = height
        """
        self.__height = height

    @property
    def width(self):
        """Getter width

        Args:

        Returns:
            int: width value

        Usage:
            >>> width = self.width
        """
        try:
            return self.__width
        except AttributeError:
            return None

    @width.setter
    def width(self, width):
        """Setter width

        Args:
            width(int): width.

        Returns:

        Usage:
            >>> self.width = width
        """
        self.__width = width

    @property
    def size(self):
        """Getter size

        Args:

        Returns:
            int: size value

        Usage:
            >>> size = self.size
        """
        try:
            return self.__size
        except AttributeError:
            return None

    @size.setter
    def size(self, size):
        """Setter size

        Args:
            size(int): size.

        Returns:

        Usage:
            >>> self.size = size
        """
        self.__size = size

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
        return super().get_attrs(Asset)

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
        return f"Asset('{self.asset_id}')"
