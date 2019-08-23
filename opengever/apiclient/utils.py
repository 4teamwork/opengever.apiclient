from functools import wraps


def singleton(cls):
    """Simple singleton implementation by replacing the class
    with the instance.
    This makes it easy to import and use it.
    """
    return cls()


def autowrap(func):
    """Decorator for GEVERClient methods which will autoomatically
    wrap returned items into API model objects.
    """
    @wraps(func)
    def wrapper(client, *args, raw=False, **kwargs):
        result = func(client, *args, **kwargs)
        if not raw:
            result = client.wrap(result)
        return result
    return wrapper
