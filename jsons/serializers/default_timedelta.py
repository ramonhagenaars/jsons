from datetime import timedelta


def default_timedelta_serializer(obj: timedelta, **kwargs) -> float:
    """
    Serialize the given timedelta instance to a float holding the total
    seconds.
    :param obj: the timedelta instance that is to be serialized.
    :param kwargs: not used.
    :return: ``timedelta`` as a float.
    """
    return obj.total_seconds()
