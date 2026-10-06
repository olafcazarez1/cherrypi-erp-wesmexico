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
        "first_name",
        "last_name",
        "email",
        "phone",
        "check_in",
        "check_out",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    reservation_id = Model.field("reservation_id")
    lodging_id = Model.field("lodging_id")
    reservation_session_id = Model.field("reservation_session_id", None)

    code = Model.field("code", "")

    first_name = Model.field("first_name", "")
    last_name = Model.field("last_name", "")

    email = Model.field("email", "")
    phone = Model.field("phone", "")

    check_in = Model.field("check_in")
    check_out = Model.field("check_out")

    adults = Model.field("adults", 1)
    children = Model.field("children", 0)
    guests = Model.field("guests", 1)

    nights = Model.field("nights", 1)

    currency = Model.field("currency", "mxn")

    observations = Model.field("observations", "")

    status = Model.field("status", "confirmed")

    expires_at = Model.field("expires_at")

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(LodgingReservation)

    def __repr__(self):
        return f"LodgingReservation('{self.reservation_id}')"
