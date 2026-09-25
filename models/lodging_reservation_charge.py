from .base import Model


class LodgingReservationCharge(Model):

    _TABLE = "lodgings_reservations_charges"
    _IDS = ["charge_id"]
    _BINARY = []

    _UNIQUE = []

    _FILTER_LIMIT_DEFAULT = 100

    _REQUIRED = [
        "charge_id",
        "reservation_id",
        "type",
        "name",
        "quantity",
        "unit_price",
        "subtotal",
        "total",
        "currency",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    charge_id = Model.field("charge_id")
    reservation_id = Model.field("reservation_id")

    type = Model.field("type", "")

    name = Model.field("name", "")
    description = Model.field("description", "")

    quantity = Model.field("quantity", 1)
    unit_price = Model.field("unit_price", 0)

    subtotal = Model.field("subtotal", 0)
    taxes = Model.field("taxes", 0)
    total = Model.field("total", 0)

    currency = Model.field("currency", "mxn")

    status = Model.field("status", "active")

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(LodgingReservationCharge)

    def __repr__(self):
        return f"LodgingReservationCharge('{self.charge_id}')"
