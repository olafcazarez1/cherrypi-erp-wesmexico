from .base import Model


class EmployeeMedicalInsurance(Model):
    """Database table"""

    _TABLE = "employees_medicals_insurances"

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
        "hospital",
        "document",
        "start_date",
        "leave_date",
        "withdrawal",
        "reason_for_withdrawal",
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
    def hospital(self):
        """Getter hospital

        Args:

        Returns:
            string: hospital value

        Usage:
            >>> hospital = self.hospital
        """
        try:
            return self.__hospital
        except AttributeError:
            return None

    @hospital.setter
    def hospital(self, hospital):
        """Setter hospital

        Args:
            hospital(string): hospital.

        Returns:

        Usage:
            >>> self.hospital = hospital
        """
        self.__hospital = hospital

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
    def start_date(self):
        """Getter start_date

        Args:

        Returns:
            string: start_date value

        Usage:
            >>> start_date = self.start_date
        """
        try:
            return self.__start_date
        except AttributeError:
            return None

    @start_date.setter
    def start_date(self, start_date):
        """Setter start_date

        Args:
            start_date(string): start_date.

        Returns:

        Usage:
            >>> self.start_date = start_date
        """
        self.__start_date = start_date

    @property
    def leave_date(self):
        """Getter leave_date

        Args:

        Returns:
            string: leave_date value

        Usage:
            >>> leave_date = self.leave_date
        """
        try:
            return self.__leave_date
        except AttributeError:
            return None

    @leave_date.setter
    def leave_date(self, leave_date):
        """Setter leave_date

        Args:
            leave_date(string): leave_date.

        Returns:

        Usage:
            >>> self.leave_date = leave_date
        """
        self.__leave_date = leave_date

    @property
    def withdrawal(self):
        """Getter withdrawal

        Args:

        Returns:
            string: withdrawal value

        Usage:
            >>> withdrawal = self.withdrawal
        """
        try:
            return self.__withdrawal
        except AttributeError:
            return None

    @withdrawal.setter
    def withdrawal(self, withdrawal):
        """Setter withdrawal

        Args:
            withdrawal(string): withdrawal.

        Returns:

        Usage:
            >>> self.withdrawal = withdrawal
        """
        self.__withdrawal = withdrawal

    @property
    def reason_for_withdrawal(self):
        """Getter reason_for_withdrawal

        Args:

        Returns:
            string: reason_for_withdrawal value

        Usage:
            >>> reason_for_withdrawal = self.reason_for_withdrawal
        """
        try:
            return self.__reason_for_withdrawal
        except AttributeError:
            return None

    @reason_for_withdrawal.setter
    def reason_for_withdrawal(self, reason_for_withdrawal):
        """Setter reason_for_withdrawal

        Args:
            reason_for_withdrawal(string): reason_for_withdrawal.

        Returns:

        Usage:
            >>> self.reason_for_withdrawal = reason_for_withdrawal
        """
        self.__reason_for_withdrawal = reason_for_withdrawal

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
        return super().get_attrs(EmployeeMedicalInsurance)

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
        return f"EmployeeMedicalInsurance('{self.employee_id}')"
