from datetime import date
import re

from jsons._date_impl import get_date_inst, DATE_PARSE_PATTERN


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
    pattern = DATE_PARSE_PATTERN
    date = obj.split('T')[0]
    
    return get_date_inst(date, pattern)
