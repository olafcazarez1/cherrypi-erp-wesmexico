from .base import Model


class EmployeeFonacotCredit(Model):
    """Database table"""

    _TABLE = "employees_fonacot_credits"

    """Database primary keys
    """
    _IDS = ["employee_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "employee_id",
        "reference",
        "document",
        "amount",
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
    def employee_id(self):
        """Getter employee_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> employee_id = self.employee_id
        """
        try:
            return self.__employee_id
        except AttributeError:
            return None

    @employee_id.setter
    def employee_id(self, employee_id):
        """Setter employee_id

        Args:
            employee_id(string): id.

        Returns:

        Usage:
            >>> self.employee_id = employee_id
        """
        self.__employee_id = employee_id

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
    def document(self):
        """Getter document

        Args:

        Returns:
            string: document value

        Usage:
            >>> document = self.document
        """
        try:
            return self.__document
        except AttributeError:
            return None

    @document.setter
    def document(self, document):
        """Setter document

        Args:
            document(string): document.

        Returns:

        Usage:
            >>> self.document = document
        """
        self.__document = document

    @property
    def amount(self):
        """Getter amount

        Args:

        Returns:
            string: amount value

        Usage:
            >>> amount = self.amount
        """
        try:
            return self.__amount
        except AttributeError:
            return None

    @amount.setter
    def amount(self, amount):
        """Setter amount

        Args:
            amount(number): amount.

        Returns:

        Usage:
            >>> self.amount = amount
        """
        self.__amount = amount

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
        return super().get_attrs(EmployeeFonacotCredit)

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
        return f"EmployeeFonacotCredit('{self.employee_id}')"
