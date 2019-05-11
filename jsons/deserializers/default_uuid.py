from typing import Optional
from uuid import UUID


def default_uuid_deserializer(obj: str,
                              cls: Optional[type] = None,
                              **kwargs) -> UUID:
    """
    Deserialize a UUID. Expected format for string is specified in RFC 4122.
    e.g. '12345678-1234-1234-1234-123456789abc'
    :param obj: the string that is to be deserialized.
    :param cls: not used.
    :param kwargs: any keyword arguments.
    :return: the deserialized obj.
    """
    return UUID(obj)
