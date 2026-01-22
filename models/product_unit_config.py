from .base import Model


class ProductUnitConfig(Model):
    """Database table"""

    _TABLE = "products_units_notifications_configs"

    """Database primary keys
    """
    _IDS = ["unit_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "product_id",
        "unit_id",
        "per_mileage",
        "mileage",
        "per_days",
        "days",
        "per_hours",
        "hours",
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
    def unit_id(self):
        """Getter unit_id

        Args:

        Returns:
            string: id value

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
            unit_id(string): id.

        Returns:

        Usage:
            >>> self.unit_id = unit_id
        """
        self.__unit_id = unit_id

    @property
    def per_mileage(self):
        """Getter per_mileage

        Args:

        Returns:
            int: per_mileage value

        Usage:
            >>> per_mileage = self.per_mileage
        """
        try:
            return self.__per_mileage
        except AttributeError:
            return None

    @per_mileage.setter
    def per_mileage(self, per_mileage):
        """Setter per_mileage

        Args:
            per_mileage(int): per_mileage.

        Returns:

        Usage:
            >>> self.per_mileage = per_mileage
        """
        self.__per_mileage = per_mileage

    @property
    def mileage(self):
        """Getter mileage

        Args:

        Returns:
            double: mileage value

        Usage:
            >>> mileage = self.mileage
        """
        try:
            return self.__mileage
        except AttributeError:
            return None

    @mileage.setter
    def mileage(self, mileage):
        """Setter mileage

        Args:
            mileage(double): mileage.

        Returns:

        Usage:
            >>> self.mileage = mileage
        """
        self.__mileage = mileage

    @property
    def per_days(self):
        """Getter per_days

        Args:

        Returns:
            int: per_days value

        Usage:
            >>> per_days = self.per_days
        """
        try:
            return self.__per_days
        except AttributeError:
            return None

    @per_days.setter
    def per_days(self, per_days):
        """Setter per_days

        Args:
            per_days(int): per_days.

        Returns:

        Usage:
            >>> self.per_days = per_days
        """
        self.__per_days = per_days

    @property
    def days(self):
        """Getter days

        Args:

        Returns:
            string: days value

        Usage:
            >>> days = self.days
        """
        try:
            return self.__days
        except AttributeError:
            return None

    @days.setter
    def days(self, days):
        """Setter days

        Args:
            days(double): days.

        Returns:

        Usage:
            >>> self.days = days
        """
        self.__days = days

    @property
    def per_hours(self):
        """Getter per_hours

        Args:

        Returns:
            int: per_hours value

        Usage:
            >>> per_hours = self.per_hours
        """
        try:
            return self.__per_hours
        except AttributeError:
            return None

    @per_hours.setter
    def per_hours(self, per_hours):
        """Setter per_hours

        Args:
            per_hours(int): per_hours.

        Returns:

        Usage:
            >>> self.per_hours = per_hours
        """
        self.__per_hours = per_hours

    @property
    def hours(self):
        """Getter hours

        Args:

        Returns:
            double: hours value

        Usage:
            >>> hours = self.hours
        """
        try:
            return self.__hours
        except AttributeError:
            return None

    @hours.setter
    def hours(self, hours):
        """Setter hours

        Args:
            hours(double): hours.

        Returns:

        Usage:
            >>> self.hours = hours
        """
        self.__hours = hours

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
        return super().get_attrs(ProductUnitConfig)

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
        return f"ProductUnitConfig('{self.unit_id}')"
