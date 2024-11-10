from typing import Callable, Optional
from functools import wraps


def decorator(dec):
    def inner_func(func, *args, **kwargs):
        return dec(func, *args, **kwargs)


@decorator
def some_decorator(func: int, *, arg1: int = 1, arg2: int = 2) -> Callable:
    """
    Some documentation
    """
    print(func, arg1, arg2)

    def new_func(*args, **kwargs):
        ...
    return new_func


def inner_decorator(func):
    def wrapper(*args, **kwargs):
        pass
    return wrapper


def decorator(arg0, arg1):
    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            pass
        return wrapper
    return inner_decorator
