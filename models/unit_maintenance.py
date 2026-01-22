from .base import Model


class UnitMaintenance(Model):
    """Database table"""

    _TABLE = "units_maintenances"

    """Database primary keys
    """
    _IDS = ["maintenance_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "maintenance_id",
        "user_id",
        "employee_id",
        "supplier_id",
        "product_id",
        "brand_id",
        "model_id",
        "version_id",
        "unit_id",
        "code",
        "appointment_date",
        "type",
        "reason",
        "subtotal",
        "taxes",
        "total",
        "is_cars_related",
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
    def maintenance_id(self):
        """Getter maintenance_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> maintenance_id = self.maintenance_id
        """
        try:
            return self.__maintenance_id
        except AttributeError:
            return None

    @maintenance_id.setter
    def maintenance_id(self, maintenance_id):
        """Setter maintenance_id

        Args:
            maintenance_id(string): id.

        Returns:

        Usage:
            >>> self.maintenance_id = maintenance_id
        """
        self.__maintenance_id = maintenance_id

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
    def product_id(self):
        """Getter product_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> product_id = self.product_id
        """
        try:
            return self.__product_id
        except AttributeError:
            return None

    @product_id.setter
    def product_id(self, product_id):
        """Setter product_id

        Args:
            product_id(string): id.

        Returns:

        Usage:
            >>> self.product_id = product_id
        """
        self.__product_id = product_id

    @property
    def brand_id(self):
        """Getter brand_id

        Args:

        Returns:
            string: brand_id value

        Usage:
            >>> brand_id = self.brand_id
        """
        try:
            return self.__brand_id
        except AttributeError:
            return None

    @brand_id.setter
    def brand_id(self, brand_id):
        """Setter brand_id

        Args:
            brand_id(string): brand_id.

        Returns:

        Usage:
            >>> self.brand_id = brand_id
        """
        self.__brand_id = brand_id

    @property
    def model_id(self):
        """Getter model_id

        Args:

        Returns:
            string: model_id value

        Usage:
            >>> model_id = self.model_id
        """
        try:
            return self.__model_id
        except AttributeError:
            return None

    @model_id.setter
    def model_id(self, model_id):
        """Setter model_id

        Args:
            model_id(string): model_id.

        Returns:

        Usage:
            >>> self.model_id = model_id
        """
        self.__model_id = model_id

    @property
    def version_id(self):
        """Getter version_id

        Args:

        Returns:
            string: version_id value

        Usage:
            >>> version_id = self.version_id
        """
        try:
            return self.__version_id
        except AttributeError:
            return None

    @version_id.setter
    def version_id(self, version_id):
        """Setter version_id

        Args:
            version_id(string): version_id.

        Returns:

        Usage:
            >>> self.version_id = version_id
        """
        self.__version_id = version_id

    @property
    def unit_id(self):
        """Getter unit_id

        Args:

        Returns:
            string: unit_id value

        Usage:
            >>> unit_id = self.unit_id
        """
        try:
            return self.__unit_id
        except AttributeError:
            return None

    @unit_id.setter
    def unit_id(self, unit_id):
        """Setter unit_id

        Args:
            unit_id(string): unit_id.

        Returns:

        Usage:
            >>> self.unit_id = unit_id
        """
        self.__unit_id = unit_id

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
    def appointment_date(self):
        """Getter appointment_date

        Args:

        Returns:
            string: appointment_date value

        Usage:
            >>> appointment_date = self.appointment_date
        """
        try:
            return self.__appointment_date
        except AttributeError:
            return None

    @appointment_date.setter
    def appointment_date(self, appointment_date):
        """Setter appointment_date

        Args:
            appointment_date(string): appointment_date.

        Returns:

        Usage:
            >>> self.appointment_date = appointment_date
        """
        self.__appointment_date = appointment_date

    @property
    def subtotal(self):
        """Getter subtotal

        Args:

        Returns:
            double: subtotal value

        Usage:
            >>> subtotal = self.subtotal
        """
        try:
            return self.__subtotal
        except AttributeError:
            return None

    @subtotal.setter
    def subtotal(self, subtotal):
        """Setter subtotal

        Args:
            subtotal(double): subtotal.

        Returns:

        Usage:
            >>> self.subtotal = subtotal
        """
        self.__subtotal = subtotal

    @property
    def taxes(self):
        """Getter taxes

        Args:

        Returns:
            double: taxes value

        Usage:
            >>> taxes = self.taxes
        """
        try:
            return self.__taxes
        except AttributeError:
            return None

    @taxes.setter
    def taxes(self, taxes):
        """Setter taxes

        Args:
            taxes(double): taxes.

        Returns:

        Usage:
            >>> self.taxes = taxes
        """
        self.__taxes = taxes

    @property
    def total(self):
        """Getter total

        Args:

        Returns:
            double: total value

        Usage:
            >>> total = self.total
        """
        try:
            return self.__total
        except AttributeError:
            return None

    @total.setter
    def total(self, total):
        """Setter total

        Args:
            total(double): total.

        Returns:

        Usage:
            >>> self.total = total
        """
        self.__total = total

    @property
    def is_cars_related(self):
        """Getter is_cars_related

        Args:

        Returns:
            bool: is_cars_related value

        Usage:
            >>> is_cars_related = self.is_cars_related
        """
        try:
            return self.__is_cars_related
        except AttributeError:
            return None

    @is_cars_related.setter
    def is_cars_related(self, is_cars_related):
        """Setter is_cars_related

        Args:
            is_cars_related(bool): is_cars_related.

        Returns:

        Usage:
            >>> self.is_cars_related = is_cars_related
        """
        self.__is_cars_related = is_cars_related

    @property
    def notes(self):
        """Getter notes

        Args:

        Returns:
            str: notes value

        Usage:
            >>> notes = self.notes
        """
        try:
            return self.__notes
        except AttributeError:
            return False

    @notes.setter
    def notes(self, notes):
        """Setter notes

        Args:
            notes(str): notes.

        Returns:

        Usage:
            >>> self.notes = notes
        """
        self.__notes = notes

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
            return "active"

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
    def reason(self):
        """Getter reason

        Args:

        Returns:
            string: reason value

        Usage:
            >>> reason = self.reason
        """
        try:
            return self.__reason
        except AttributeError:
            return "active"

    @reason.setter
    def reason(self, reason):
        """Setter reason

        Args:
            reason(string): reason.

        Returns:

        Usage:
            >>> self.reason = reason
        """
        self.__reason = reason

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
        return super().get_attrs(UnitMaintenance)

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
        return f"UnitMaintenance('{self.maintenance_id}')"
