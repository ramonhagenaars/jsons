from datetime import timezone, timedelta

from jsons._load_impl import load


def default_timezone_deserializer(obj: dict,
                                  cls: type = timezone,
                                  **kwargs) -> timezone:
    """
    Deserialize a dict to a timezone instance.
    :param obj: the dict that is to be deserialized.
    :param cls: not used.
    :param kwargs: not used.
    :return: a ``datetime.timezone`` instance.
    """
    return timezone(load(obj['offset'], timedelta), obj['name'])
