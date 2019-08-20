
def singleton(cls):
    """Simple singleton implementation by replacing the class
    with the instance.
    This makes it easy to import and use it.
    """
    return cls()
