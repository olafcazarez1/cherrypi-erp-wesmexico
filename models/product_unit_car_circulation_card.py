from .base import Model


class ProductUnitCarCirculationCard(Model):
    """Database table"""

    _TABLE = "products_units_cars_circulation_card"

    """Database primary keys
    """
    _IDS = ["product_id", "unit_id"]

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
        "register_id",
        "legal_name",
        "total",
        "payment_concept",
        "document",
        "expedition_date",
        "expiration_date",
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
    def register_id(self):
        """Getter register_id

        Args:

        Returns:
            string: register_id value

        Usage:
            >>> register_id = self.register_id
        """
        try:
            return self.__register_id
        except AttributeError:
            return None

    @register_id.setter
    def register_id(self, register_id):
        """Setter register_id

        Args:
            register_id(string): register_id.

        Returns:

        Usage:
            >>> self.register_id = register_id
        """
        self.__register_id = register_id

    @property
    def legal_name(self):
        """Getter legal_name

        Args:

        Returns:
            string: legal_name value

        Usage:
            >>> legal_name = self.legal_name
        """
        try:
            return self.__legal_name
        except AttributeError:
            return None

    @legal_name.setter
    def legal_name(self, legal_name):
        """Setter legal_name

        Args:
            legal_name(string): legal_name.

        Returns:

        Usage:
            >>> self.legal_name = legal_name
        """
        self.__legal_name = legal_name

    @property
    def total(self):
        """Getter total

        Args:

        Returns:
            double: id value

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
            total(double): id.

        Returns:

        Usage:
            >>> self.total = total
        """
        self.__total = total

    @property
    def payment_concept(self):
        """Getter payment_concept

        Args:

        Returns:
            string: payment_concept value

        Usage:
            >>> payment_concept = self.payment_concept
        """
        try:
            return self.__payment_concept
        except AttributeError:
            return None

    @payment_concept.setter
    def payment_concept(self, payment_concept):
        """Setter payment_concept

        Args:
            payment_concept(string): payment_concept.

        Returns:

        Usage:
            >>> self.payment_concept = payment_concept
        """
        self.__payment_concept = payment_concept

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
        return super().get_attrs(ProductUnitCarCirculationCard)

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
        return f"ProductUnitCarCirculationCard('{self.unit_id}')"
