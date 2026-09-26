from .base import Model


class Document(Model):

    _TABLE = "documents"
    _IDS = ["document_id"]
    _BINARY = []
    _UNIQUE = []

    _FILTER_LIMIT_DEFAULT = 50

    _REQUIRED = [
        "document_id",
        "source",
        "parent_id",
        "category",
        "subcategory",
        "data",
        "status",
    ]

    _RESTRICTED = [
        "created_at",
        "updated_at",
    ]

    document_id = Model.field("document_id")

    source = Model.field("source")
    parent_id = Model.field("parent_id")

    category = Model.field("category")
    subcategory = Model.field("subcategory")

    data = Model.field("data")

    status = Model.field("status", "active")

    created_at = Model.field("created_at")
    updated_at = Model.field("updated_at")

    def get_attrs(self):
        return super().get_attrs(Document)

    def __repr__(self):
        return "Document('{}', '{}', '{}', '{}')".format(
            self.document_id,
            self.source,
            self.category,
            self.subcategory,
        )
