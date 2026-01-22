from .base import Model


class Product(Model):
    """Database table name"""

    _TABLE = "products"

    """Database primary keys
    """
    _IDS = ["product_id"]

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
        "brand_id",
        "model_id",
        "category_id",
        "subcategory_id",
        "external_reference",
        "code",
        "name",
        "short_name",
        "description",
        "image",
        "currency",
        "type",
        "is_imported",
        "has_units",
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
    def brand_id(self):
        """Getter brand_id

        Args:

        Returns:
            string: id value

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
            brand_id(string): id.

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
            string: id value

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
            model_id(string): id.

        Returns:

        Usage:
            >>> self.model_id = model_id
        """
        self.__model_id = model_id

    @property
    def category_id(self):
        """Getter category_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> category_id = self.category_id
        """
        try:
            return self.__category_id
        except AttributeError:
            return None

    @category_id.setter
    def category_id(self, category_id):
        """Setter category_id

        Args:
            category_id(string): id.

        Returns:

        Usage:
            >>> self.category_id = category_id
        """
        self.__category_id = category_id

    @property
    def subcategory_id(self):
        """Getter subcategory_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> subcategory_id = self.subcategory_id
        """
        try:
            return self.__subcategory_id
        except AttributeError:
            return None

    @subcategory_id.setter
    def subcategory_id(self, subcategory_id):
        """Setter subcategory_id

        Args:
            subcategory_id(string): id.

        Returns:

        Usage:
            >>> self.subcategory_id = subcategory_id
        """
        self.__subcategory_id = subcategory_id

    @property
    def external_reference(self):
        """Getter external_reference

        Args:

        Returns:
            string: id value

        Usage:
            >>> external_reference = self.external_reference
        """
        try:
            return self.__external_reference
        except AttributeError:
            return None

    @external_reference.setter
    def external_reference(self, external_reference):
        """Setter external_reference

        Args:
            external_reference(string): id.

        Returns:

        Usage:
            >>> self.external_reference = external_reference
        """
        self.__external_reference = external_reference

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
    def name(self):
        """Getter name

        Args:

        Returns:
            string: name value

        Usage:
            >>> name = self.name
        """
        try:
            return self.__name
        except AttributeError:
            return None

    @name.setter
    def name(self, name):
        """Setter name

        Args:
            name(string): name.

        Returns:

        Usage:
            >>> self.name = name
        """
        self.__name = name

    @property
    def short_name(self):
        """Getter short_name

        Args:

        Returns:
            string: short_name value

        Usage:
            >>> short_name = self.short_name
        """
        try:
            return self.__short_name
        except AttributeError:
            return None

    @short_name.setter
    def short_name(self, short_name):
        """Setter short_name

        Args:
            short_name(string): short_name.

        Returns:

        Usage:
            >>> self.short_name = short_name
        """
        self.__short_name = short_name

    @property
    def description(self):
        """Getter description

        Args:

        Returns:
            string: id value

        Usage:
            >>> description = self.description
        """
        try:
            return self.__description
        except AttributeError:
            return None

    @description.setter
    def description(self, description):
        """Setter description

        Args:
            description(string): id.

        Returns:

        Usage:
            >>> self.description = description
        """
        self.__description = description

    @property
    def image(self):
        """Getter image

        Args:

        Returns:
            string: id value

        Usage:
            >>> image = self.image
        """
        try:
            return self.__image
        except AttributeError:
            return None

    @image.setter
    def image(self, image):
        """Setter image

        Args:
            image(string): id.

        Returns:

        Usage:
            >>> self.image = image
        """
        self.__image = image

    @property
    def currency(self):
        """Getter currency

        Args:

        Returns:
            string: currency value

        Usage:
            >>> currency = self.currency
        """
        try:
            return self.__currency
        except AttributeError:
            return None

    @currency.setter
    def currency(self, currency):
        """Setter currency

        Args:
            currency(string): currency.

        Returns:

        Usage:
            >>> self.currency = currency
        """
        self.__currency = currency

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
    def is_imported(self):
        """Getter is_imported

        Args:

        Returns:
            bool: is_imported value

        Usage:
            >>> is_imported = self.is_imported
        """
        try:
            return self.__is_imported
        except AttributeError:
            return False

    @is_imported.setter
    def is_imported(self, is_imported):
        """Setter is_imported

        Args:
            is_imported(bool): is_imported.

        Returns:

        Usage:
            >>> self.is_imported = is_imported
        """
        self.__is_imported = is_imported

    @property
    def has_units(self):
        """Getter has_units

        Args:

        Returns:
            bool: has_units value

        Usage:
            >>> has_units = self.has_units
        """
        try:
            return self.__has_units
        except AttributeError:
            return False

    @has_units.setter
    def has_units(self, has_units):
        """Setter has_units

        Args:
            has_units(bool): has_units.

        Returns:

        Usage:
            >>> self.has_units = has_units
        """
        self.__has_units = has_units

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
        return super().get_attrs(Product)

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
        return f"Product('{self.product_id}')"
