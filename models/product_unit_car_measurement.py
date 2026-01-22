from .base import Model


class ProductUnitCarMeasurement(Model):
    """Database table"""

    _TABLE = "products_units_cars_measurements"

    """Database primary keys
    """
    _IDS = ["measurement_id"]

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
        "measurement_id",
        "source",
        "reference",
        "previous_mileage",
        "mileage",
        "fuel",
        "hours",
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
    def measurement_id(self):
        """Getter measurement_id

        Args:

        Returns:
            string: measurement_id value

        Usage:
            >>> measurement_id = self.measurement_id
        """
        try:
            return self.__measurement_id
        except AttributeError:
            return None

    @measurement_id.setter
    def measurement_id(self, measurement_id):
        """Setter measurement_id

        Args:
            measurement_id(string): measurement_id.

        Returns:

        Usage:
            >>> self.measurement_id = measurement_id
        """
        self.__measurement_id = measurement_id

    @property
    def source(self):
        """Getter source

        Args:

        Returns:
            string: source value

        Usage:
            >>> source = self.source
        """
        try:
            return self.__source
        except AttributeError:
            return None

    @source.setter
    def source(self, source):
        """Setter source

        Args:
            source(string): source.

        Returns:

        Usage:
            >>> self.source = source
        """
        self.__source = source

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
    def mileage(self):
        """Getter mileage

        Args:

        Returns:
            double: id value

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
            mileage(double): id.

        Returns:

        Usage:
            >>> self.mileage = mileage
        """
        self.__mileage = mileage

    @property
    def previous_mileage(self):
        """Getter previous_mileage

        Args:

        Returns:
            double: id value

        Usage:
            >>> previous_mileage = self.previous_mileage
        """
        try:
            return self.__previous_mileage
        except AttributeError:
            return None

    @previous_mileage.setter
    def previous_mileage(self, previous_mileage):
        """Setter previous_mileage

        Args:
            previous_mileage(double): previous mileage.

        Returns:

        Usage:
            >>> self.previous_mileage = previous_mileage
        """
        self.__previous_mileage = previous_mileage

    @property
    def fuel(self):
        """Getter fuel

        Args:

        Returns:
            string: fuel value

        Usage:
            >>> fuel = self.fuel
        """
        try:
            return self.__fuel
        except AttributeError:
            return None

    @fuel.setter
    def fuel(self, fuel):
        """Setter fuel

        Args:
            fuel(string): fuel.

        Returns:

        Usage:
            >>> self.fuel = fuel
        """
        self.__fuel = fuel

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
            return None

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
        return super().get_attrs(ProductUnitCarMeasurement)

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
        return f"ProductUnitCarMeasurement('{self.unit_id}')"
