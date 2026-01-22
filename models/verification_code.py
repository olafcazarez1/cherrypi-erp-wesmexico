import uuid

from datetime import datetime
from .base import Model


class VerificationCode(Model):
    """Database table name"""

    _TABLE = "verification_codes"

    """Database primary keys
    """
    _IDS = ["secure_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = ["user_id", "secure_id"]

    """Fields should not been overrided for set_attrs method
    """
    _RESTRICTED = ["created_at", "updated_at"]

    """While the global search index is available on this fields the global
    search is going to work for q parameter in filter method
    """
    _SEARCH_INDEX = [
        "secure_id" "user_id",
    ]

    """Filter limit default (Used in filters())
    """
    _FILTER_LIMIT_DEFAULT = 50

    """Maximum limit value allowed (Used in filters())
    """
    _FILTER_LIMIT_MAX = 500

    @property
    def secure_id(self):
        """Getter secure_id

        Args:

        Returns:
            string: secure_id value

        Usage:
            >>> secure_id = self.secure_id
        """
        try:
            return self.__secure_id
        except AttributeError:
            return None

    @secure_id.setter
    def secure_id(self, secure_id):
        """Setter secure_id

        Args:
            secure_id(string): secure_id.

        Returns:

        Usage:
            >>> self.secure_id = secure_id
        """
        self.__secure_id = secure_id

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

    @classmethod
    def generate(cls, reference):
        code = VerificationCode()
        code.secure_id = str(uuid.uuid4())
        code.user_id = reference
        code.created_at = datetime.utcnow()
        code.updated_at = datetime.utcnow()
        code.insert()
        return code.secure_id

    def get_attrs(self):
        """Get the list of properties that belongs to this class

        Returns:
            list: List of attributes in the Model
        """
        return super().get_attrs(VerificationCode)

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
        return f"VerificationCode('{self.secure_id}')"
