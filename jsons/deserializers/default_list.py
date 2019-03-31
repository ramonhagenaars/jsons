from jsons._main_impl import load


def default_list_deserializer(obj: list, cls: type = None, **kwargs) -> list:
    """
    Deserialize a list by deserializing all items of that list.
    :param obj: the list that needs deserializing.
    :param cls: the type optionally with a generic (e.g. List[str]).
    :param kwargs: any keyword arguments.
    :return: a deserialized list instance.
    """
    cls_ = None
    kwargs_ = {**kwargs}
    if cls and hasattr(cls, '__args__'):
        cls_ = cls.__args__[0]
        # Mark the cls as 'inferred' so that later it is known where cls came
        # from and the precedence of classes can be determined.
        kwargs_['_inferred_cls'] = True
    return [load(x, cls_, **kwargs_) for x in obj]
