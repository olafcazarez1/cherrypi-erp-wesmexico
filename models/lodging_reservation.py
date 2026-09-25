from .base import Model


class LodgingReservation(Model):

    _TABLE = "lodgings_reservations"
    _IDS = ["reservation_id"]
    _BINARY = []

    _UNIQUE = [
        "code",
    ]

    _FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "reservation_id",
        "lodging_id",
        "code",
        "guest_name",
        "guest_email",
        "check_in",
        "check_out",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    reservation_id = Model.field("reservation_id")
    lodging_id = Model.field("lodging_id")

    code = Model.field("code", "")

    guest_name = Model.field("guest_name", "")
    guest_email = Model.field("guest_email", "")
    guest_phone = Model.field("guest_phone", "")

    check_in = Model.field("check_in")
    check_out = Model.field("check_out")

    adults = Model.field("adults", 1)
    children = Model.field("children", 0)
    guests = Model.field("guests", 1)

    nights = Model.field("nights", 1)

    currency = Model.field("currency", "mxn")

    observations = Model.field("observations", "")

    status = Model.field("status", "confirmed")

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(LodgingReservation)

    def __repr__(self):
        return f"LodgingReservation('{self.reservation_id}')"
