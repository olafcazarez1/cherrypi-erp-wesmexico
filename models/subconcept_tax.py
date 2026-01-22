from .base import Model


class SubConceptTax(Model):
    """Database table name"""

    _TABLE = "subconcepts_taxes"

    """Database primary keys
    """
    _IDS = ["subconcept_id", "tax_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = ["subconcept_id", "tax_id", "status"]

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
    def subconcept_id(self):
        """Getter subconcept_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> subconcept_id = self.subconcept_id
        """
        try:
            return self.__subconcept_id
        except AttributeError:
            return None

    @subconcept_id.setter
    def subconcept_id(self, subconcept_id):
        """Setter subconcept_id

        Args:
                subconcept_id(string): id.

        Returns:

        Usage:
                >>> self.subconcept_id = subconcept_id
        """
        self.__subconcept_id = subconcept_id

    @property
    def tax_id(self):
        """Getter tax_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> tax_id = self.tax_id
        """
        try:
            return self.__tax_id
        except AttributeError:
            return None

    @tax_id.setter
    def tax_id(self, tax_id):
        """Setter tax_id

        Args:
                tax_id(string): id.

        Returns:

        Usage:
                >>> self.tax_id = tax_id
        """
        self.__tax_id = tax_id

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
        return super().get_attrs(SubConceptTax)

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
        return f"SubConceptTax('{self.tax_id}')"
