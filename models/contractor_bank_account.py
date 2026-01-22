from .base import Model


class ContractorBankAccount(Model):
    """Database table name"""

    _TABLE = "contractors_bank_accounts"

    """Database primary keys
    """
    _IDS = ["contractor_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = ["contractor_id", "bank_account_id"]

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
    def bank_account_id(self):
        """Getter bank_account_id

        Args:

        Returns:
            string: bank_account_id value

        Usage:
            >>> bank_account_id = self.bank_account_id
        """
        try:
            return self.__bank_account_id
        except AttributeError:
            return None

    @bank_account_id.setter
    def bank_account_id(self, bank_account_id):
        """Setter bank_account_id

        Args:
            bank_account_id(string): bank_account_id.

        Returns:

        Usage:
            >>> self.bank_account_id = bank_account_id
        """
        self.__bank_account_id = bank_account_id

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
        return super().get_attrs(ContractorBankAccount)

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
        return f"ContractorBankAccount('{self.contractor_id}')"
