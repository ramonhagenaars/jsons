"""
Contains the classes that may be raised by jsons.
"""
from json import JSONDecodeError


class JsonsError(Exception):
    """
    Base class for all `jsons` errors.
    """
    def __init__(self, message: str):
        """
        Constructor.
        :param message: the message describing the problem.
        """
        Exception.__init__(self, message)


class ArgumentError(JsonsError, ValueError):
    """
    Raised when serialization or deserialization went wrong caused by a wrong
    argument when serializing or deserializing.
    """
    def __init__(self, message: str, argument: str):
        """
        Constructor.
        :param message: the message describing the problem.
        :param argument: the name of the argument in question.
        """
        JsonsError.__init__(self, message)
        ValueError.__init__(self, message)
        self._argument = argument

    @property
    def argument(self) -> str:
        """
        The argument in question.
        :return: the name of the argument.
        """
        return self._argument


class DeserializationError(JsonsError):
    """
    Raised when deserialization failed for some reason.
    """
    def __init__(self, message: str, source: object, target: type):
        """
        Constructor.
        :param message: the message describing the problem.
        :param source: the object that was to be deserialized.
        :param target: the type to which `source` was to be deserialized.
        """
        JsonsError.__init__(self, message)
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


class SerializationError(JsonsError):
    """
    Raised when serialization failed for some reason.
    """


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
        DeserializationError.__init__(self, message, source, target)
        JSONDecodeError.__init__(self, message, error.doc, error.pos)


class UnfulfilledArgumentError(DeserializationError, ArgumentError):
    """
    Raised on a deserialization failure when an argument could not be fulfilled
    by the given object attr_getter.
    """
    def __init__(self,
                 message: str,
                 argument: str,
                 source: object,
                 target: type):
        """
        Constructor.
        :param message: the message of this error.
        :param argument: the argument that was unfulfilled.
        :param source: the object that was to be deserialized.
        :param target: the type to which `source` was to be deserialized.
        """
        DeserializationError.__init__(self, message, source, target)
        ArgumentError.__init__(self, message, argument)


class SignatureMismatchError(DeserializationError, ArgumentError):
    def __init__(self,
                 message: str,
                 argument: str,
                 source: object,
                 target: type):
        DeserializationError.__init__(self, message, source, target)
        ArgumentError.__init__(self, message, argument)


class InvalidDecorationError(JsonsError):
    """
    Raised when a jsons decorator was wrongly used.
    """
    def __init__(self, message: str):
        """
        Constructor.
        :param message: the message of this error.
        """
        JsonsError.__init__(self, message)
