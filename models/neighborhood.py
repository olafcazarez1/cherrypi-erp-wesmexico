from .base import Model


class Neighborhood(Model):
    _TABLE = "neighborhoods"

    _IDS = [
        "zip",
        "neighborhood_id",
        "name",
    ]

    _BINARY = []
    _UNIQUE = []

    __FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "neighborhood_id",
        "zip",
        "name",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    neighborhood_id = Model.field(
        "neighborhood_id",
        "",
    )

    zip = Model.field("zip", "")
    name = Model.field("name", "")

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(Neighborhood)

    def __repr__(self):
        return (
            f"Neighborhood("
            f"'{self.zip}', "
            f"'{self.neighborhood_id}', "
            f"'{self.name}'"
            f")"
        )