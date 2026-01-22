from .base import Model


class ProductUnitCar(Model):
    """Database table"""

    _TABLE = "products_units_cars"

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
        "year",
        "color",
        "type",
        "economic_number",
        "stock_number",
        "cylinders",
        "doors",
        "passengers",
        "type_of_transmission",
        "fuel",
        "tank_capacity",
        "has_insurance",
        "has_circulation_card",
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
    def year(self):
        """Getter year

        Args:

        Returns:
            int: year value

        Usage:
            >>> year = self.year
        """
        try:
            return self.__year
        except AttributeError:
            return None

    @year.setter
    def year(self, year):
        """Setter year

        Args:
            year(int): year.

        Returns:

        Usage:
            >>> self.year = year
        """
        self.__year = year

    @property
    def color(self):
        """Getter color

        Args:

        Returns:
            string: name value

        Usage:
            >>> color = self.color
        """
        try:
            return self.__color
        except AttributeError:
            return None

    @color.setter
    def color(self, color):
        """Setter color

        Args:
            color(string): name.

        Returns:

        Usage:
            >>> self.color = color
        """
        self.__color = color

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
    def economic_number(self):
        """Getter economic_number

        Args:

        Returns:
            string: economic number value

        Usage:
            >>> economic_number = self.economic_number
        """
        try:
            return self.__economic_number
        except AttributeError:
            return None

    @economic_number.setter
    def economic_number(self, economic_number):
        """Setter economic_number

        Args:
            economic_number(string): economic number.

        Returns:

        Usage:
            >>> self.economic_number = economic_number
        """
        self.__economic_number = economic_number

    @property
    def stock_number(self):
        """Getter stock_number

        Args:

        Returns:
            string: economic number value

        Usage:
            >>> stock_number = self.stock_number
        """
        try:
            return self.__stock_number
        except AttributeError:
            return None

    @stock_number.setter
    def stock_number(self, stock_number):
        """Setter stock_number

        Args:
            stock_number(string): economic number.

        Returns:

        Usage:
            >>> self.stock_number = stock_number
        """
        self.__stock_number = stock_number

    @property
    def cylinders(self):
        """Getter cylinders

        Args:

        Returns:
            string: cylinders value

        Usage:
            >>> cylinders = self.cylinders
        """
        try:
            return self.__cylinders
        except AttributeError:
            return None

    @cylinders.setter
    def cylinders(self, cylinders):
        """Setter cylinders

        Args:
            cylinders(string): cylinders.

        Returns:

        Usage:
            >>> self.cylinders = cylinders
        """
        self.__cylinders = cylinders

    @property
    def doors(self):
        """Getter doors

        Args:

        Returns:
            int: doors value

        Usage:
            >>> doors = self.doors
        """
        try:
            return self.__doors
        except AttributeError:
            return None

    @doors.setter
    def doors(self, doors):
        """Setter doors

        Args:
            doors(int): doors.

        Returns:

        Usage:
            >>> self.doors = doors
        """
        self.__doors = doors

    @property
    def passengers(self):
        """Getter passengers

        Args:

        Returns:
            int: passengers value

        Usage:
            >>> passengers = self.passengers
        """
        try:
            return self.__passengers
        except AttributeError:
            return None

    @passengers.setter
    def passengers(self, passengers):
        """Setter passengers

        Args:
            passengers(int): passengers.

        Returns:

        Usage:
            >>> self.passengers = passengers
        """
        self.__passengers = passengers

    @property
    def type_of_transmission(self):
        """Getter type_of_transmission

        Args:

        Returns:
            string: type_of_transmission value

        Usage:
            >>> type_of_transmission = self.type_of_transmission
        """
        try:
            return self.__type_of_transmission
        except AttributeError:
            return None

    @type_of_transmission.setter
    def type_of_transmission(self, type_of_transmission):
        """Setter type_of_transmission

        Args:
            type_of_transmission(string): type_of_transmission.

        Returns:

        Usage:
            >>> self.type_of_transmission = type_of_transmission
        """
        self.__type_of_transmission = type_of_transmission

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
    def tank_capacity(self):
        """Getter tank_capacity

        Args:

        Returns:
            int: tank_capacity value

        Usage:
            >>> tank_capacity = self.tank_capacity
        """
        try:
            return self.__tank_capacity
        except AttributeError:
            return "active"

    @tank_capacity.setter
    def tank_capacity(self, tank_capacity):
        """Setter tank_capacity

        Args:
            tank_capacity(int): tank_capacity.

        Returns:

        Usage:
            >>> self.tank_capacity = tank_capacity
        """
        self.__tank_capacity = tank_capacity

    @property
    def has_insurance(self):
        """Getter has_insurance

        Args:

        Returns:
            bool: has_insurance value

        Usage:
            >>> has_insurance = self.has_insurance
        """
        try:
            return self.__has_insurance
        except AttributeError:
            return "active"

    @has_insurance.setter
    def has_insurance(self, has_insurance):
        """Setter has_insurance

        Args:
            has_insurance(bool): has_insurance.

        Returns:

        Usage:
            >>> self.has_insurance = has_insurance
        """
        self.__has_insurance = has_insurance

    @property
    def has_circulation_card(self):
        """Getter has_circulation_card

        Args:

        Returns:
            bool: has_circulation_card value

        Usage:
            >>> has_circulation_card = self.has_circulation_card
        """
        try:
            return self.__has_circulation_card
        except AttributeError:
            return "active"

    @has_circulation_card.setter
    def has_circulation_card(self, has_circulation_card):
        """Setter has_circulation_card

        Args:
            has_circulation_card(bool): has_circulation_card.

        Returns:

        Usage:
            >>> self.has_circulation_card = has_circulation_card
        """
        self.__has_circulation_card = has_circulation_card

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
        return super().get_attrs(ProductUnitCar)

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
        return f"ProductUnitCar('{self.unit_id}')"
