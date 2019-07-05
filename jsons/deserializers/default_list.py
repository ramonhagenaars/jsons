from threading import Thread
from jsons._load_impl import load
from jsons.exceptions import JsonsError


def default_list_deserializer(
        obj: list,
        cls: type = None,
        *,
        threads: int = 1,
        **kwargs) -> list:
    """
    Deserialize a list by deserializing all items of that list.
    :param obj: the list that needs deserializing.
    :param cls: the type optionally with a generic (e.g. List[str]).
    :param threads: the number of threads that is allowed to use.
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

    if threads == 1:
        func = _single_threaded
    elif threads > 1:
        func = _multi_threaded
    else:
        raise JsonsError('Invalid number of threads: {}'.format(threads))
    return func(obj, cls_, threads, **kwargs_)


def _single_threaded(
        # Load the elements of the list in a single thread.
        obj: list,
        cls: type,
        threads: int,
        **kwargs):
    return [load(x, cls, threads=1, **kwargs) for x in obj]


def _multi_threaded(
        obj: list,
        cls: type,
        threads: int,
        **kwargs):
    # Load the elements of the list with multiple threads.

    # First, create a list with the correct size for the threads to fill.
    result = [0] * len(obj)

    threads_used = min(threads, len(obj))
    threads_left = threads - threads_used or 1

    # Divide the list in parts.
    slice_size = int(len(obj) / threads_used)
    rest_size = len(obj) % threads_used

    # Start the threads and store them to join them later.
    threads_instances = []
    for i in range(threads_used):
        start = i
        end = (i + 1) * slice_size
        if i == threads_used - 1:
            end += rest_size
        thread = Thread(
            target=_fill,
            args=(obj, cls, result, start, end, threads_left, kwargs))
        thread.start()
        threads_instances.append(thread)

    for thread in threads_instances:
        thread.join()

    return result


def _fill(
        obj: list,
        cls: type,
        result: list,
        start: int,
        end: int,
        threads: int,
        kwargs: dict):
    # Fill result with the loaded objects of obj within the range start - end.
    for i_ in range(start, end):
        loaded = load(obj[i_], cls, threads=threads, **kwargs)
        result[i_] = loaded
