from .base import Model


class StockInOut(Model):
    """Database table name"""

    _TABLE = "stocks_io"

    """Database primary keys
    """
    _IDS = ["stock_io_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "stock_io_id",
        "user_id",
        "employee_id",
        "company_id",
        "branch_id",
        "warehouse_id",
        "supplier_id",
        "code",
        "reference",
        "transaction_type",
        "document_type",
        "currency",
        "exchange_rate",
        "amount",
        "subtotal",
        "discount",
        "tax",
        "total",
        "type",
        "transaction_date",
        "payment_type",
        "payment_method",
        "tax_receipt",
        "purchase_origin",
        "importation_number",
        "importation_date",
        "custom_id",
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
    def stock_io_id(self):
        """Getter stock_io_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> stock_io_id = self.stock_io_id
        """
        try:
            return self.__stock_io_id
        except AttributeError:
            return None

    @stock_io_id.setter
    def stock_io_id(self, stock_io_id):
        """Setter stock_io_id

        Args:
            stock_io_id(string): id.

        Returns:

        Usage:
            >>> self.stock_io_id = stock_io_id
        """
        self.__stock_io_id = stock_io_id

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
    def employee_id(self):
        """Getter employee_id

        Args:

        Returns:
            string: employee_id value

        Usage:
            >>> employee_id = self.employee_id
        """
        try:
            return self.__employee_id
        except AttributeError:
            return "active"

    @employee_id.setter
    def employee_id(self, employee_id):
        """Setter employee_id

        Args:
            employee_id(string): employee_id.

        Returns:

        Usage:
            >>> self.employee_id = employee_id
        """
        self.__employee_id = employee_id

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
            return "active"

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
    def supplier_id(self):
        """Getter supplier_id

        Args:

        Returns:
            string: supplier_id value

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
            supplier_id(string): supplier_id.

        Returns:

        Usage:
            >>> self.supplier_id = supplier_id
        """
        self.__supplier_id = supplier_id

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
            return "active"

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
    def document_type(self):
        """Getter document_type

        Args:

        Returns:
            string: document_type value

        Usage:
            >>> document_type = self.document_type
        """
        try:
            return self.__document_type
        except AttributeError:
            return "active"

    @document_type.setter
    def document_type(self, document_type):
        """Setter document_type

        Args:
            document_type(string): document_type.

        Returns:

        Usage:
            >>> self.document_type = document_type
        """
        self.__document_type = document_type

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
    def tax(self):
        """Getter tax

        Args:

        Returns:
            double: tax value

        Usage:
            >>> tax = self.tax
        """
        try:
            return self.__tax
        except AttributeError:
            return None

    @tax.setter
    def tax(self, tax):
        """Setter tax

        Args:
            tax(double): tax.

        Returns:

        Usage:
            >>> self.tax = tax
        """
        self.__tax = tax

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
    def type(self):
        """Getter type

        Args:

        Returns:
            double: type value

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
            type(double): type.

        Returns:

        Usage:
            >>> self.type = type
        """
        self.__type = type

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
    def payment_type(self):
        """Getter payment_type

        Args:

        Returns:
            string: payment_type value

        Usage:
            >>> payment_type = self.payment_type
        """
        try:
            return self.__payment_type
        except AttributeError:
            return "active"

    @payment_type.setter
    def payment_type(self, payment_type):
        """Setter payment_type

        Args:
            payment_type(string): payment_type.

        Returns:

        Usage:
            >>> self.payment_type = payment_type
        """
        self.__payment_type = payment_type

    @property
    def payment_method(self):
        """Getter payment_method

        Args:

        Returns:
            string: payment_method value

        Usage:
            >>> payment_method = self.payment_method
        """
        try:
            return self.__payment_method
        except AttributeError:
            return "active"

    @payment_method.setter
    def payment_method(self, payment_method):
        """Setter payment_method

        Args:
            payment_method(string): payment_method.

        Returns:

        Usage:
            >>> self.payment_method = payment_method
        """
        self.__payment_method = payment_method

    @property
    def tax_receipt(self):
        """Getter tax_receipt

        Args:

        Returns:
            string: tax_receipt value

        Usage:
            >>> tax_receipt = self.tax_receipt
        """
        try:
            return self.__tax_receipt
        except AttributeError:
            return "active"

    @tax_receipt.setter
    def tax_receipt(self, tax_receipt):
        """Setter tax_receipt

        Args:
            tax_receipt(string): tax_receipt.

        Returns:

        Usage:
            >>> self.tax_receipt = tax_receipt
        """
        self.__tax_receipt = tax_receipt

    @property
    def purchase_origin(self):
        """Getter purchase_origin

        Args:

        Returns:
            string: purchase_origin value

        Usage:
            >>> purchase_origin = self.purchase_origin
        """
        try:
            return self.__purchase_origin
        except AttributeError:
            return "national"

    @purchase_origin.setter
    def purchase_origin(self, purchase_origin):
        """Setter purchase_origin

        Args:
            purchase_origin(string): purchase_origin.

        Returns:

        Usage:
            >>> self.purchase_origin = purchase_origin
        """
        self.__purchase_origin = purchase_origin

    @property
    def importation_number(self):
        """Getter importation_number

        Args:

        Returns:
            string: importation_number value

        Usage:
            >>> importation_number = self.importation_number
        """
        try:
            return self.__importation_number
        except AttributeError:
            return ""

    @importation_number.setter
    def importation_number(self, importation_number):
        """Setter importation_number

        Args:
            importation_number(string): importation_number.

        Returns:

        Usage:
            >>> self.importation_number = importation_number
        """
        self.__importation_number = importation_number

    @property
    def importation_date(self):
        """Getter importation_date

        Args:

        Returns:
            date: importation_date value

        Usage:
            >>> importation_date = self.importation_date
        """
        try:
            return self.__importation_date
        except AttributeError:
            return "1970-01-01"

    @importation_date.setter
    def importation_date(self, importation_date):
        """Setter importation_date

        Args:
            importation_date(date): importation_date.

        Returns:

        Usage:
            >>> self.importation_date = importation_date
        """
        self.__importation_date = importation_date

    @property
    def custom_id(self):
        """Getter custom_id

        Args:

        Returns:
            string: custom_id value

        Usage:
            >>> custom_id = self.custom_id
        """
        try:
            return self.__custom_id
        except AttributeError:
            return "00"

    @custom_id.setter
    def custom_id(self, custom_id):
        """Setter custom_id

        Args:
            custom_id(string): custom_id.

        Returns:

        Usage:
            >>> self.custom_id = custom_id
        """
        self.__custom_id = custom_id

    @property
    def notes(self):
        """Getter notes

        Args:

        Returns:
            string: notes value

        Usage:
            >>> notes = self.notes
        """
        try:
            return self.__notes
        except AttributeError:
            return "active"

    @notes.setter
    def notes(self, notes):
        """Setter notes

        Args:
            notes(string): notes.

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
        return super().get_attrs(StockInOut)

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
        return f"StockInOut('{self.stock_io_id}')"
