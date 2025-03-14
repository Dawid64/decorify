""" Module for profiling operations """
from functools import wraps
import logging
import traceback
import sys
from typing import List, Literal, Optional, Callable, Any
from decorify.base import decorator
import gc # python garbage collector
import tracemalloc # python memory profiler


def generate_ascii_tree(item, prefix='', is_last=False, is_root=True):
    """Recursively generates ASCII tree from nested list."""

    # TODO: can be changed into iterative approach
    text = ''
    if isinstance(item, list):
        node = item[0]
        children = item[1:]
    else:
        node = item
        children = []

    if is_root:
        text += node + '\n'
        child_prefix = ''
    else:
        connector = '└── ' if is_last else '├── '
        text += prefix + connector + node + '\n'
        child_prefix = prefix + ('    ' if is_last else '│   ')

    last_child_index = len(children) - 1
    for idx, child in enumerate(children):
        is_child_last = idx == last_child_index
        text += generate_ascii_tree(child, child_prefix,
                                    is_child_last, is_root=False)
    return text


class Tree:
    """
    Minimalistic tree structure, created for the purpose of `decorify.crawler`.
    Each Node containes: name, parent, childrens
    Methods: to_list - transforms tree structure into nested lists that can be passed to `decorify.profiling.generate_ascii_tree` function.
    """

    def __init__(self, name: str, parent: Optional["Tree"] = None):
        self.name = name
        self.parent = parent
        self.childrens: List[Tree] = []

    def to_list(self):
        if not self.childrens:
            return [self.name]
        return [self.name, *[child.to_list() for child in self.childrens]]

    def __repr__(self):
        return generate_ascii_tree(self.to_list())

    def remove_dunders(self):
        if self.name.startswith('__'):
            return
        new_childrens = []
        for child in self.childrens:
            if child.remove_dunders():
                new_childrens.append(child)
        self.childrens = new_childrens
        return True


@decorator
def crawler(c_calls: bool = False, show_dunder_methods: bool = True, return_type: Literal['Tree', 'List', 'Logger', 'Print'] = 'Print', logger: logging.Logger = None, __func__=None):
    """
    ## Crawler
    Decorator for finding structure of the function.
    It creates profiler that substitutes current profiler and looks for functions calls.
    Based on the calls and returns profiler generates tree-like structure.
    The output can be either passed as an `decorify.profiling.Tree` a minimalistic tree structure or a nested list.
    #### Crawler shoul not be used:
    - On a recursive function
    - When other profiler is enabled
    - When Exception or Error is going to be raised

    **!! Note: The crawler may significantly slow down the function, it's recommended for debugging learning purposes !!**

    Parameters
    ----------
    c_calls : bool
        If enabled crawler also looks for C calls, by default False
    show_dunder_methods : bool
        If disabled crawler does not display dunder methods, by default True
    return_type : Literal['Tree', 'List', 'Logger', 'Print']
        Type of the output, by default 'Print':
        - 'Tree' - returns `decorify.profiling.Tree` structure
        - 'List' - returns python nested list
        - 'Logger' - messages logger with tree structure (remember to enable logging)
        - 'Print' - prints tree structure
    logger : logging.Logger
        If return_type is 'Logger' to specify logger, if left None it uses root logger, by default None

    Returns
    -------
    Callable
        Wrapped function returning tree structure, nested list or default results depending on return_type parameter.
        If return_type is "Tree" it returns `decorify.profiling.Tree` structure, if "List" it returns python nested list.
    """

    # TODO: Add support for exceptions
    trace_tree: Tree = Tree('Base')
    head: Tree = trace_tree
    if return_type == 'Logger' and logger is None:
        logger = logging.getLogger()

    def profiler(call_stack, event, arg):
        nonlocal head
        if event == 'call':
            name = traceback.extract_stack(call_stack)[-1].name
            new_tree = Tree(name, head)
            head.childrens.append(new_tree)
            head = new_tree
        elif event == 'return':
            head = head.parent
        elif c_calls and event == 'c_call':
            new_tree = Tree(arg.__name__, head)
            head.childrens.append(new_tree)
            head = new_tree
        elif c_calls and event == 'c_return':
            head = head.parent

    @wraps(__func__)
    def inner(*args, **kwargs):
        current_profiler = sys.getprofile()
        sys.setprofile(profiler)
        res = __func__(*args, **kwargs)
        sys.setprofile(current_profiler)
        nonlocal trace_tree, head
        func_trace = trace_tree.childrens[0]
        trace_tree = Tree('Base')
        head = trace_tree
        if not show_dunder_methods:
            func_trace.remove_dunders()
        if return_type == 'List':
            return func_trace.to_list()
        if return_type == 'Tree':
            return func_trace
        if return_type == 'Print':
            print(func_trace)
        if return_type == 'Logger':
            logger.info('test')
        return res

    return inner

def track_leaks(__func__: Callable[..., Any]) -> Callable[..., tuple[Any, int]]:
    """Decorator for finding memory leaks. 
    It utilizes Python's gc module to track objects before and after function 
    call. The decorator returns a tuple of function's output and number of 
    leaked objects.

    Parameters
    ----------
    __func__: Callable[..., Any] 
        The function to wrap. Defaults to None.

    Returns
    -------
    Callable[..., tuple[Any, int]]
        Wrapped function that returns a tuple of function's output and number of
        leaked objects.
    """
    @wraps(__func__)
    def inner_func(*args, **kwargs) -> tuple[Any, int]:
        # enable garbage collector
        gc_enabled = gc.isenabled()
        if not gc_enabled:
            gc.enable()
        # track objects
        tracked = len(gc.get_objects())
        result = __func__(*args, **kwargs)
        # find leaked objects
        leaked = len(gc.get_objects()) - tracked
        if not gc_enabled:
            gc.disable()
        return result, leaked
    return inner_func

def measure_memory_usage(__func__: Callable[..., Any]) -> Callable[..., tuple[Any, int]]:
    """Decorator for measuring memory usage. The decorator returns a tuple of 
    function's output and peak memory usage in bytes.

    Args:
    __func__: Callable[..., Any]
        The function to wrap. Defaults to None.

    Returns:
    Callable[..., tuple[Any, int]]
        Wrapped function that returns a tuple of function's output and memory 
        usage in bytes.
    """
    @wraps(__func__)
    def inner_func(*args, **kwargs) -> tuple[Any, int]:
        tracing = tracemalloc.is_tracing()
        if not tracing:
            tracemalloc.start()
        start_current, _ = tracemalloc.get_traced_memory()
        result = __func__(*args, **kwargs)
        _, peak = tracemalloc.get_traced_memory()
        if not tracing:
            tracemalloc.stop()
        return result, peak - start_current
    return inner_func
