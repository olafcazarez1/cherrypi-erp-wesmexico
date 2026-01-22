from .base import Model


class Supplier(Model):
    """Database table name"""

    _TABLE = "suppliers"

    """Database primary keys
    """
    _IDS = ["supplier_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "supplier_id",
        "category_id",
        "code",
        "legal_name",
        "trade_name",
        "address_street",
        "address_external_number",
        "address_internal_number",
        "neighborhood",
        "state_id",
        "municipality_id",
        "locality_id",
        "zip",
        "taxpayer_id",
        "tax_regime_id",
        "email",
        "phone",
        "cell_phone",
        "references",
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
    def trade_name(self):
        """Getter trade_name

        Args:

        Returns:
                string: trade_name value

        Usage:
                >>> trade_name = self.trade_name
        """
        try:
            return self.__trade_name
        except AttributeError:
            return None

    @trade_name.setter
    def trade_name(self, trade_name):
        """Setter trade_name

        Args:
                trade_name(string): trade_name.

        Returns:

        Usage:
                >>> self.trade_name = trade_name
        """
        self.__trade_name = trade_name

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
    def taxpayer_id(self):
        """Getter taxpayer_id

        Args:

        Returns:
                string: taxpayer_id value

        Usage:
                >>> taxpayer_id = self.taxpayer_id
        """
        try:
            return self.__taxpayer_id
        except AttributeError:
            return ""

    @taxpayer_id.setter
    def taxpayer_id(self, taxpayer_id):
        """Setter taxpayer_id

        Args:
                taxpayer_id(string): taxpayer_id.

        Returns:

        Usage:
                >>> self.taxpayer_id = taxpayer_id
        """
        self.__taxpayer_id = taxpayer_id

    @property
    def tax_regime_id(self):
        """Getter tax_regime_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> tax_regime_id = self.tax_regime_id
        """
        try:
            return self.__tax_regime_id
        except AttributeError:
            return None

    @tax_regime_id.setter
    def tax_regime_id(self, tax_regime_id):
        """Setter tax_regime_id

        Args:
                tax_regime_id(string): id.

        Returns:

        Usage:
                >>> self.tax_regime_id = tax_regime_id
        """
        self.__tax_regime_id = tax_regime_id

    @property
    def email(self):
        """Getter email

        Args:

        Returns:
                string: email value

        Usage:
                >>> email = self.email
        """
        try:
            return self.__email
        except AttributeError:
            return ""

    @email.setter
    def email(self, email):
        """Setter email

        Args:
                email(string): email.

        Returns:

        Usage:
                >>> self.email = email
        """
        self.__email = email

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
    def references(self):
        """Getter references

        Args:

        Returns:
                string: references value

        Usage:
                >>> references = self.references
        """
        try:
            return self.__references
        except AttributeError:
            return ""

    @references.setter
    def references(self, references):
        """Setter references

        Args:
                references(string): references.

        Returns:

        Usage:
                >>> self.references = references
        """
        self.__references = references

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
        return super().get_attrs(Supplier)

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
        return f"Supplier('{self.supplier_id}')"
