from .base import Model


class LodgingReservationPayment(Model):

    _TABLE = "lodging_reservation_payments"

    _IDS = [
        "payment_id",
    ]

    _UNIQUE = []

    _REQUIRED = [
        "reservation_id",
        "provider",
        "amount",
        "currency",
        "status",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    payment_id = Model.field("payment_id", None)

    reservation_id = Model.field("reservation_id", None)

    provider = Model.field("provider", "")

    provider_reference = Model.field("provider_reference", "")

    provider_payment_id = Model.field("provider_payment_id", "")

    amount = Model.field("amount", 0)

    currency = Model.field("currency", "MXN")

    status = Model.field("status", "pending")

    created_at = Model.field("created_at", None)

    updated_at = Model.field("updated_at", None)

    def __repr__(self):

        return "<LodgingReservationPayment %s>" % (self.payment_id)
