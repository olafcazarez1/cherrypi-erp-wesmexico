from .base import Model


class DocumentPayment(Model):
    """Database table name"""

    _TABLE = "sales_documents_payments"

    """Database primary keys
    """
    _IDS = ["payment_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "payment_id",
        "document_id",
        "branch_id",
        "register_id",
        "user_id",
        "reference",
        "code",
        "transaction_method",
        "amount",
        "pay_with",
        "change",
        "balance",
        "currency",
        "exchange_rate",
        "is_signed",
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
    def payment_id(self):
        """Getter payment_id

        Args:

        Returns:
            string: payment id value

        Usage:
            >>> payment_id = self.payment_id
        """
        try:
            return self.__payment_id
        except AttributeError:
            return None

    @payment_id.setter
    def payment_id(self, payment_id):
        """Setter payment_id

        Args:
            payment_id(string): payment id.

        Returns:

        Usage:
            >>> self.payment_id = payment_id
        """
        self.__payment_id = payment_id

    @property
    def branch_id(self):
        """Getter branch_id

        Args:

        Returns:
            string: branch id value

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
            branch_id(string): branch id.

        Returns:

        Usage:
            >>> self.branch_id = branch_id
        """
        self.__branch_id = branch_id

    @property
    def document_id(self):
        """Getter document_id

        Args:

        Returns:
            string: document id value

        Usage:
            >>> document_id = self.document_id
        """
        try:
            return self.__document_id
        except AttributeError:
            return None

    @document_id.setter
    def document_id(self, document_id):
        """Setter document_id

        Args:
            document_id(string): document id.

        Returns:

        Usage:
            >>> self.document_id = document_id
        """
        self.__document_id = document_id

    @property
    def register_id(self):
        """Getter register_id

        Args:

        Returns:
            string: register_id value

        Usage:
            >>> register_id = self.register_id
        """
        try:
            return self.__register_id
        except AttributeError:
            return None

    @register_id.setter
    def register_id(self, register_id):
        """Setter register_id

        Args:
            register_id(string): register_id.

        Returns:

        Usage:
            >>> self.register_id = register_id
        """
        self.__register_id = register_id

    @property
    def user_id(self):
        """Getter user_id

        Args:

        Returns:
            string: user id value

        Usage:
            >>> user_id = self.user_id
        """
        try:
            return self.__user_id
        except AttributeError:
            return "active"

    @user_id.setter
    def user_id(self, user_id):
        """Setter user_id

        Args:
            user_id(string): user id.

        Returns:

        Usage:
            >>> self.user_id = user_id
        """
        self.__user_id = user_id

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
    def transaction_method(self):
        """Getter transaction_method

        Args:

        Returns:
            string: transaction_method value

        Usage:
            >>> transaction_method = self.transaction_method
        """
        try:
            return self.__transaction_method
        except AttributeError:
            return "active"

    @transaction_method.setter
    def transaction_method(self, transaction_method):
        """Setter transaction_method

        Args:
            transaction_method(string): transaction_method.

        Returns:

        Usage:
            >>> self.transaction_method = transaction_method
        """
        self.__transaction_method = transaction_method

    @property
    def pay_with(self):
        """Getter pay_with

        Args:

        Returns:
            double: pay_with value

        Usage:
            >>> pay_with = self.pay_with
        """
        try:
            return self.__pay_with
        except AttributeError:
            return None

    @pay_with.setter
    def pay_with(self, pay_with):
        """Setter pay_with

        Args:
            pay_with(double): pay_with.

        Returns:

        Usage:
            >>> self.pay_with = pay_with
        """
        self.__pay_with = pay_with

    @property
    def change(self):
        """Getter change

        Args:

        Returns:
            double: change value

        Usage:
            >>> change = self.change
        """
        try:
            return self.__change
        except AttributeError:
            return None

    @change.setter
    def change(self, change):
        """Setter change

        Args:
            change(double): change.

        Returns:

        Usage:
            >>> self.change = change
        """
        self.__change = change

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
    def currency(self):
        """Getter currency

        Args:

        Returns:
            double: currency value

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
            currency(double): currency.

        Returns:

        Usage:
            >>> self.currency = currency
        """
        self.__currency = currency

    @property
    def exchange_rate(self):
        """Getter exchange_rate

        Args:

        Returns:
            double: exchange_rate value

        Usage:
            >>> exchange_rate = self.exchange_rate
        """
        try:
            return self.__exchange_rate
        except AttributeError:
            return None

    @exchange_rate.setter
    def exchange_rate(self, exchange_rate):
        """Setter exchange_rate

        Args:
            exchange_rate(double): exchange_rate.

        Returns:

        Usage:
            >>> self.exchange_rate = exchange_rate
        """
        self.__exchange_rate = exchange_rate

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
            return "active"

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
    def is_signed(self):
        """Getter is_signed

        Args:

        Returns:
            string: is_signed value

        Usage:
            >>> is_signed = self.is_signed
        """
        try:
            return self.__is_signed
        except AttributeError:
            return False

    @is_signed.setter
    def is_signed(self, is_signed):
        """Setter is_signed

        Args:
            is_signed(string): is_signed.

        Returns:

        Usage:
            >>> self.is_signed = is_signed
        """
        self.__is_signed = is_signed

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
        return super().get_attrs(DocumentPayment)

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
        return f"DocumentPayment('{self.payment_id}')"
