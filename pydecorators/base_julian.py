from functools import wraps
from typing import Callable

def decorator(dec: Callable):
    def inner_func(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return dec(args[0])

        def wrapped_func(func: Callable):
            return dec(func, *args, **kwargs)
        return wrapped_func
    return inner_func


@decorator
def modulo(func,/,mod,mod2):
    @wraps(func)
    def wrapper(*args,**kwargs):
        return func(*args,**kwargs) % mod % mod2
    return wrapper


@modulo(10,6)
def pow(a,b):
    return a**b


