""" Base Module with decorator structurer """
from typing import Callable


def decorator(dec: Callable):
    def inner_func(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return dec(__func__=args[0])

        def wrapped_func(func: Callable):
            return dec(*args, **kwargs, __func__=func)
        return wrapped_func
    return inner_func
