from enum import Enum
from typing import List


def getEnumValues(enum_class: Enum) -> List[str]:
    return [member.value for member in enum_class]


class FilterOperatosEnum(str, Enum):
    lt = "lt"
    lte = "lte"
    eq = "eq"
    gt = "gt"
    gte = "gte"
    neq = "neq"


class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"


class UserTypeEnum(str, Enum):
    user = "user"
    admin = "admin"
    agent = "agent"


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    na = "na"
