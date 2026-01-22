from .base import Model


class ProductAssignment(Model):
    """Database table"""

    _TABLE = "products_assignments"

    """Database primary keys
    """
    _IDS = ["assignment_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "assignment_id",
        "user_id",
        # "assigned_by",
        "company_id",
        "branch_id",
        "warehouse_id",
        "employee_id",
        "department_id",
        "work_area_id",
        "code",
        "type",
        "transaction_date",
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
    def user_id(self):
        """Getter user_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> user_id = self.user_id
        """
        try:
            return self.__user_id
        except AttributeError:
            return None

    @user_id.setter
    def user_id(self, user_id):
        """Setter user_id

        Args:
                user_id(string): id.

        Returns:

        Usage:
                >>> self.user_id = user_id
        """
        self.__user_id = user_id

    #     @property
    #     def assigned_by(self):
    #         """Getter assigned_by

    #         Args:

    #         Returns:
    #                 string: id value

    #         Usage:
    #                 >>> assigned_by = self.assigned_by
    #         """
    #         try:
    #             return self.__assigned_by
    #         except AttributeError:
    #             return None

    #     @assigned_by.setter
    #     def assigned_by(self, assigned_by):
    #         """Setter assigned_by

    #         Args:
    #                 assigned_by(string): id.

    #         Returns:

    #         Usage:
    #                 >>> self.assigned_by = assigned_by
    #         """
    #         self.__assigned_by = assigned_by

    @property
    def company_id(self):
        """Getter company_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> company_id = self.company_id
        """
        try:
            return self.__company_id
        except AttributeError:
            return None

    @company_id.setter
    def company_id(self, company_id):
        """Setter company_id

        Args:
                company_id(string): id.

        Returns:

        Usage:
                >>> self.company_id = company_id
        """
        self.__company_id = company_id

    @property
    def branch_id(self):
        """Getter branch_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> branch_id = self.branch_id
        """
        try:
            return self.__branch_id
        except AttributeError:
            return None

    @branch_id.setter
    def branch_id(self, branch_id):
        """Setter branch_id

        Args:
                branch_id(string): id.

        Returns:

        Usage:
                >>> self.branch_id = branch_id
        """
        self.__branch_id = branch_id

    @property
    def warehouse_id(self):
        """Getter warehouse_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> warehouse_id = self.warehouse_id
        """
        try:
            return self.__warehouse_id
        except AttributeError:
            return None

    @warehouse_id.setter
    def warehouse_id(self, warehouse_id):
        """Setter warehouse_id

        Args:
                warehouse_id(string): id.

        Returns:

        Usage:
                >>> self.warehouse_id = warehouse_id
        """
        self.__warehouse_id = warehouse_id

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
    def department_id(self):
        """Getter department_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> department_id = self.department_id
        """
        try:
            return self.__department_id
        except AttributeError:
            return None

    @department_id.setter
    def department_id(self, department_id):
        """Setter department_id

        Args:
                department_id(string): id.

        Returns:

        Usage:
                >>> self.department_id = department_id
        """
        self.__department_id = department_id

    @property
    def work_area_id(self):
        """Getter work_area_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> work_area_id = self.work_area_id
        """
        try:
            return self.__work_area_id
        except AttributeError:
            return None

    @work_area_id.setter
    def work_area_id(self, work_area_id):
        """Setter work_area_id

        Args:
                work_area_id(string): id.

        Returns:

        Usage:
                >>> self.work_area_id = work_area_id
        """
        self.__work_area_id = work_area_id

    @property
    def code(self):
        """Getter code

        Args:

        Returns:
                string: code value

        Usage:
                >>> code = self.code
        """
        try:
            return self.__code
        except AttributeError:
            return None

    @code.setter
    def code(self, code):
        """Setter code

        Args:
                code(string): code.

        Returns:

        Usage:
                >>> self.code = code
        """
        self.__code = code

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
    def transaction_date(self):
        """Getter transaction_date

        Args:

        Returns:
                string: transaction_date value

        Usage:
                >>> transaction_date = self.transaction_date
        """
        try:
            return self.__transaction_date
        except AttributeError:
            return None

    @transaction_date.setter
    def transaction_date(self, transaction_date):
        """Setter transaction_date

        Args:
                transaction_date(string): transaction_date.

        Returns:

        Usage:
                >>> self.transaction_date = transaction_date
        """
        self.__transaction_date = transaction_date

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
        return super().get_attrs(ProductAssignment)

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
        return f"ProductAssignment('{self.assignment_id}')"
