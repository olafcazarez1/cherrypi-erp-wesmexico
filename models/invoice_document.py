from .base import Model


class InvoiceDocument(Model):
    """Database table name"""

    _TABLE = "invoiced_documents"

    """Database primary keys
    """
    _IDS = ["invoice_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "invoice_id",
        "company_id",
        "branch_id",
        "warehouse_id",
        "client_id",
        "user_id",
        "code",
        "currency",
        "exchange_rate",
        "amount",
        "subtotal",
        "discount",
        "taxes",
        "total",
        "transaction_method",
        "transaction_type",
        "transaction_date",
        "transaction_status",
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
    def invoice_id(self):
        """Getter invoice_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> invoice_id = self.invoice_id
        """
        try:
            return self.__invoice_id
        except AttributeError:
            return None

    @invoice_id.setter
    def invoice_id(self, invoice_id):
        """Setter invoice_id

        Args:
            invoice_id(string): id.

        Returns:

        Usage:
            >>> self.invoice_id = invoice_id
        """
        self.__invoice_id = invoice_id

    @property
    def company_id(self):
        """Getter company_id

        Args:

        Returns:
            string: company_id value

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
            company_id(string): company_id.

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
            string: branch_id value

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
            branch_id(string): branch_id.

        Returns:

        Usage:
            >>> self.branch_id = branch_id
        """
        self.__branch_id = branch_id

    @property
    def warehouse_id(self):
        """Getter warehouse_id

        Args:

        Returns:
            string: warehouse_id value

        Usage:
            >>> warehouse_id = self.warehouse_id
        """
        try:
            return self.__warehouse_id
        except AttributeError:
            return None

    @warehouse_id.setter
    def warehouse_id(self, warehouse_id):
        """Setter warehouse_id

        Args:
            warehouse_id(string): warehouse_id.

        Returns:

        Usage:
            >>> self.warehouse_id = warehouse_id
        """
        self.__warehouse_id = warehouse_id

    @property
    def client_id(self):
        """Getter client_id

        Args:

        Returns:
            string: client_id value

        Usage:
            >>> client_id = self.client_id
        """
        try:
            return self.__client_id
        except AttributeError:
            return None

    @client_id.setter
    def client_id(self, client_id):
        """Setter client_id

        Args:
            client_id(string): client_id.

        Returns:

        Usage:
            >>> self.client_id = client_id
        """
        self.__client_id = client_id

    @property
    def user_id(self):
        """Getter user_id

        Args:

        Returns:
            string: user_id value

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
            user_id(string): user_id.

        Returns:

        Usage:
            >>> self.user_id = user_id
        """
        self.__user_id = user_id

    @property
    def payment_type_id(self):
        """Getter payment_type_id

        Args:

        Returns:
            string: payment_type_id value

        Usage:
            >>> payment_type_id = self.payment_type_id
        """
        try:
            return self.__payment_type_id
        except AttributeError:
            return None

    @payment_type_id.setter
    def payment_type_id(self, payment_type_id):
        """Setter payment_type_id

        Args:
            payment_type_id(string): payment_type_id.

        Returns:

        Usage:
            >>> self.payment_type_id = payment_type_id
        """
        self.__payment_type_id = payment_type_id

    @property
    def payment_method_id(self):
        """Getter payment_method_id

        Args:

        Returns:
            string: payment_method_id value

        Usage:
            >>> payment_method_id = self.payment_method_id
        """
        try:
            return self.__payment_method_id
        except AttributeError:
            return None

    @payment_method_id.setter
    def payment_method_id(self, payment_method_id):
        """Setter payment_method_id

        Args:
            payment_method_id(string): payment_method_id.

        Returns:

        Usage:
            >>> self.payment_method_id = payment_method_id
        """
        self.__payment_method_id = payment_method_id

    @property
    def receipt_type_id(self):
        """Getter receipt_type_id

        Args:

        Returns:
            string: receipt_type_id value

        Usage:
            >>> receipt_type_id = self.receipt_type_id
        """
        try:
            return self.__receipt_type_id
        except AttributeError:
            return None

    @receipt_type_id.setter
    def receipt_type_id(self, receipt_type_id):
        """Setter receipt_type_id

        Args:
            receipt_type_id(string): receipt_type_id.

        Returns:

        Usage:
            >>> self.receipt_type_id = receipt_type_id
        """
        self.__receipt_type_id = receipt_type_id

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
    def subtotal(self):
        """Getter subtotal

        Args:

        Returns:
            double: subtotal value

        Usage:
            >>> subtotal = self.subtotal
        """
        try:
            return self.__subtotal
        except AttributeError:
            return None

    @subtotal.setter
    def subtotal(self, subtotal):
        """Setter subtotal

        Args:
            subtotal(double): subtotal.

        Returns:

        Usage:
            >>> self.subtotal = subtotal
        """
        self.__subtotal = subtotal

    @property
    def discount(self):
        """Getter discount

        Args:

        Returns:
            double: discount value

        Usage:
            >>> discount = self.discount
        """
        try:
            return self.__discount
        except AttributeError:
            return None

    @discount.setter
    def discount(self, discount):
        """Setter discount

        Args:
            discount(double): discount.

        Returns:

        Usage:
            >>> self.discount = discount
        """
        self.__discount = discount

    @property
    def taxes(self):
        """Getter taxes

        Args:

        Returns:
            double: taxes value

        Usage:
            >>> taxes = self.taxes
        """
        try:
            return self.__taxes
        except AttributeError:
            return None

    @taxes.setter
    def taxes(self, taxes):
        """Setter taxes

        Args:
            taxes(double): taxes.

        Returns:

        Usage:
            >>> self.taxes = taxes
        """
        self.__taxes = taxes

    @property
    def total(self):
        """Getter total

        Args:

        Returns:
            double: total value

        Usage:
            >>> total = self.total
        """
        try:
            return self.__total
        except AttributeError:
            return None

    @total.setter
    def total(self, total):
        """Setter total

        Args:
            total(double): total.

        Returns:

        Usage:
            >>> self.total = total
        """
        self.__total = total

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
    def transaction_type(self):
        """Getter transaction_type

        Args:

        Returns:
            string: transaction_type value

        Usage:
            >>> transaction_type = self.transaction_type
        """
        try:
            return self.__transaction_type
        except AttributeError:
            return "full_payment"

    @transaction_type.setter
    def transaction_type(self, transaction_type):
        """Setter transaction_type

        Args:
            transaction_type(string): transaction_type.

        Returns:

        Usage:
            >>> self.transaction_type = transaction_type
        """
        self.__transaction_type = transaction_type

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
    def transaction_status(self):
        """Getter transaction_status

        Args:

        Returns:
            string: transaction_status value

        Usage:
            >>> transaction_status = self.transaction_status
        """
        try:
            return self.__transaction_status
        except AttributeError:
            return "pending"

    @transaction_status.setter
    def transaction_status(self, transaction_status):
        """Setter transaction_status

        Args:
            transaction_status(string): transaction_status.

        Returns:

        Usage:
            >>> self.transaction_status = transaction_status
        """
        self.__transaction_status = transaction_status

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
            return "pending"

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
        return super().get_attrs(InvoiceDocument)

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
        return f"InvoiceDocument('{self.invoice_id}')"
