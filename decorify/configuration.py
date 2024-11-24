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
        def _get_defult_args_dict():
            output = dict()
            #TODO info annotation __name__ is a string not a type 
            for name,info in inspect.signature(__func__).parameters.items() :
                if info.annotation is not inspect._empty and info.default is not inspect._empty:
                    output[name] ={'type':info.annotation.__name__  if isinstance(info.annotation,type) else (info.annotation),'value':info.default} #(info.annotation.__name__  if isinstance(info.annotation,type) else info.annotation,info.default)
                elif info.annotation is not inspect._empty:
                    output[name] = info.annotation.__name__  if isinstance(info.annotation,type) else (info.annotation)     #info.annotation.__name__  if isinstance(info.annotation,type) else info.annotation
                elif info.default is not inspect._empty:
                    output[name] = info.default
                else:
                    output[name] = None
            print(output)
            return output
        def _open_file():
            if Path(path).suffix in ['.yaml','yml']:
                try:
                    import yaml
                except:
                    if isinstance(logger, logging.Logger):
                        logger.warning("Yaml packackege is not installed")
                        return __func__(*args, **kwargs)

                if not Path(path).is_file():
                    output_file = Path(path)
                    output_file.parent.mkdir(exist_ok=True, parents=True)
                    with open(path, 'w') as f:
                        yaml.safe_dump(_get_defult_args_dict(), f, default_flow_style=False)
                with open(path, 'r') as f:
                        return yaml.safe_load(f)

            if Path(path).suffix == '.txt':
                if not Path(path).is_file():
                    output_file = Path(path)
                    output_file.parent.mkdir(exist_ok=True, parents=True)
                    with open(path, 'w') as f:
                        f.write(str(_get_defult_args_dict()))
                with open(path) as f:
                    # TODO is it not a safety risk to use eval
                    return eval(f.read())

            if Path(path).suffix == '.json':
                if not Path(path).is_file():
                    print('nie ma jsona')
                    output_file = Path(path)
                    output_file.parent.mkdir(exist_ok=True, parents=True)
                    with open(path, 'w') as f:
                        json.dump(_get_defult_args_dict(), f, ensure_ascii=False, indent=4)
                    print('zapisano jsona')
                with open(path, 'r') as f:
                    return json.load(f)

                
            if Path(path).suffix == '.toml`':
                if  not Path(path).is_file():
                    output_file = Path(path)
                    output_file.parent.mkdir(exist_ok=True, parents=True)
                    with open(path, 'w') as f:
                        pass
                with open(path, 'r') as f:
                    pass

             
            if isinstance(logger, logging.Logger):
                logger.warning("Unsuported config file")
            return {}


        # checking if path is instead already a dict
        d = path if isinstance(path,dict) else _open_file()

        if d == dict():
            if isinstance(logger, logging.Logger):
                logger.warning("Configuration file not formatted properly, can't decode the dict returning the funciton without configuration")
            return __func__(*args, **kwargs)
        
        if not isinstance(d,dict):
            if isinstance(logger, logging.Logger):
                logger.warning("Configuration file not formatted properly, can't decode the dict returning the funciton without configuration")
            return __func__(*args, **kwargs)
        
        # print(f"Base: args: {args}, kwargs: {kwargs}")

        new_args = []
        current_arg = 0
        checked_args = []
        for name,info in inspect.signature(__func__).parameters.items() :
            # Checking args passed to function
            if current_arg < len(args):
                checked_args.append(name)
                if name in d and isinstance(d[name],dict) and not isinstance(args[current_arg], d[name]['type']):
                    new_args.append(d[name]['value'])
                else:
                    new_args.append(list(args)[current_arg])
                current_arg += 1
            elif name in d:
                if isinstance(d[name],dict):
                    if name not in kwargs or not isinstance(kwargs[name], d[name]['type']): 
                        kwargs[name] = d[name]['value']
                else:
                    #TODO zaimplementowac to do argow tez  i np floaty porownywac z intami jako or == 
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
def test_func(a,b:int=2,c=4,d:float|None=0.3):
    print(a,b,c,d)
    return a + b + c + d


@dictconfig
def test_func(a,b,c,d):
    print(a,b,c,d)
    return a + b + c + d


print(test_func(d=1))