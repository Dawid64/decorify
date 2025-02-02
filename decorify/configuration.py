""" Module with a way to configure function values"""
import ast
from functools import wraps
import inspect

import logging
import types
from typing import Any, Callable, Optional
from .base import decorator
from pathlib import Path
import sys 

import json


#TODO instead of printing wrong format raise an exception??



@decorator
def configure(path: str|dict|None = None, *, logger: Optional[logging.Logger] = None, __func__: Callable = None) -> Callable:
    """
    Decorator for configuring function values from a file or a dictionary.

    This decorator reads configuration data from the provided source and applies
    it to the decorated function's arguments, ensuring that both positional and
    keyword arguments are updated accordingly. The order of arguments is preserved.
    
    Files supported: .yaml, .yml, .txt, .toml, .json

    ## Parameters
    path: str|dict - path to the file with configuration or dict with configuration 
    logger: logging.Logger - optional logger to log warnings

    ## Returns
    function - Wrapped function with configured values

    ## Edge cases
    ### File
    - If the file is not found, not formatted properly or not supported the function will be returned without configuration.
    - If yaml library is not insllled or python version is <3.11 and toml is not installed logs that's the library missing and returns the function without configuration.
    ### Configuration
    - If the postitional argument is not found in the config file and not set in the function, an exception will be raised.
    - If the postiional argument has a different type in the config file than in the function, deafualt value will be taken if default value is set otherwise an exception will be raised.
    - If the keyword argument has a different type in the config file than in the function, deafualt value will be taken 
    """

    @wraps(__func__)
    def wrapper(*args, **kwargs):
        
        def _open_file():
            if  not Path(path).is_file():
                if isinstance(logger, logging.Logger):
                    logger.warning("Configuration file not found, returning the function without configuration")
                return {}

            match Path(path).suffix:
                case '.yaml', '.yml':
                    try:
                        import yaml
                    except:
                        if isinstance(logger, logging.Logger):
                            logger.warning("Yaml packackege is not installed, you can instal it using 'pip install pyyaml', returning the function without configuration")
                        return {}
                    with open(path, 'r') as f:
                            return yaml.safe_load(f)
                case '.txt':
                    with open(path, 'r') as f:
                        return eval(f.read())
                case '.toml':
                    
                    if sys.version_info >=  (3, 11):  # Python 3.11+
                        import tomllib as toml
                    else:
                        try:
                            import toml
                            with open(path, 'rb') as f:
                                return toml.load(f)
                        except:
                            if isinstance(logger, logging.Logger):
                                logger.warning("Toml packackege is not installed, you can instal it using 'pip install toml' or upgrade to python 3.11+ to have it in standard libraries, returning the function without configuration")
                            return {}
                    with open(path, 'rb') as f:
                        return toml.load(f)
                case '.json':
                    with open(path, 'r') as f:
                        return json.load(f)
                case _: 
                    if isinstance(logger, logging.Logger):
                        logger.warning("Unsuported config file type, returning the function without configuration")
                    return {}

        config = path if isinstance(path,dict) else _open_file()

        if not isinstance(config,dict):
            if isinstance(logger, logging.Logger):
                logger.warning("Configuration file not formatted properly, can't decode the dict returning the funciton without configuration")
            return __func__(*args, **kwargs)
        
        # Saving the order of args and kwargs 
        for i, (name,info) in enumerate(inspect.signature(__func__).parameters.items()):
            if i >= len(args):
                #kwargs and unset args
                if info.default == inspect._empty and name not in kwargs:
                    #setting to args
                    if name in config:

                        if isinstance(config[name], (int,float) if info.annotation == float else info.annotation if  info.annotation != inspect._empty else object):
                            args += (config[name],)
                        else:
                            raise ValueError(f"Argument '{name}' has diffrent type in config ({type(config[name])}) file than in function ({info.annotation})")
                    else:
                        raise Exception(f"Argument '{name}' not found in config file and not set in function")
                else:
                    #setting to kwargs
                    if name not in kwargs : 
                        if name in config:
                            if isinstance(config[name], (int,float) if info.annotation == float else info.annotation if  info.annotation != inspect._empty else object):
                                kwargs[name] = config[name]
                            else:
                                if info.default != inspect._empty:
                                    if isinstance(logger, logging.Logger):
                                        logger.warning(f"Argument '{name}' has diffrent type in config ({type(config[name])}) file than in function ({info.annotation}), using default value")
                                    kwargs[name] = info.default
                                else:
                                    raise ValueError(f"Argument '{name}' has diffrent type in config ({type(config[name])}) file than in function ({info.annotation})")
                    else:
                        if not isinstance(kwargs[name], (int,float) if info.annotation == float else info.annotation if  info.annotation != inspect._empty else object):
                            raise ValueError(f"Argument '{name}' has wrong value set in the function call")
            else:
                #args
                if not isinstance(args[i], (int,float) if info.annotation == float else info.annotation if  info.annotation != inspect._empty else object):
                    raise ValueError(f"Argument '{name}' has wrong value set in the function call") 
                
        return  __func__(*args, **kwargs)
    return wrapper

