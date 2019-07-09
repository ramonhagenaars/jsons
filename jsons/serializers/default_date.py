from datetime import date
from jsons._date_impl import to_str, RFC3339_DATETIME_PATTERN


def default_date_serializer(obj: date, **kwargs) -> str:
    """
    Serialize the given datetime instance to a string. It uses the RFC3339
    pattern.
    :param obj: the datetime instance that is to be serialized.
    :param kwargs: not used.
    :return: ``date`` as an RFC3339 string.
    """
    return to_str(obj, RFC3339_DATETIME_PATTERN)
