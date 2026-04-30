from .base import Model


class PurchaseOrderDocument(Model):
    _TABLE = "purchase_orders_documents"
    _IDS = ["purchase_order_id"]
    _BINARY = []
    _UNIQUE = []

    _FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "purchase_order_id",
        "company_id",
        "branch_id",
        "warehouse_id",
        "supplier_id",
        "user_id",
        "employee_id",
        "code",
        "reference",
        "priority",
        "currency",
        "exchange_rate",
        "amount",
        "discount",
        "subtotal",
        "taxes",
        "total",
        "transaction_date",
        "notes",
        "status",
    ]

    _RESTRICTED = ["created_at", "updated_at"]

    purchase_order_id = Model.field("purchase_order_id")
    company_id = Model.field("company_id")
    branch_id = Model.field("branch_id")
    warehouse_id = Model.field("warehouse_id")
    supplier_id = Model.field("supplier_id")
    user_id = Model.field("user_id")
    employee_id = Model.field("employee_id")

    code = Model.field("code")
    reference = Model.field("reference", "")
    priority = Model.field("priority", "medium")

    currency = Model.field("currency", "mxn")
    exchange_rate = Model.field("exchange_rate", 1.00)

    amount = Model.field("amount", 0.00)
    discount = Model.field("discount", 0.00)
    subtotal = Model.field("subtotal", 0.00)
    taxes = Model.field("taxes", 0.00)
    total = Model.field("total", 0.00)

    transaction_date = Model.field("transaction_date")
    notes = Model.field("notes", "")

    is_approved = Model.field("is_approved", 0)
    approved_by = Model.field("approved_by")
    approved_at = Model.field("approved_at")

    status = Model.field("status", "new")

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(PurchaseOrderDocument)

    def __repr__(self):
        return f"PurchaseOrderDocument('{self.purchase_order_id}')"
