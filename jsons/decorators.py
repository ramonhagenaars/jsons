"""
This module contains decorators that facilitate the `jsons` functions in an
alternative fashion.
"""
from inspect import signature, Parameter, isawaitable, iscoroutinefunction

from jsons import JsonSerializable, dump, load, loads, loadb, dumps, dumpb
from jsons.exceptions import InvalidDecorationError


def loaded(
        parameters=True,
        returnvalue=True,
        fork_inst=JsonSerializable,
        loader=load,
        **kwargs):
    """
    Return a decorator that can call `jsons.load` upon all parameters and the
    return value of the decorated function.


    **Example**:

    >>> from datetime import datetime
    >>> @loaded()
    ... def func(arg: datetime) -> datetime:
    ...     # arg is now of type datetime.
    ...     return '2018-10-04T21:57:00Z'  # This will become a datetime.
    >>> res = func('2018-10-04T21:57:00Z')
    >>> type(res).__name__
    'datetime'

    :param parameters: determines whether parameters should be taken into
    account.
    :param returnvalue: determines whether the return value should be taken
    into account.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :param kwargs: any keyword arguments that should be passed on to
    `jsons.load`
    :param loader: the load function which must be one of (``load``,
    ``loads``, ``loadb``)
    :return: a decorator that can be placed on a function.
    """
    if loader not in (load, loads, loadb):
        raise InvalidDecorationError("The 'loader' argument must be one of: "
                                     "jsons.load, jsons.loads, jsons.loadb")
    return _get_decorator(parameters, returnvalue, fork_inst, loader, kwargs)


def dumped(
        parameters=True,
        returnvalue=True,
        fork_inst=JsonSerializable,
        dumper=dump,
        **kwargs):
    """
    Return a decorator that can call `jsons.dump` upon all parameters and the
    return value of the decorated function.


    **Example**:

    >>> from datetime import datetime
    >>> @dumped()
    ... def func(arg):
    ...     # arg is now of type str.
    ...     return datetime.now()
    >>> res = func(datetime.now())
    >>> type(res).__name__
    'str'

    :param parameters: determines whether parameters should be taken into
    account.
    :param returnvalue: determines whether the return value should be taken
    into account.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :param kwargs: any keyword arguments that should be passed on to
    `jsons.dump`
    :param dumper: the dump function which must be one of (``dump``,
    ``dumps``, ``dumpb``)
    :return: a decorator that can be placed on a function.
    """
    if dumper not in (dump, dumps, dumpb):
        raise InvalidDecorationError("The 'dumper' argument must be one of: "
                                     "jsons.dump, jsons.dumps, jsons.dumpb")
    return _get_decorator(parameters, returnvalue, fork_inst, dumper, kwargs)


def _get_decorator(parameters, returnvalue, fork_inst, mapper, mapper_kwargs):
    def _decorator(decorated):
        _validate_decoration(decorated, fork_inst)
        args = [decorated, parameters, returnvalue,
                fork_inst, mapper, mapper_kwargs]
        wrapper = (_get_async_wrapper(*args) if iscoroutinefunction(decorated)
                   else _get_wrapper(*args))
        return wrapper

    return _decorator


def _get_wrapper(
        decorated,
        parameters,
        returnvalue,
        fork_inst,
        mapper,
        mapper_kwargs):
    def _wrapper(*args, **kwargs):
        result = _run_decorated(decorated, mapper if parameters else None,
                                fork_inst, args, kwargs, mapper_kwargs)
        if returnvalue:
            result = _map_returnvalue(result, decorated, fork_inst, mapper,
                                      mapper_kwargs)
        return result

    return _wrapper


def _get_async_wrapper(
        decorated,
        parameters,
        returnvalue,
        fork_inst,
        mapper,
        mapper_kwargs):
    async def _async_wrapper(*args, **kwargs):
        result = _run_decorated(decorated, mapper if parameters else None,
                                fork_inst, args, kwargs, mapper_kwargs)
        if isawaitable(result):
            result = await result
        if returnvalue:
            result = _map_returnvalue(result, decorated, fork_inst, mapper,
                                      mapper_kwargs)
        return result

    return _async_wrapper


def _get_params_sig(args, func):
    sig = signature(func)
    params = sig.parameters
    param_names = [param_name for param_name in params]
    result = [(args[i], params[param_names[i]]) for i in range(len(args))]
    return result


def _map_args(args, decorated, fork_inst, mapper, mapper_kwargs):
    params_sig = _get_params_sig(args, decorated)
    new_args = []
    for arg, sig in params_sig:
        if sig.name in ('self', 'cls') and hasattr(arg, decorated.__name__):
            # `decorated` is a method and arg is either `self` or `cls`.
            new_arg = arg
        else:
            cls = sig.annotation if sig.annotation != Parameter.empty else None
            new_arg = mapper(arg, cls=cls, fork_inst=fork_inst,
                             **mapper_kwargs)

        new_args.append(new_arg)
    return new_args


def _map_returnvalue(returnvalue, decorated, fork_inst, mapper, mapper_kwargs):
    return_annotation = signature(decorated).return_annotation
    cls = return_annotation if return_annotation != Parameter.empty else None
    result = mapper(returnvalue, cls=cls, fork_inst=fork_inst, **mapper_kwargs)
    return result


def _run_decorated(decorated, mapper, fork_inst, args, kwargs, mapper_kwargs):
    new_args = args
    if mapper:
        new_args = _map_args(args, decorated, fork_inst, mapper, mapper_kwargs)
    result = decorated(*new_args, **kwargs)
    return result


def _validate_decoration(decorated, fork_inst):
    if isinstance(decorated, staticmethod):
        fork_inst._warn('You cannot decorate a static- or classmethod. '
                        'You can still obtain the desired behavior by '
                        'decorating your method first and then place '
                        '@staticmethod/@classmethod on top (switching the '
                        'order).', 'decorated-static')
        raise InvalidDecorationError(
            'Cannot decorate a static- or classmethod.')
    if isinstance(decorated, type):
        raise InvalidDecorationError('Cannot decorate a class.')
