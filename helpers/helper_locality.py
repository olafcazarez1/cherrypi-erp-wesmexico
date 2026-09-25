from models.state import State
from models.municipality import Municipality
from models.locality import Locality


class HelperLocality(object):

    def __init__(self):
        pass

    @classmethod
    def get(cls, item: dict, conn: any):

        response = {}

        response["state"] = State().where({"state_id": item["state_id"]}).one_or_none(conn=conn).as_dict()

        response["municipality"] = (
            Municipality()
            .where(
                {"state_id": item["state_id"]},
                {"municipality_id": item["municipality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        response["locality"] = (
            Locality()
            .where(
                {"state_id": item["state_id"]},
                {"municipality_id": item["municipality_id"]},
                {"locality_id": item["locality_id"]},
            )
            .one_or_none(conn=conn)
            .as_dict()
        )

        return response
