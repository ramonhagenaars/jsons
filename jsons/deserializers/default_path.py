from pathlib import PurePath


def default_path_deserializer(obj: str, cls: type = PurePath, **kwargs) -> PurePath:
    """
    Deserialize a string to a `pathlib.PurePath` object. Since ``pathlib``
    implements ``PurePath``, no filename or existence checks are performed.
    :param obj: the string to deserialize.
    :param kwargs: not used.
    :return: a ``str``.
    """
    return cls(obj)
