from .base import Model


class DocumentInvoice(Model):
    """Database table name"""

    _TABLE = "documents_invoices"

    """Database primary keys
    """
    _IDS = ["invoice_id", "document_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = ["invoice_id", "document_id", "status"]

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
    def invoice_id(self):
        """Getter invoice_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> invoice_id = self.invoice_id
        """
        try:
            return self.__invoice_id
        except AttributeError:
            return None

    @invoice_id.setter
    def invoice_id(self, invoice_id):
        """Setter invoice_id

        Args:
            invoice_id(string): id.

        Returns:

        Usage:
            >>> self.invoice_id = invoice_id
        """
        self.__invoice_id = invoice_id

    @property
    def document_id(self):
        """Getter document_id

        Args:

        Returns:
            string: id value

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
            document_id(string): id.

        Returns:

        Usage:
            >>> self.document_id = document_id
        """
        self.__document_id = document_id

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
        return super().get_attrs(DocumentInvoice)

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
        return f"DocumentInvoice('{self.invoice_id}')"
