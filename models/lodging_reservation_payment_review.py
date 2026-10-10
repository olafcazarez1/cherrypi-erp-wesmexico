from .base import Model


class LodgingReservationPaymentReview(Model):

    _TABLE = "lodgings_reservations_payments_reviews"

    _IDS = [
        "review_id",
    ]

    _BINARY = []
    _UNIQUE = []

    _REQUIRED = [
        "review_id",
        "payment_id",
        "asset_id",
        "url",
        "status",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    review_id = Model.field("review_id")
    payment_id = Model.field("payment_id")

    asset_id = Model.field("asset_id")
    url = Model.field("url", "")

    status = Model.field("status", "pending")

    reviewed_by = Model.field("reviewed_by")
    reviewed_at = Model.field("reviewed_at")

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(LodgingReservationPaymentReview)

    def __repr__(self):
        return f"LodgingReservationPaymentReview('{self.review_id}')"
