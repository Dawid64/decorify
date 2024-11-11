from functools import wraps
from typing import Callable
from .base import decorator


@decorator
def retry(func: Callable, max_retries:int=5):
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
    @wraps(func)
    def wrapper(*args, **kwargs):
        tries = 0 
        while tries < max_retries:
            try:
                return func(*args, **kwargs)
            except:
                tries += 1  
        return None
    return wrapper

import random

@decorator
def loop(func: Callable, n:int=5):
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
    @wraps(func)
    def wrapper(*args, **kwargs):
        values = []
        for i in range(n):
            values.append(func(*args,**kwargs))
        return values
    return wrapper

@decorator
def average(func: Callable, n:int=5):
    """
    Decorator for calculating average value of function ran n times (function should return int or float values)
    Parameters
    ----------       
    n: int
        Number of times the function should be executed
    Returns
    -------
    float
        Average value of the function values
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        values = []
        for _ in range(n):
            values.append(func(*args,**kwargs))
        try:
            return sum(values) / n 
        except Exception as e:
            raise ValueError("One or more of the returns of the functino is invalid")
    return wrapper


