from datetime import date

from jsons._datetime_impl import get_datetime_inst, RFC3339_DATE_PATTERN


def default_date_deserializer(obj: str,
                              cls: type = date,
                              **kwargs) -> date:
    """
    Deserialize a string with an RFC3339 pattern to a date instance.
    :param obj: the string that is to be deserialized.
    :param cls: not used.
    :param kwargs: not used.
    :return: a ``datetime.date`` instance.
    """
    return get_datetime_inst(obj, RFC3339_DATE_PATTERN).date()
