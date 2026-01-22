from .base import Model


class BranchOffice(Model):
    """Database table name"""

    _TABLE = "branch_offices"

    """Database primary keys
    """
    _IDS = ["company_id", "branch_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "company_id",
        "branch_id",
        "code",
        "type",
        "name",
        # 'serie',
        "address_street",
        "address_external_number",
        "address_internal_number",
        "neighborhood",
        "state_id",
        "municipality_id",
        "locality_id",
        "zip",
        "phone",
        "timezone",
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

    # @property
    # def serie(self):
    # 	"""Getter serie

    # 	Args:

    # 	Returns:
    # 		string: serie value

    # 	Usage:
    # 		>>> serie = self.serie
    # 	"""
    # 	try:
    # 		return self.__serie
    # 	except AttributeError:
    # 		return None

    # @serie.setter
    # def serie(self, serie):
    # 	"""Setter serie

    # 	Args:
    # 		serie(string): serie.

    # 	Returns:

    # 	Usage:
    # 		>>> self.serie = serie
    # 	"""
    # 	self.__serie = serie

    @property
    def address_street(self):
        """Getter address_street

        Args:

        Returns:
                string: address_street value

        Usage:
                >>> address_street = self.address_street
        """
        try:
            return self.__address_street
        except AttributeError:
            return None

    @address_street.setter
    def address_street(self, address_street):
        """Setter address_street

        Args:
                address_street(string): address_street.

        Returns:

        Usage:
                >>> self.address_street = address_street
        """
        self.__address_street = address_street

    @property
    def address_external_number(self):
        """Getter address_external_number

        Args:

        Returns:
                string: address_external_number value

        Usage:
                >>> address_external_number = self.address_external_number
        """
        try:
            return self.__address_external_number
        except AttributeError:
            return ""

    @address_external_number.setter
    def address_external_number(self, address_external_number):
        """Setter address_external_number

        Args:
                address_external_number(string): address_external_number.

        Returns:

        Usage:
                >>> self.address_external_number = address_external_number
        """
        self.__address_external_number = address_external_number

    @property
    def address_internal_number(self):
        """Getter address_internal_number

        Args:

        Returns:
                string: address_internal_number value

        Usage:
                >>> address_internal_number = self.address_internal_number
        """
        try:
            return self.__address_internal_number
        except AttributeError:
            return ""

    @address_internal_number.setter
    def address_internal_number(self, address_internal_number):
        """Setter address_internal_number

        Args:
                address_internal_number(string): address_internal_number.

        Returns:

        Usage:
                >>> self.address_internal_number = address_internal_number
        """
        self.__address_internal_number = address_internal_number

    @property
    def neighborhood(self):
        """Getter neighborhood

        Args:

        Returns:
                string: neighborhood value

        Usage:
                >>> neighborhood = self.neighborhood
        """
        try:
            return self.__neighborhood
        except AttributeError:
            return ""

    @neighborhood.setter
    def neighborhood(self, neighborhood):
        """Setter neighborhood

        Args:
                neighborhood(string): neighborhood.

        Returns:

        Usage:
                >>> self.neighborhood = neighborhood
        """
        self.__neighborhood = neighborhood

    @property
    def state_id(self):
        """Getter state_id

        Args:

        Returns:
                string: state id value

        Usage:
                >>> state_id = self.state_id
        """
        try:
            return self.__state_id
        except AttributeError:
            return None

    @state_id.setter
    def state_id(self, state_id):
        """Setter state_id

        Args:
                state_id(string): state id.

        Returns:

        Usage:
                >>> self.state_id = state_id
        """
        self.__state_id = state_id

    @property
    def municipality_id(self):
        """Getter municipality_id

        Args:

        Returns:
                string: municipality id value

        Usage:
                >>> municipality_id = self.municipality_id
        """
        try:
            return self.__municipality_id
        except AttributeError:
            return None

    @municipality_id.setter
    def municipality_id(self, municipality_id):
        """Setter municipality_id

        Args:
                municipality_id(string): municipality id.

        Returns:

        Usage:
                >>> self.municipality_id = municipality_id
        """
        self.__municipality_id = municipality_id

    @property
    def locality_id(self):
        """Getter locality_id

        Args:

        Returns:
                string: locality id value

        Usage:
                >>> locality_id = self.locality_id
        """
        try:
            return self.__locality_id
        except AttributeError:
            return None

    @locality_id.setter
    def locality_id(self, locality_id):
        """Setter locality_id

        Args:
                locality_id(string): locality id.

        Returns:

        Usage:
                >>> self.locality_id = locality_id
        """
        self.__locality_id = locality_id

    @property
    def zip(self):
        """Getter zip

        Args:

        Returns:
                string: zip value

        Usage:
                >>> zip = self.zip
        """
        try:
            return self.__zip
        except AttributeError:
            return 0

    @zip.setter
    def zip(self, zip):
        """Setter zip

        Args:
                zip(string): zip.

        Returns:

        Usage:
                >>> self.zip = zip
        """
        self.__zip = zip

    @property
    def phone(self):
        """Getter phone

        Args:

        Returns:
                string: phone value

        Usage:
                >>> phone = self.phone
        """
        try:
            return self.__phone
        except AttributeError:
            return ""

    @phone.setter
    def phone(self, phone):
        """Setter phone

        Args:
                phone(string): phone.

        Returns:

        Usage:
                >>> self.phone = phone
        """
        self.__phone = phone

    @property
    def timezone(self):
        """Getter timezone

        Args:

        Returns:
                string: timezone value

        Usage:
                >>> timezone = self.timezone
        """
        try:
            return self.__timezone
        except AttributeError:
            return ""

    @timezone.setter
    def timezone(self, timezone):
        """Setter timezone

        Args:
                timezone(string): timezone.

        Returns:

        Usage:
                >>> self.timezone = timezone
        """
        self.__timezone = timezone

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
        return super().get_attrs(BranchOffice)

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
        return f"BranchOffice('{self.branch_id}')"
