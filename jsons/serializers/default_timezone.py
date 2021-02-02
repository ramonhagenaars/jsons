from datetime import timezone

from jsons._dump_impl import dump


def default_timezone_serializer(obj: timezone, **kwargs) -> dict:
    """
    Serialize the given timezone instance to a dict holding the total
    seconds.
    :param obj: the timezone instance that is to be serialized.
    :param kwargs: not used.
    :return: ``timezone`` as a dict.
    """
    name = obj.tzname(None)
    offset = dump(obj.utcoffset(None), **kwargs)
    return {
        'name': name,
        'offset': offset
    }
