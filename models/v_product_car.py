from .base import Model


class vProductCar(Model):
    """Database table"""

    _TABLE = "v_products_cars"

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
        "company_id",
        "department_id",
        "brand_id",
        "model_id",
        "version_id",
        "code",
        "serie",
        "reference",
        "uid",
        "num_uid",
        "description",
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
    def version_id(self):
        """Getter version_id

        Args:

        Returns:
            string: id value

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
            version_id(string): id.

        Returns:

        Usage:
            >>> self.version_id = version_id
        """
        self.__version_id = version_id

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
    def serie(self):
        """Getter serie

        Args:

        Returns:
            string: serie value

        Usage:
            >>> serie = self.serie
        """
        try:
            return self.__serie
        except AttributeError:
            return None

    @serie.setter
    def serie(self, serie):
        """Setter serie

        Args:
            serie(string): serie.

        Returns:

        Usage:
            >>> self.serie = serie
        """
        self.__serie = serie

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
    def uid(self):
        """Getter uid

        Args:

        Returns:
            string: uid value

        Usage:
            >>> uid = self.uid
        """
        try:
            return self.__uid
        except AttributeError:
            return None

    @uid.setter
    def uid(self, uid):
        """Setter uid

        Args:
            uid(string): uid.

        Returns:

        Usage:
            >>> self.uid = uid
        """
        self.__uid = uid

    @property
    def num_uid(self):
        """Getter num_uid

        Args:

        Returns:
            string: num_uid value

        Usage:
            >>> num_uid = self.num_uid
        """
        try:
            return self.__num_uid
        except AttributeError:
            return None

    @num_uid.setter
    def num_uid(self, num_uid):
        """Setter num_uid

        Args:
            num_uid(string): num_uid.

        Returns:

        Usage:
            >>> self.num_uid = num_uid
        """
        self.__num_uid = num_uid

    @property
    def description(self):
        """Getter description

        Args:

        Returns:
            string: description value

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
            description(string): description.

        Returns:

        Usage:
            >>> self.description = description
        """
        self.__description = description

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
        return super().get_attrs(vProductCar)

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__diccars)
        return newone

    def __repr__(self):
        """Built-in function used to return the object representation

        Args:
            None

        Returns:
            str: A string with the object representation
        """
        return f"vProductCar('{self.unit_id}"
