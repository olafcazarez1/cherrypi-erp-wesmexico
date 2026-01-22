from .base import Model


class EmployeeDriverLicense(Model):
    """Database table"""

    _TABLE = "employees_driving_licenses"

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
        "number",
        "issuing_agency",
        "place_of_issue",
        "type",
        "document",
        "expedition_date",
        "expiration_date",
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
    def number(self):
        """Getter number

        Args:

        Returns:
            string: number value

        Usage:
            >>> number = self.number
        """
        try:
            return self.__number
        except AttributeError:
            return None

    @number.setter
    def number(self, number):
        """Setter number

        Args:
            number(string): number.

        Returns:

        Usage:
            >>> self.number = number
        """
        self.__number = number

    @property
    def issuing_agency(self):
        """Getter issuing_agency

        Args:

        Returns:
            string: issuing_agency value

        Usage:
            >>> issuing_agency = self.issuing_agency
        """
        try:
            return self.__issuing_agency
        except AttributeError:
            return None

    @issuing_agency.setter
    def issuing_agency(self, issuing_agency):
        """Setter issuing_agency

        Args:
            issuing_agency(string): issuing_agency.

        Returns:

        Usage:
            >>> self.issuing_agency = issuing_agency
        """
        self.__issuing_agency = issuing_agency

    @property
    def place_of_issue(self):
        """Getter place_of_issue

        Args:

        Returns:
            string: place_of_issue value

        Usage:
            >>> place_of_issue = self.place_of_issue
        """
        try:
            return self.__place_of_issue
        except AttributeError:
            return None

    @place_of_issue.setter
    def place_of_issue(self, place_of_issue):
        """Setter place_of_issue

        Args:
            place_of_issue(string): place_of_issue.

        Returns:

        Usage:
            >>> self.place_of_issue = place_of_issue
        """
        self.__place_of_issue = place_of_issue

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
    def expedition_date(self):
        """Getter expedition_date

        Args:

        Returns:
            string: expedition_date value

        Usage:
            >>> expedition_date = self.expedition_date
        """
        try:
            return self.__expedition_date
        except AttributeError:
            return None

    @expedition_date.setter
    def expedition_date(self, expedition_date):
        """Setter expedition_date

        Args:
            expedition_date(string): expedition_date.

        Returns:

        Usage:
            >>> self.expedition_date = expedition_date
        """
        self.__expedition_date = expedition_date

    @property
    def expiration_date(self):
        """Getter expiration_date

        Args:

        Returns:
            string: expiration_date value

        Usage:
            >>> expiration_date = self.expiration_date
        """
        try:
            return self.__expiration_date
        except AttributeError:
            return None

    @expiration_date.setter
    def expiration_date(self, expiration_date):
        """Setter expiration_date

        Args:
            expiration_date(string): expiration_date.

        Returns:

        Usage:
            >>> self.expiration_date = expiration_date
        """
        self.__expiration_date = expiration_date

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
        return super().get_attrs(EmployeeDriverLicense)

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
        return f"EmployeeDriverLicense('{self.employee_id}')"
