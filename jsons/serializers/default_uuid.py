from uuid import UUID


def default_uuid_serializer(obj: UUID, **kwargs) -> str:
    """
    Serialize the given obj. By default, it is serialized as specified in RFC 4122.
    e.g. '12345678-1234-1234-1234-123456789abc'
    :param obj: an instance of an uuid.UUID.
    :param kwargs: any keyword arguments.
    :return: ``obj`` serialized as a string.
    """
    return str(obj)
