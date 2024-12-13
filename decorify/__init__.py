"""
# Decorify
Python Library for decorators


Decorify  is a lightweight Python library without any dependencies that offers a collection of simple, reusable decorators to enhance your functions. These decorators cover common use cases like logging, timing, retrying, and more.
"""
from decorify.base import decorator
from decorify.basic import timeit, grid_search, timeout, rate_limiter, time_limiter
from decorify.exceptions import default_value, validate_typehints
from decorify.io_redirect import mute, redirect
from decorify.profiling import crawler

__all__ = ['decorator', 'timeit', 'grid_search', 'timeout', 'mute', 'redirect',
           'rate_limiter', 'time_limiter', 'default_value', 'validate_typehints', 'crawler']

__version__ = '0.1.2'
