from pathlib import PurePath


def default_path_serializer(obj: PurePath, **kwargs) -> str:
    """
    Serialize a ``pathlib.PurePath`` object to a ``str``, Posix-style.

    Posix-style strings are used as they can be used to create ``pathlib.Path``
    objects on both Posix and Windows systems, but Windows-style strings can
    only be used to create valid ``pathlib.Path`` objects on Windows.
    :param obj: the path to serialize.
    :param kwargs: not used.
    :return: a ``str``.
    """
    return obj.as_posix()
