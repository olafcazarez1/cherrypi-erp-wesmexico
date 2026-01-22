from .base import Model


class ProductAssignmentDocument(Model):
    """Database table name"""

    _TABLE = "products_assignments_documents"

    """Database primary keys
    """
    _IDS = ["assignment_id", "document_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = ["assignment_id", "document_id", "path"]

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
    def assignment_id(self):
        """Getter assignment_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> assignment_id = self.assignment_id
        """
        try:
            return self.__assignment_id
        except AttributeError:
            return None

    @assignment_id.setter
    def assignment_id(self, assignment_id):
        """Setter assignment_id

        Args:
            assignment_id(string): id.

        Returns:

        Usage:
            >>> self.assignment_id = assignment_id
        """
        self.__assignment_id = assignment_id

    @property
    def document_id(self):
        """Getter document_id

        Args:

        Returns:
            string: document_id value

        Usage:
            >>> document_id = self.document_id
        """
        try:
            return self.__document_id
        except AttributeError:
            return None

    @document_id.setter
    def document_id(self, document_id):
        """Setter document_id

        Args:
            document_id(string): document_id.

        Returns:

        Usage:
            >>> self.document_id = document_id
        """
        self.__document_id = document_id

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
        return super().get_attrs(ProductAssignmentDocument)

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
        return f"ProductAssignmentDocument('{self.document_id}')"
