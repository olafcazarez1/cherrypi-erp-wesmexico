from .base import Model


class Lodging(Model):

    _TABLE = "lodgings"
    _IDS = ["lodging_id"]
    _BINARY = []
    _UNIQUE = [
        "code",
        "name",
    ]

    _FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "lodging_id",
        "code",
        "name",
        "type",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    lodging_id = Model.field("lodging_id")

    code = Model.field("code", "")
    name = Model.field("name", "")
    type = Model.field("type", "")

    description = Model.field("description", "")

    image = Model.field("image", "")

    bedrooms = Model.field("bedrooms", 0)
    beds = Model.field("beds", 0)
    bathrooms = Model.field("bathrooms", 0)
    max_occupancy = Model.field("max_occupancy", 1)

    price_per_night = Model.field("price_per_night", 0)
    currency = Model.field("currency", "mxn")

    check_in_time = Model.field("check_in_time")
    check_out_time = Model.field("check_out_time")

    address_street = Model.field("address_street", "")
    address_external_number = Model.field("address_external_number", "")
    address_internal_number = Model.field("address_internal_number", "")

    neighborhood = Model.field("neighborhood", "")

    state_id = Model.field("state_id", "")
    municipality_id = Model.field("municipality_id", "")
    locality_id = Model.field("locality_id", "")

    zip = Model.field("zip", "")

    observations = Model.field("observations", "")

    status = Model.field("status", "active")

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):

        return super().get_attrs(Lodging)

    def __repr__(self):

        return f"Lodging('{self.lodging_id}')"
