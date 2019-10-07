from datetime import timedelta


def default_timedelta_deserializer(obj: float,
                                   cls: type = float,
                                   **kwargs) -> timedelta:
    """
    Deserialize a float to a timedelta instance.
    :param obj: the float that is to be deserialized.
    :param cls: not used.
    :param kwargs: not used.
    :return: a ``datetime.timedelta`` instance.
    """
    return timedelta(seconds=obj)
