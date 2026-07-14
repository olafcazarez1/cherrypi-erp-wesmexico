from .base import Model


class PostalCode(Model):
    _TABLE = "postal_codes"

    _IDS = [
        "zip",
    ]

    _BINARY = []
    _UNIQUE = []

    _FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "state_id",
        "municipality_id",
        "locality_id",
        "zip",
        "border_zone",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    state_id = Model.field("state_id")
    municipality_id = Model.field("municipality_id")
    locality_id = Model.field("locality_id")

    zip = Model.field("zip", "")
    border_zone = Model.field("border_zone", 0)

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(PostalCode)

    def __repr__(self):
        return f"PostalCode('{self.zip}')"