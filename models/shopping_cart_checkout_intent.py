from .base import Model


class ShoppingCartCheckoutIntent(Model):
    _TABLE = "shopping_cart_checkout_intents"
    _IDS = ["cart_id"]
    _BINARY = []
    _UNIQUE = []

    _FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "cart_id",
        "provider",
        "name",
        "email",
        "phone",
        "street",
        "exterior_number",
        "neighborhood",
        "postal_code",
        "city",
        "state",
        "status",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    cart_id = Model.field("cart_id")

    provider = Model.field("provider", "")
    provider_reference = Model.field(
        "provider_reference",
        "",
    )

    document_id = Model.field(
        "document_id",
        None,
    )

    name = Model.field("name", "")
    email = Model.field("email", "")
    phone = Model.field("phone", "")

    street = Model.field("street", "")

    exterior_number = Model.field(
        "exterior_number",
        "",
    )

    interior_number = Model.field(
        "interior_number",
        "",
    )

    neighborhood = Model.field(
        "neighborhood",
        "",
    )

    postal_code = Model.field(
        "postal_code",
        "",
    )

    city = Model.field("city", "")
    state = Model.field("state", "")

    reference = Model.field(
        "reference",
        "",
    )

    status = Model.field(
        "status",
        "pending",
    )

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(ShoppingCartCheckoutIntent)

    def __repr__(self):
        return "ShoppingCartCheckoutIntent" f"('{self.cart_id}')"
