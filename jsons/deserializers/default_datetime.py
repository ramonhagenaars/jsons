import datetime
import re

from jsons._datetime_impl import get_datetime_inst, RFC3339_DATETIME_PATTERN


def default_datetime_deserializer(obj: str,
                                  cls: type = datetime,
                                  **kwargs) -> datetime:
    """
    Deserialize a string with an RFC3339 pattern to a datetime instance.
    :param obj: the string that is to be deserialized.
    :param cls: not used.
    :param kwargs: not used.
    :return: a ``datetime.datetime`` instance.
    """
    pattern = RFC3339_DATETIME_PATTERN
    if '.' in obj:
        pattern += '.%f'
        # strptime allows a fraction of length 6, so trip the rest (if exists).
        regex_pattern = re.compile(r'(\.[0-9]+)')
        frac = regex_pattern.search(obj).group()
        obj = obj.replace(frac, frac[0:7])
    return get_datetime_inst(obj, pattern)
