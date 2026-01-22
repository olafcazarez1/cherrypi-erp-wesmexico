from .base import Model

# from .branch_office import BranchOffice
# from .branch_office_user import BranchOfficeUser


class User(Model):
    """Database table name"""

    _TABLE = "users"

    """Database primary keys
    """
    _IDS = ["user_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = ["email"]

    """Required files for INSERT statement
    """
    _REQUIRED = ["user_id", "name", "email", "type", "is_verified"]

    """Fields should not been overrided for set_attrs method
    """
    _RESTRICTED = ["created_at", "updated_at"]

    """While the global search index is available on this fields the global
    search is going to work for q parameter in filter method
    """
    _SEARCH_INDEX = ["user_id", "email"]

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
    def user_id(self):
        """Getter user_id

        Args:

        Returns:
            string: scholarship id value

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
            user_id(string): scholarship id.

        Returns:

        Usage:
            >>> self.user_id = user_id
        """
        self.__user_id = user_id

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
            return None

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
    def password(self):
        """Getter password

        Args:

        Returns:
            string: password value

        Usage:
            >>> password = self.password
        """
        try:
            return self.__password
        except AttributeError:
            return None

    @password.setter
    def password(self, password):
        """Setter password

        Args:
            password(string): password.

        Returns:

        Usage:
            >>> self.password = password
        """
        self.__password = password

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
    def is_verified(self):
        """Getter is_verified

        Args:

        Returns:
            bool: is_verified value

        Usage:
            >>> is_verified = self.is_verified
        """
        try:
            return self.__is_verified
        except AttributeError:
            return False

    @is_verified.setter
    def is_verified(self, is_verified):
        """Setter is_verified

        Args:
            is_verified(bool): is_verified.

        Returns:

        Usage:
            >>> self.is_verified = is_verified
        """
        self.__is_verified = is_verified

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

    # def get_branches(self, only_ids=False):
    #     conn = self.get_connection()
    #     result = BranchOfficeUser().where({"user_id": self.user_id}, {"status": "active"}).all(conn=conn)

    #     branches = []
    #     for item in result.all():
    #         if only_ids:
    #             branches.append(item.branch_id)
    #             continue

    #         branch = BranchOffice().where({"branch_id": item.branch_id}).one_or_none(conn=conn)
    #         m_data = branch.as_dict()
    #         m_data.update(item.as_dict())
    #         branches.append(m_data)

    #     return branches

    def get_attrs(branchlf) -> list:
        """Get the list User's properties that belongs to this class

        Returns:
            list: List of attributes in the Model
        """
        return super().get_attrs(User)

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
        return f"User('{self.user_id}')"
