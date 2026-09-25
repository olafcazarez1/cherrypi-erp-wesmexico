from .base import Model


class LodgingAmenity(Model):

    _TABLE = "lodgings_amenities"
    _IDS = ["amenity_id"]
    _BINARY = []
    _UNIQUE = ["code"]

    _FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "amenity_id",
        "code",
        "name",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    amenity_id = Model.field("amenity_id")

    code = Model.field("code", "")
    name = Model.field("name", "")
    description = Model.field("description", "")

    status = Model.field("status", "active")

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(LodgingAmenity)

    def __repr__(self):
        return f"LodgingAmenity('{self.amenity_id}')"
