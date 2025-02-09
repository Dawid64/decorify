""" Module with a way to configure function values"""

from functools import wraps
from inspect import signature
from logging import Logger
from typing import Optional, Callable
from pathlib import Path
from sys import version_info 
from json import load as json_load
from .base import decorator
from .exceptions import validate_typehints

@decorator
def configure(path: str|dict|None = None, *, logger: Optional[Logger] = None, __func__: Callable = None) -> Callable:
    """
    Decorator for configuring function values from a file or a dictionary.

    This decorator reads configuration data from the provided source and applies
    it to the decorated function's arguments.
    The order of poisitonal arguments is preserved.
    
    Files supported: .yaml, .yml, .txt, .toml, .json

    ## Parameters
    path: str|dict - path to the file with configuration or dict with configuration 
    logger: logging.Logger - optional logger to log warnings

    ## Returns
    function - Wrapped function with configured values

    
    ### Configuration
    - If an positional argument wasn't defined in the function call it will be passed as keyword argument from configuration if defined,
    otherwise a ValueError will be raised.
    - If the argument is already defined in the function call it will not be overwritten by the configuration.
    - If argument's passed in the function call and the ones that configuration overwrites are don't match the typehints, 
    the function will raise a ValueError.

    ### File
    - If the file is not found, not formatted properly or not supported the function will be returned without configuration.
    - If yaml library is not insllled or python version is <3.11 and toml is not installed logs that's the library missing
      and returns the function without configuration.
    """
    @wraps(__func__)
    def wrapper(*args, **kwargs):
        config = path if isinstance(path,dict) else _open_file(path, logger)
        if not isinstance(config,dict):
            if isinstance(logger,Logger):
                logger.warning("Configuration file not formatted properly, can't decode the dict returning the funciton without configuration")
            return __func__(*args, **kwargs)   

        for name, info in list(signature(__func__).parameters.items())[len(args):]:
            if name not in kwargs and name in config: 
                kwargs[name] = config[name]

        return validate_typehints(__func__)(*args, **kwargs)
    return wrapper

def _open_file(path, logger: Optional[Logger] = None):
    """
    Opens the file and retunrs a dict with values
    Files supported: .yaml, .yml, .txt, .toml, .json
    """
    if not Path(path).is_file():
        if isinstance(logger, Logger):
            logger.warning("Configuration file not found, returning the function without configuration")
        return {}

    match Path(path).suffix:
        case '.yaml' | '.yml':
            try:
                import yaml
            except:
                if isinstance(logger,Logger):
                    logger.warning("Yaml packackege is not installed, you can instal it using 'pip install pyyaml', returning the function without configuration")
                return {}
            with open(path, 'r') as f:
                return yaml.load(f, Loader=yaml.FullLoader)

        case '.txt':
            with open(path, 'r') as f:
                return eval(f.read())
            
        case '.toml':
            if version_info >=  (3, 11):  # Python 3.11+
                import tomllib as toml
            else:
                try:
                    import toml
                except:
                    if isinstance(logger, Logger):
                        logger.warning("Toml packackege is not installed, you can instal it using 'pip install toml' or upgrade to python 3.11+ to have it in standard libraries, returning the function without configuration")
                    return {}
            with open(path, 'rb') as f:
                return toml.load(f)
            
        case '.json':
            with open(path, 'r') as f:
                return json_load(f)
        case _: 
            if isinstance(logger, Logger):
                logger.warning("Unsuported config file type, returning the function without configuration")
            return {}
