import uuid

from datetime import datetime
from .base import Model


class Serie(Model):
    """Database table name"""

    _TABLE = "series"

    """Database primary keys
    """
    _IDS = ["serie_id"]

    """Database binary fields
    """
    _BINARY = []

    """Unique key fields
    """
    _UNIQUE = ["reference", "key"]

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "serie_id",
        "reference",
        "key",
        "prefix",
        "index",
    ]

    """Fields should not been overrided for set_attrs method
    """
    _RESTRICTED = ["created_at", "updated_at"]

    """While the global search index is available on this fields the global
    search is going to work for q parameter in filter method
    """
    _SEARCH_INDEX = ["reference", "serie_id"]

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
    def serie_id(self):
        """Getter serie_id

        Args:

        Returns:
            string: serie id value

        Usage:
            >>> serie_id = self.serie_id
        """
        try:
            return self.__serie_id
        except AttributeError:
            return None

    @serie_id.setter
    def serie_id(self, serie_id):
        """Setter serie_id

        Args:
            serie_id(string): serie id.

        Returns:

        Usage:
            >>> self.serie_id = serie_id
        """
        self.__serie_id = serie_id

    @property
    def reference(self):
        """Getter reference

        Args:

        Returns:
            string: reference value

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
            reference(string): reference.

        Returns:

        Usage:
            >>> self.reference = reference
        """
        self.__reference = reference

    @property
    def key(self):
        """Getter key

        Args:

        Returns:
            string: key value

        Usage:
            >>> key = self.key
        """
        try:
            return self.__key
        except AttributeError:
            return None

    @key.setter
    def key(self, key):
        """Setter key

        Args:
            key(string): key.

        Returns:

        Usage:
            >>> self.key = key
        """
        self.__key = key

    @property
    def prefix(self):
        """Getter prefix

        Args:

        Returns:
            string: prefix value

        Usage:
            >>> prefix = self.prefix
        """
        try:
            return self.__prefix
        except AttributeError:
            return None

    @prefix.setter
    def prefix(self, prefix):
        """Setter prefix

        Args:
            prefix(string): prefix.

        Returns:

        Usage:
            >>> self.prefix = prefix
        """
        self.__prefix = prefix

    @property
    def index(self):
        """Getter index

        Args:

        Returns:
            string: index value

        Usage:
            >>> index = self.index
        """
        try:
            return self.__index
        except AttributeError:
            return None

    @index.setter
    def index(self, index):
        """Setter index

        Args:
            index(string): index.

        Returns:

        Usage:
            >>> self.index = index
        """
        self.__index = index

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
        return super().get_attrs(Serie)

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
        return f"Serie('{self.serie_id}')"

    @classmethod
    def generate(cls, reference, key, prefix="", zfill=4, conn=None):

        if conn is None:
            conn = Serie().get_connection()

        serie = Serie().where({"reference": reference}, {"key": key}).one_or_none(conn=conn)

        if serie is None:
            serie = Serie()
            serie.serie_id = str(uuid.uuid4())
            serie.reference = reference
            serie.key = key
            serie.prefix = prefix.upper()
            serie.index = 0
            serie.created_at = datetime.utcnow()
            serie.insert(conn=conn)

        serie.index = serie.index + 1
        serie.updated_at = datetime.utcnow()
        serie.update(conn=conn)

        return "{prefix}{index}".format(prefix=serie.prefix, index=str(serie.index).zfill(zfill))
