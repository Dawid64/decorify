""" Module for profiling operations """
from functools import wraps
import logging
import traceback
import sys
from typing import List, Literal, Optional
from decorify.base import decorator


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


@decorator
def crawler(c_calls: bool = False, return_type: Literal['Tree', 'List', 'Logger', 'Print'] = 'Print', logger: logging.Logger = None, __func__=None):
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


@crawler(c_calls=True)
def test():
    test_tree = Tree('Base')

    def test_func():
        test_tree = Tree('Base')
        test_tree.childrens.append(Tree('A', test_tree))
        test_tree.childrens.append(Tree('B', test_tree))
        test_tree.childrens[0].childrens.append(
            Tree('AA', test_tree.childrens[0]))
        test_tree.childrens[0].childrens.append(
            Tree('AB', test_tree.childrens[0]))
        test_tree.childrens[1].childrens.append(
            Tree('BA', test_tree.childrens[1]))
        test_tree.childrens[1].childrens.append(
            Tree('BB', test_tree.childrens[1]))
        return test_tree
    tree = test_func()
    sum([1, 2, 3])
    return 1


if __name__ == '__main__':
    test()
