"""
Contains the classes that may be raised by jsons.
"""
from json import JSONDecodeError


class DeserializationError(Exception):
    """
    Raised when deserialization failed for some reason.
    """
    def __init__(self, source: object, target: type):
        """
        Constructor.
        :param source: the object that was to be deserialized.
        :param target: the type to which `source` was to be deserialized.
        """
        self._source = source
        self._target = target

    @property
    def source(self) -> object:
        """
        The object that was to be deserialized.
        :return: the object that was to be deserialized.
        """
        return self._source

    @property
    def target(self) -> type:
        """
        The target type to which `source` was to be deserialized.
        :return: the type to which `source` was to be deserialized.
        """
        return self._target


class DecodeError(DeserializationError, JSONDecodeError):
    """
    Raised when decoding a string or bytes to Python types failed. This error
    is actually a wrapper around `json.JSONDecodeError`.
    """
    def __init__(self, message: str, source: object, target: type,
                 error: JSONDecodeError):
        """
        Constructor.
        :param message: the message of this error.
        :param source: the object that was to be deserialized.
        :param target: the type to which `source` was to be deserialized.
        :param error: the wrapped `JSONDecodeError`.
        """
        DeserializationError.__init__(self, source, target)
        JSONDecodeError.__init__(self, message, error.doc, error.pos)


class UnfulfilledArgumentError(DeserializationError, ValueError):
    """
    Raised on a deserialization failure when an argument could not be fulfilled
    by the given object attr_getter.
    """
    def __init__(self, message: str, argument: str, source: object,
                 target: type):
        """
        Constructor.
        :param message: the message of this error.
        :param argument: the argument that was unfulfilled.
        :param source: the object that was to be deserialized.
        :param target: the type to which `source` was to be deserialized.
        """
        ValueError.__init__(self, message)
        DeserializationError.__init__(self, source, target)
        self._argument = argument

    @property
    def argument(self) -> str:
        """
        The argument in question.
        :return: the name of the argument.
        """
        return self._argument


class InvalidDecorationError(Exception):
    """
    Raised when a jsons decorator was wrongly used.
    """
    def __init__(self, message: str):
        """
        Constructor.
        :param message: the message of this error.
        """
        Exception.__init__(self, message)
