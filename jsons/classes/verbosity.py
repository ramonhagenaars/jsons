try:
    from enum import Flag
except ImportError:  # pragma: no cover
    from jsons._compatibility_impl import Flag


class Verbosity(Flag):
    """
    An enum that defines the level of verbosity of the serialization of an
    object.
    """
    WITH_NOTHING = 0
    WITH_CLASS_INFO = 10
    WITH_DUMP_TIME = 20
    WITH_EVERYTHING = WITH_CLASS_INFO | WITH_DUMP_TIME

    @staticmethod
    def from_value(value: any) -> 'Verbosity':
        """
        Return a ``Verbosity`` instance from the given value.
        :param value:
        :return: a ``Verbosity`` instance corresponding to ``value``.
        """
        if isinstance(value, Verbosity):
            return value
        if value in (False, None):
            return Verbosity.WITH_NOTHING
        if value is True:
            return Verbosity.WITH_EVERYTHING
        if value:
            return Verbosity.WITH_EVERYTHING
        return Verbosity.WITH_NOTHING
