from typing import Callable, Optional
from .base import decorator 
from functools import wraps
import logging
import inspect


@decorator
def exception_handling_default_value(func:Callable, default_value=None,*,logger:Optional[logging.Logger]=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # TODO
            if isinstance(logger,logging.Logger):
                logger.warning(f"Set default value in function '{func.__name__}', because of '{e}'")
            return default_value

    return wrapper


@decorator
def validate_typehints(func:Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        all_arguments = dict(zip(inspect.getfullargspec(func).args,args))
        all_arguments.update(kwargs)
        for arg, anottation in func.__annotations__.items():
            if arg in all_arguments:
                assert isinstance(all_arguments[arg],anottation)
        return func(*args,**kwargs)
    return wrapper