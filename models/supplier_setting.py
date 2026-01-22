from .base import Model


class SupplierSetting(Model):
    """Database table"""

    _TABLE = "suppliers_settings"

    """Database primary keys
    """
    _IDS = ["supplier_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "supplier_id",
        "freight_included",
        "notes",
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
    def supplier_id(self):
        """Getter supplier_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> supplier_id = self.supplier_id
        """
        try:
            return self.__supplier_id
        except AttributeError:
            return None

    @supplier_id.setter
    def supplier_id(self, supplier_id):
        """Setter supplier_id

        Args:
            supplier_id(string): id.

        Returns:

        Usage:
            >>> self.supplier_id = supplier_id
        """
        self.__supplier_id = supplier_id

    @property
    def freight_included(self):
        """Getter freight_included

        Args:

        Returns:
            string: freight_included value

        Usage:
            >>> freight_included = self.freight_included
        """
        try:
            return self.__freight_included
        except AttributeError:
            return None

    @freight_included.setter
    def freight_included(self, freight_included):
        """Setter freight_included

        Args:
            freight_included(string): freight_included.

        Returns:

        Usage:
            >>> self.freight_included = freight_included
        """
        self.__freight_included = freight_included

    @property
    def notes(self):
        """Getter notes

        Args:

        Returns:
            string: notes value

        Usage:
            >>> notes = self.notes
        """
        try:
            return self.__notes
        except AttributeError:
            return None

    @notes.setter
    def notes(self, notes):
        """Setter notes

        Args:
            notes(string): notes.

        Returns:

        Usage:
            >>> self.notes = notes
        """
        self.__notes = notes

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
        return super().get_attrs(SupplierSetting)

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
        return f"SupplierSetting('{self.supplier_id}')"
