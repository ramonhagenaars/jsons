from datetime import date

from jsons._datetime_impl import to_str, RFC3339_DATE_PATTERN


def default_date_serializer(obj: date, **kwargs) -> str:
    """
    Serialize the given date instance to a string. It uses the RFC3339
    pattern. If date is a localtime, an offset is provided. If date is
    in UTC, the result is suffixed with a 'Z'.
    :param obj: the date instance that is to be serialized.
    :param kwargs: not used.
    :return: ``date`` as an RFC3339 string.
    """
    return to_str(obj, False, kwargs['fork_inst'],
                  RFC3339_DATE_PATTERN)
