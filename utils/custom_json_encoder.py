import json
import datetime

from decimal import Decimal


class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, datetime.timedelta):
            return obj.total_seconds()

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        if isinstance(obj, datetime.time):
            return obj.isoformat()

        return super().default(obj)

    def iterencode(self, value):
        for chunk in super().iterencode(value):
            yield chunk.encode("utf-8")
