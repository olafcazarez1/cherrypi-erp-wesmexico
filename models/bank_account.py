from .base import Model


class BankAccount(Model):
    """Database table associated_with"""

    _TABLE = "bank_accounts"

    """Database primary keys
    """
    _IDS = ["bank_account_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "bank_account_id",
        "associated_id",
        "code",
        "associated_with",
        "internal_code",
        "bank_id",
        "bank_code",
        "bank_name",
        "description",
        "currency",
        "account_number",
        "card_number",
        "interbank_key",
        "reference",
        "balance",
        "type",
        "is_default",
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
    def bank_account_id(self):
        """Getter bank_account_id

        Args:

        Returns:
            string: id value

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
            bank_account_id(string): id.

        Returns:

        Usage:
            >>> self.bank_account_id = bank_account_id
        """
        self.__bank_account_id = bank_account_id

    @property
    def associated_id(self):
        """Getter associated_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> associated_id = self.associated_id
        """
        try:
            return self.__associated_id
        except AttributeError:
            return None

    @associated_id.setter
    def associated_id(self, associated_id):
        """Setter associated_id

        Args:
            associated_id(string): id.

        Returns:

        Usage:
            >>> self.associated_id = associated_id
        """
        self.__associated_id = associated_id

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
    def associated_with(self):
        """Getter associated_with

        Args:

        Returns:
            string: associated_with value

        Usage:
            >>> associated_with = self.associated_with
        """
        try:
            return self.__associated_with
        except AttributeError:
            return None

    @associated_with.setter
    def associated_with(self, associated_with):
        """Setter associated_with

        Args:
            associated_with(string): associated_with.

        Returns:

        Usage:
            >>> self.associated_with = associated_with
        """
        self.__associated_with = associated_with

    @property
    def internal_code(self):
        """Getter internal_code

        Args:

        Returns:
            string: internal_code value

        Usage:
            >>> internal_code = self.internal_code
        """
        try:
            return self.__internal_code
        except AttributeError:
            return None

    @internal_code.setter
    def internal_code(self, internal_code):
        """Setter internal_code

        Args:
            internal_code(string): internal_code.

        Returns:

        Usage:
            >>> self.internal_code = internal_code
        """
        self.__internal_code = internal_code

    @property
    def bank_id(self):
        """Getter bank_id

        Args:

        Returns:
            string: bank_id value

        Usage:
            >>> bank_id = self.bank_id
        """
        try:
            return self.__bank_id
        except AttributeError:
            return None

    @bank_id.setter
    def bank_id(self, bank_id):
        """Setter bank_id

        Args:
            bank_id(string): bank_id.

        Returns:

        Usage:
            >>> self.bank_id = bank_id
        """
        self.__bank_id = bank_id

    @property
    def bank_code(self):
        """Getter bank_code

        Args:

        Returns:
            string: bank_code value

        Usage:
            >>> bank_code = self.bank_code
        """
        try:
            return self.__bank_code
        except AttributeError:
            return None

    @bank_code.setter
    def bank_code(self, bank_code):
        """Setter bank_code

        Args:
            bank_code(string): bank_code.

        Returns:

        Usage:
            >>> self.bank_code = bank_code
        """
        self.__bank_code = bank_code

    @property
    def bank_name(self):
        """Getter bank_name

        Args:

        Returns:
            string: bank_name value

        Usage:
            >>> bank_name = self.bank_name
        """
        try:
            return self.__bank_name
        except AttributeError:
            return None

    @bank_name.setter
    def bank_name(self, bank_name):
        """Setter bank_name

        Args:
            bank_name(string): bank_name.

        Returns:

        Usage:
            >>> self.bank_name = bank_name
        """
        self.__bank_name = bank_name

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
    def account_number(self):
        """Getter account_number

        Args:

        Returns:
            string: account_number value

        Usage:
            >>> account_number = self.account_number
        """
        try:
            return self.__account_number
        except AttributeError:
            return None

    @account_number.setter
    def account_number(self, account_number):
        """Setter account_number

        Args:
            account_number(string): account_number.

        Returns:

        Usage:
            >>> self.account_number = account_number
        """
        self.__account_number = account_number

    @property
    def card_number(self):
        """Getter card_number

        Args:

        Returns:
            string: card_number value

        Usage:
            >>> card_number = self.card_number
        """
        try:
            return self.__card_number
        except AttributeError:
            return None

    @card_number.setter
    def card_number(self, card_number):
        """Setter card_number

        Args:
            card_number(string): card_number.

        Returns:

        Usage:
            >>> self.card_number = card_number
        """
        self.__card_number = card_number

    @property
    def interbank_key(self):
        """Getter interbank_key

        Args:

        Returns:
            string: interbank_key value

        Usage:
            >>> interbank_key = self.interbank_key
        """
        try:
            return self.__interbank_key
        except AttributeError:
            return None

    @interbank_key.setter
    def interbank_key(self, interbank_key):
        """Setter interbank_key

        Args:
            interbank_key(string): interbank_key.

        Returns:

        Usage:
            >>> self.interbank_key = interbank_key
        """
        self.__interbank_key = interbank_key

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
    def balance(self):
        """Getter balance

        Args:

        Returns:
            double: balance value

        Usage:
            >>> balance = self.balance
        """
        try:
            return self.__balance
        except AttributeError:
            return None

    @balance.setter
    def balance(self, balance):
        """Setter balance

        Args:
            balance(double): balance.

        Returns:

        Usage:
            >>> self.balance = balance
        """
        self.__balance = balance

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
            return "active"

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
    def is_default(self):
        """Getter is_default

        Args:

        Returns:
            bool: is_default value

        Usage:
            >>> is_default = self.is_default
        """
        try:
            return self.__is_default
        except AttributeError:
            return False

    @is_default.setter
    def is_default(self, is_default):
        """Setter is_default

        Args:
            is_default(bool): is_default.

        Returns:

        Usage:
            >>> self.is_default = is_default
        """
        self.__is_default = is_default

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
        return super().get_attrs(BankAccount)

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
        return f"BankAccount('{self.bank_account_id}')"
