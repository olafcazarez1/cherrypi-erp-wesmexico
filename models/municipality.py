from .base import Model


class Municipality(Model):
    """Database table name"""

    _TABLE = "municipalities"

    """Database primary keys
    """
    _IDS = ["state_id", "municipality_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "state_id",
        "municipality_id",
        "name",
    ]

    """Fields should not been overrided for set_attrs method
    """
    _RESTRICTED = ["last_update"]

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
    def state_id(self):
        """Getter state_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> state_id = self.state_id
        """
        try:
            return self.__state_id
        except AttributeError:
            return None

    @state_id.setter
    def state_id(self, state_id):
        """Setter state_id

        Args:
            state_id(string): id.

        Returns:

        Usage:
            >>> self.state_id = state_id
        """
        self.__state_id = state_id

    @property
    def municipality_id(self):
        """Getter municipality_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> municipality_id = self.municipality_id
        """
        try:
            return self.__municipality_id
        except AttributeError:
            return None

    @municipality_id.setter
    def municipality_id(self, municipality_id):
        """Setter municipality_id

        Args:
            municipality_id(string): id.

        Returns:

        Usage:
            >>> self.municipality_id = municipality_id
        """
        self.__municipality_id = municipality_id

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
    def last_update(self):
        """Getter last_update

        Args:

        Returns:
            string: last_update value

        Usage:
            >>> last_update = self.last_update
        """
        try:
            return self.__last_update
        except AttributeError:
            return None

    @last_update.setter
    def last_update(self, last_update):
        """Setter last_update

        Args:
            last_update(string): last_update.

        Returns:

        Usage:
            >>> self.last_update = last_update
        """
        self.__last_update = last_update

    def get_attrs(self):
        """Get the list of properties that belongs to this class

        Returns:
            list: List of attributes in the Model
        """
        return super().get_attrs(Municipality)

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
        return f"Municipality('{self.state_id}')"
