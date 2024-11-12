from functools import wraps
from typing import Callable
from .base import decorator


@decorator
def retry(max_retries: int = 5, *, __func__: Callable = None):
    """
    Decorator for running the function until it suceeds or number of tires exceeds max retries

    Parameters
    ----------       
    max_retries: int
        Maximal number of retries 

    Returns
    -------
    function
        Wrapped function or None if the number of tries exceeds max retries 

    """
    @wraps(__func__)
    def wrapper(*args, **kwargs):
        tries = 0
        while tries < max_retries:
            try:
                return __func__(*args, **kwargs)
            except Exception as e:
                tries += 1
                if tries == max_retries:
                    raise e
        return None
    return wrapper


@decorator
def loop(n: int = 5, *, __func__: Callable = None):
    """
    Decorator for running the function n times

    Parameters
    ----------       
    n: int
        Number of times the function should be executed

    Returns
    -------
    list
        List with return values of the function
    """
    @wraps(__func__)
    def wrapper(*args, **kwargs):
        values = []
        for i in range(n):
            values.append(__func__(*args, **kwargs))
        return values
    return wrapper


@decorator
def average(n: int = 5, __func__: Callable = None):
    """
    Decorator for calculating average value of function ran n times (function output should be addable and divisble by an integer)

    Parameters
    ----------       
    n: int
        Number of times the function should be executed

    Returns
    -------
    float
        Average value of the function values
    """
    @wraps(__func__)
    def wrapper(*args, **kwargs):
        values = []
        for _ in range(n):
            values.append(__func__(*args, **kwargs))
        return sum(values) / n
    return wrapper
