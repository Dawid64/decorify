""" Module with a way to configure function values"""
import ast
from functools import wraps
import inspect
import json
import logging
import types
from typing import Any, Callable, Optional
from base import decorator
from pathlib import Path


@decorator
def configure(path: str|dict|None = None, *, logger: Optional[logging.Logger] = None, __func__: Callable = None) -> Callable:
    """
    Decorator for configuring function values from a file

    Parameters
    ----------
    """

    @wraps(__func__)
    def wrapper(*args, **kwargs):
        def get_defult_args_dict():
            output = dict()
            #TODO info annotation __name__ is a string not a type 
            for name,info in inspect.signature(__func__).parameters.items() :
                if info.annotation is not inspect._empty and info.default is not inspect._empty:
                    output[name] = (info.annotation.__qualname__  if isinstance(info.annotation,type) else info.annotation,info.default)
                elif info.annotation is not inspect._empty:
                    output[name] =  info.annotation.__qualname__  if isinstance(info.annotation,type) else info.annotation
                elif info.default is not inspect._empty:
                    output[name] = info.default
                else:
                    output[name] = None
            return output
        def open_file():
            print('opening file')
            if Path(path).is_file():
                if Path(path).suffix in ['.yaml','yml']:
                    pass
                if Path(path).suffix == '.toml':
                    pass
                if Path(path).suffix == '.txt':
                    with open(path) as f:
                        # TODO is it not a safety risk to use eval
                        return eval(f.read())
            
            else:
                output_file = Path(path)
                output_file.parent.mkdir(exist_ok=True, parents=True)
                if Path(path).suffix == '.txt':
                    output_file.write_text(str(get_defult_args_dict()))


            pass


        d = {}
        # checking if instead of path a dict was passed as values
        if isinstance(path,dict):
           d = path
        else:
            d = open_file()

        if d == dict():
            if isinstance(logger, logging.Logger):
                logger.warning("Configuration file not formatted properly, can't decode the dict return the funciton without configuration")
            return __func__(*args, **kwargs)
        
        if not isinstance(d,dict):
            if isinstance(logger, logging.Logger):
                logger.warning("Configuration file not formatted properly, can't decode the dict return the funciton without configuration")
            return __func__(*args, **kwargs)
        
        # print(f"Base: args: {args}, kwargs: {kwargs}")

        new_args = []
        current_arg = 0
        checked_args = []
        for name,info in inspect.signature(__func__).parameters.items() :
            # Checking args passed to function
            if current_arg < len(args):
                checked_args.append(name)
                if name in d and isinstance(d[name],tuple) and not isinstance(args[current_arg], d[name][0]):
                    new_args.append(d[name][1])
                else:
                    new_args.append(list(args)[current_arg])
                current_arg += 1
            elif name in d:
                if isinstance(d[name],tuple):
                    # TODO jak sprawdza np czy jest floatem i da sie inta to zwraca ze nie jest 
                    if name not in kwargs or not isinstance(kwargs[name], d[name][0]): 
                        kwargs[name] = d[name][1]
                else:
                    if  isinstance(d[name],type):
                        kwargs[name] = d[name]()
                    elif isinstance(d[name],types.UnionType) :
                        kwargs[name] = d[name].__args__[0]()
                    else:
                        kwargs[name] = d[name]

                        


        # print(args)
        # print(kwargs)
        return  __func__(*new_args, **kwargs)


        
    
    if path is None:
        if isinstance(logger, logging.Logger):
            logger.warning('No path specified in declaration of decorator')
        return 
    return wrapper




logger = logging.getLogger('Logger testowy')
dictconfig = configure('decorify/configs/config.txt',logger=logger)


@dictconfig
def test_func(a:int,b:int,c=0,d:float|None=0.3):
    print(a,b,c,d)
    return a + b + c + d



# print(type(int|float))
print(test_func())