from .base import Model


class PurchaseOrderDocumentProduct(Model):
    _TABLE = "purchase_orders_documents_details"
    _IDS = ["purchase_order_id", "product_id", "measure_id"]
    _BINARY = []
    _UNIQUE = []

    _FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "purchase_order_id",
        "product_id",
        "measure_id",
        "currency",
        "quantity",
        "original_price",
        "discount_factor",
        "price",
        "amount",
        "discount",
        "subtotal",
        "taxes",
        "total",
    ]

    _RESTRICTED = ["created_at", "updated_at"]

    purchase_order_id = Model.field("purchase_order_id")
    product_id = Model.field("product_id")
    measure_id = Model.field("measure_id")

    currency = Model.field("currency", "mxn")

    quantity = Model.field("quantity", 0.00)
    original_price = Model.field("original_price", 0.00)
    discount_factor = Model.field("discount_factor", 0.00)

    price = Model.field("price", 0.00)
    amount = Model.field("amount", 0.00)
    discount = Model.field("discount", 0.00)
    subtotal = Model.field("subtotal", 0.00)
    taxes = Model.field("taxes", 0.00)
    total = Model.field("total", 0.00)

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(PurchaseOrderDocumentProduct)

    def __repr__(self):
        return f"PurchaseOrderDocumentProduct('{self.purchase_order_id}')"
