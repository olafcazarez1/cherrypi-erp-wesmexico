from .base import Model


class EmployeeRelative(Model):
    """Database table names"""

    _TABLE = "employees_relatives"

    """Database primary keys
    """
    _IDS = ["employee_id", "relative_id"]

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
        "relative_id",
        "names",
        "first_last_name",
        "second_last_name",
        "cell_phone",
        "relation",
        "emergency",
        "status",
    ]

    _ALIAS = {"full_name": 'CONCAT(`names`, " ", `first_last_name`, " ", `second_last_name`)'}

    """Fields should not been overrided for set_attrs method
    """
    _RESTRICTED = ["full_name", "created_at", "updated_at"]

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
    def relative_id(self):
        """Getter relative_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> relative_id = self.relative_id
        """
        try:
            return self.__relative_id
        except AttributeError:
            return None

    @relative_id.setter
    def relative_id(self, relative_id):
        """Setter relative_id

        Args:
            relative_id(string): id.

        Returns:

        Usage:
            >>> self.relative_id = relative_id
        """
        self.__relative_id = relative_id

    @property
    def full_name(self):
        """Getter full_name

        Args:

        Returns:
            string: full_name value

        Usage:
            >>> full_name = self.full_name
        """
        try:
            return self.__full_name
        except AttributeError:
            return None

    @full_name.setter
    def full_name(self, full_name):
        """Setter full_name

        Args:
            full_name(string): full_name.

        Returns:

        Usage:
            >>> self.full_name = full_name
        """
        self.__full_name = full_name

    @property
    def names(self):
        """Getter names

        Args:

        Returns:
            string: names value

        Usage:
            >>> names = self.names
        """
        try:
            return self.__names
        except AttributeError:
            return None

    @names.setter
    def names(self, names):
        """Setter names

        Args:
            names(string): names.

        Returns:

        Usage:
            >>> self.names = names
        """
        self.__names = names

    @property
    def first_last_name(self):
        """Getter first_last_name

        Args:

        Returns:
            string: first_last_name value

        Usage:
            >>> first_last_name = self.first_last_name
        """
        try:
            return self.__first_last_name
        except AttributeError:
            return "active"

    @first_last_name.setter
    def first_last_name(self, first_last_name):
        """Setter first_last_name

        Args:
            first_last_name(string): first_last_name.

        Returns:

        Usage:
            >>> self.first_last_name = first_last_name
        """
        self.__first_last_name = first_last_name

    @property
    def second_last_name(self):
        """Getter second_last_name

        Args:

        Returns:
            string: second_last_name value

        Usage:
            >>> second_last_name = self.second_last_name
        """
        try:
            return self.__second_last_name
        except AttributeError:
            return "active"

    @second_last_name.setter
    def second_last_name(self, second_last_name):
        """Setter second_last_name

        Args:
            second_last_name(string): second_last_name.

        Returns:

        Usage:
            >>> self.second_last_name = second_last_name
        """
        self.__second_last_name = second_last_name

    @property
    def cell_phone(self):
        """Getter cell_phone

        Args:

        Returns:
            string: cell_phone value

        Usage:
            >>> cell_phone = self.cell_phone
        """
        try:
            return self.__cell_phone
        except AttributeError:
            return ""

    @cell_phone.setter
    def cell_phone(self, cell_phone):
        """Setter cell_phone

        Args:
            cell_phone(string): cell_phone.

        Returns:

        Usage:
            >>> self.cell_phone = cell_phone
        """
        self.__cell_phone = cell_phone

    @property
    def relation(self):
        """Getter relation

        Args:

        Returns:
            string: relation value

        Usage:
            >>> relation = self.relation
        """
        try:
            return self.__relation
        except AttributeError:
            return "active"

    @relation.setter
    def relation(self, relation):
        """Setter relation

        Args:
            relation(string): relation.

        Returns:

        Usage:
            >>> self.relation = relation
        """
        self.__relation = relation

    @property
    def emergency(self):
        """Getter emergency

        Args:

        Returns:
            string: emergency value

        Usage:
            >>> emergency = self.emergency
        """
        try:
            return self.__emergency
        except AttributeError:
            return ""

    @emergency.setter
    def emergency(self, emergency):
        """Setter emergency

        Args:
            emergency(string): emergency.

        Returns:

        Usage:
            >>> self.emergency = emergency
        """
        self.__emergency = emergency

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
        return super().get_attrs(EmployeeRelative)

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
        return f"EmployeeRelative('{self.relative_id}')"
