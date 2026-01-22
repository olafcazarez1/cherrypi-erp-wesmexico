from .base import Model


class ContractorContact(Model):
    """Database table name"""

    _TABLE = "contractors_contacts"

    """Database primary keys
    """
    _IDS = ["contractor_id", "contact_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "contractor_id",
        "contact_id",
        "code",
        "name",
        "position",
        "email",
        "phone",
        "extension",
        "cell_phone",
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
    def contractor_id(self):
        """Getter contractor_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> contractor_id = self.contractor_id
        """
        try:
            return self.__contractor_id
        except AttributeError:
            return None

    @contractor_id.setter
    def contractor_id(self, contractor_id):
        """Setter contractor_id

        Args:
            contractor_id(string): id.

        Returns:

        Usage:
            >>> self.contractor_id = contractor_id
        """
        self.__contractor_id = contractor_id

    @property
    def contact_id(self):
        """Getter contact_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> contact_id = self.contact_id
        """
        try:
            return self.__contact_id
        except AttributeError:
            return None

    @contact_id.setter
    def contact_id(self, contact_id):
        """Setter contact_id

        Args:
            contact_id(string): id.

        Returns:

        Usage:
            >>> self.contact_id = contact_id
        """
        self.__contact_id = contact_id

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
    def position(self):
        """Getter position

        Args:

        Returns:
            string: position value

        Usage:
            >>> position = self.position
        """
        try:
            return self.__position
        except AttributeError:
            return "active"

    @position.setter
    def position(self, position):
        """Setter position

        Args:
            position(string): position.

        Returns:

        Usage:
            >>> self.position = position
        """
        self.__position = position

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
            return "active"

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
    def extension(self):
        """Getter extension

        Args:

        Returns:
            string: extension value

        Usage:
            >>> extension = self.extension
        """
        try:
            return self.__extension
        except AttributeError:
            return "active"

    @extension.setter
    def extension(self, extension):
        """Setter extension

        Args:
            extension(string): extension.

        Returns:

        Usage:
            >>> self.extension = extension
        """
        self.__extension = extension

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
        return super().get_attrs(ContractorContact)

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
        return f"ContractorContact('{self.contractor_id}')"
