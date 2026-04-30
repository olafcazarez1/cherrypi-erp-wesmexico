from .base import Model


class PurchaseOrderDocumentTax(Model):
    _TABLE = "purchase_orders_documents_products_taxes"
    _IDS = ["purchase_order_id", "product_id", "tax_id"]
    _BINARY = []
    _UNIQUE = []

    _FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "purchase_order_id",
        "product_id",
        "tax_id",
        "percent",
    ]

    _RESTRICTED = ["created_at", "updated_at"]

    purchase_order_id = Model.field("purchase_order_id")
    product_id = Model.field("product_id")
    tax_id = Model.field("tax_id")

    percent = Model.field("percent", 0.00)

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(PurchaseOrderDocumentTax)

    def __repr__(self):
        return f"PurchaseOrderDocumentTax('{self.purchase_order_id}')"
