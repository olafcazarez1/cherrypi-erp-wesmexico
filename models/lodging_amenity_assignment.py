from .base import Model


class LodgingAmenityAssignment(Model):

    _TABLE = "lodgings_amenities_assignments"

    _IDS = [
        "lodging_id",
        "amenity_id",
    ]

    _BINARY = []
    _UNIQUE = []

    _FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "lodging_id",
        "amenity_id",
    ]

    _RESTRICTED = [
        "created_at",
    ]

    lodging_id = Model.field("lodging_id")
    amenity_id = Model.field("amenity_id")

    created_at = Model.field("created_at")

    def get_attrs(self):

        return super().get_attrs(LodgingAmenityAssignment)

    def __repr__(self):

        return "LodgingAmenityAssignment(" f"'{self.lodging_id}', " f"'{self.amenity_id}'" ")"
