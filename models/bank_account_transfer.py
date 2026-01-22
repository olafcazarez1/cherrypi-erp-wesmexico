from .base import Model


class BankAccountTransfer(Model):
    """Database table"""

    _TABLE = "bank_accounts_transfers"

    """Database primary keys
    """
    _IDS = ["transfer_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "relation_id",
        "relation_type",
        "user_id",
        "transfer_id",
        "from_account_id",
        "to_account_id",
        "code",
        "amount",
        "transaction_date",
        "notes",
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
    def transfer_id(self):
        """Getter transfer_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> transfer_id = self.transfer_id
        """
        try:
            return self.__transfer_id
        except AttributeError:
            return None

    @transfer_id.setter
    def transfer_id(self, transfer_id):
        """Setter transfer_id

        Args:
            transfer_id(string): id.

        Returns:

        Usage:
            >>> self.transfer_id = transfer_id
        """
        self.__transfer_id = transfer_id

    @property
    def from_account_id(self):
        """Getter from_account_id

        Args:

        Returns:
            double: id value

        Usage:
            >>> from_account_id = self.from_account_id
        """
        try:
            return self.__from_account_id
        except AttributeError:
            return None

    @from_account_id.setter
    def from_account_id(self, from_account_id):
        """Setter from_account_id

        Args:
            from_account_id(double): id.

        Returns:

        Usage:
            >>> self.from_account_id = from_account_id
        """
        self.__from_account_id = from_account_id

    @property
    def to_account_id(self):
        """Getter to_account_id

        Args:

        Returns:
            double: to_account_id value

        Usage:
            >>> to_account_id = self.to_account_id
        """
        try:
            return self.__to_account_id
        except AttributeError:
            return None

    @to_account_id.setter
    def to_account_id(self, to_account_id):
        """Setter to_account_id

        Args:
            to_account_id(double): to_account_id.

        Returns:

        Usage:
            >>> self.to_account_id = to_account_id
        """
        self.__to_account_id = to_account_id

    @property
    def user_id(self):
        """Getter user_id

        Args:

        Returns:
            string: id value

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
            user_id(string): id.

        Returns:

        Usage:
            >>> self.user_id = user_id
        """
        self.__user_id = user_id

    @property
    def relation_id(self):
        """Getter relation_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> relation_id = self.relation_id
        """
        try:
            return self.__relation_id
        except AttributeError:
            return None

    @relation_id.setter
    def relation_id(self, relation_id):
        """Setter relation_id

        Args:
            relation_id(string): id.

        Returns:

        Usage:
            >>> self.relation_id = relation_id
        """
        self.__relation_id = relation_id

    @property
    def relation_type(self):
        """Getter relation_type

        Args:

        Returns:
            string: relation_type value

        Usage:
            >>> relation_type = self.relation_type
        """
        try:
            return self.__relation_type
        except AttributeError:
            return None

    @relation_type.setter
    def relation_type(self, relation_type):
        """Setter relation_type

        Args:
            relation_type(string): relation_type.

        Returns:

        Usage:
            >>> self.relation_type = relation_type
        """
        self.__relation_type = relation_type

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

    # @property
    # def currency(self):
    # 	"""Getter currency

    # 	Args:

    # 	Returns:
    # 		string: currency value

    # 	Usage:
    # 		>>> currency = self.currency
    # 	"""
    # 	try:
    # 		return self.__currency
    # 	except AttributeError:
    # 		return None

    # @currency.setter
    # def currency(self, currency):
    # 	"""Setter currency

    # 	Args:
    # 		currency(string): currency.

    # 	Returns:

    # 	Usage:
    # 		>>> self.currency = currency
    # 	"""
    # 	self.__currency = currency

    @property
    def amount(self):
        """Getter amount

        Args:

        Returns:
            double: amount value

        Usage:
            >>> amount = self.amount
        """
        try:
            return self.__amount
        except AttributeError:
            return None

    @amount.setter
    def amount(self, amount):
        """Setter amount

        Args:
            amount(double): amount.

        Returns:

        Usage:
            >>> self.amount = amount
        """
        self.__amount = amount

    @property
    def transaction_date(self):
        """Getter transaction_date

        Args:

        Returns:
            string: transaction_date value

        Usage:
            >>> transaction_date = self.transaction_date
        """
        try:
            return self.__transaction_date
        except AttributeError:
            return None

    @transaction_date.setter
    def transaction_date(self, transaction_date):
        """Setter transaction_date

        Args:
            transaction_date(string): transaction_date.

        Returns:

        Usage:
            >>> self.transaction_date = transaction_date
        """
        self.__transaction_date = transaction_date

    @property
    def notes(self):
        """Getter notes

        Args:

        Returns:
            str: notes value

        Usage:
            >>> notes = self.notes
        """
        try:
            return self.__notes
        except AttributeError:
            return False

    @notes.setter
    def notes(self, notes):
        """Setter notes

        Args:
            notes(str): notes.

        Returns:

        Usage:
            >>> self.notes = notes
        """
        self.__notes = notes

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
        return super().get_attrs(BankAccountTransfer)

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
        return f"BankAccountTransfer('{self.transfer_id}')"
