from typing import Optional, Callable
from typish import get_type
from jsons._common_impl import get_class_name
from jsons._dump_impl import dump
from jsons.exceptions import RecursionDetectedError, SerializationError


def default_dict_serializer(
        obj: dict,
        cls: Optional[type] = None,
        *,
        strict: bool = False,
        strip_nulls: bool = False,
        key_transformer: Optional[Callable[[str], str]] = None,
        **kwargs) -> dict:
    """
    Serialize the given ``obj`` to a dict of serialized objects.
    :param obj: the dict that is to be serialized.
    :param cls: the type of ``obj``; ``obj`` is dumped as if of that type.
    :param strict: if ``True`` the serialization will raise upon any the
    failure of any attribute. Otherwise it continues with a warning.
    :param strip_nulls: if ``True`` the resulting dict will not contain null
    values.
    :param key_transformer: a function that will be applied to all keys in the
    resulting dict.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a dict of which all elements are serialized.
    """
    result = dict()
    fork_inst = kwargs['fork_inst']
    for key in obj:
        dumped_elem = None
        try:
            dumped_elem = dump(obj[key],
                               key_transformer=key_transformer,
                               strip_nulls=strip_nulls, **kwargs)

            _store_cls_info(dumped_elem, key, obj, **kwargs)

        except RecursionDetectedError:
            fork_inst._warn('Recursive structure detected in attribute "{}" '
                            'of object of type "{}", ignoring the attribute.'
                            .format(key, get_class_name(cls)))
        except SerializationError as err:
            if strict:
                raise
            else:
                fork_inst._warn('Failed to dump attribute "{}" of object of '
                                'type "{}". Reason: {}. Ignoring the '
                                'attribute.'
                                .format(key, get_class_name(cls), err.message))
                break
        if not (strip_nulls and dumped_elem is None):
            if key_transformer:
                key = key_transformer(key)
            result[key] = dumped_elem
    return result


def _store_cls_info(result: object, attr: str, original_obj: dict, **kwargs):
    if isinstance(result, dict) and kwargs.get('_store_cls'):
        cls = get_type(original_obj[attr])
        if cls.__module__ == 'typing':
            cls_name = repr(cls)
        else:
            cls_name = get_class_name(cls, fully_qualified=True,
                                      fork_inst=kwargs['fork_inst'])
        result['-cls'] = cls_name
