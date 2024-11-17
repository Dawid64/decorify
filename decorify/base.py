""" Base Module with decorator structurer """
from typing import Any, Callable


def decorator(dec: Callable):
    def inner_func(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return dec(__func__=args[0])

        def wrapped_func(func: Callable):
            return dec(*args, **kwargs, __func__=func)
        return wrapped_func
    return inner_func


class _DecoratorMetaClass(type):
    """
    Metaclass to enable creation of class-based decorators.

    This metaclass allows the class to be used as decorator with or without arguments.

    Using decorator with arguments:
        - the __init__ method is called with passed arguments.
        - the __call__ method is called with the function to be decorated.

    Using decorator without arguments:
        - the __init__ method is called without any arguments (arguments takes default values).
        - the __call__ method is called with the function to be decorated.
    """
    def __call__(cls, *args, **kwargs):
        if args and isinstance(args[0], Callable) and len(args) == 1 and not kwargs:
            instance = cls.__new__(cls)
            instance.__init__()
            return instance.__call__(*args, **kwargs)
        return super().__call__(*args, **kwargs)
