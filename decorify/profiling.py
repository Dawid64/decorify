from functools import wraps
import traceback
import sys
from typing import List, Optional
from decorify.base import decorator


class Tree:
    """
    Tree-based structure
    """

    def __init__(self, name: str, parent: Optional["Tree"] = None):
        self.name = name
        self.parent = parent
        self.childrens: List[Tree] = []

    def to_list(self):
        if not self.childrens:
            return self.name
        return [self.name, [child.to_list() for child in self.childrens]]


@decorator
def crawler(build_ins: bool = False, as_list: bool = False, __func__=None):
    trace_tree: Tree = Tree('Base')
    head: Tree = trace_tree

    def profiler(call_stack, event, arg):
        nonlocal head
        if event == 'call':
            name = traceback.extract_stack(call_stack)[-1].name
            new_tree = Tree(name, head)
            head.childrens.append(new_tree)
            head = new_tree
        elif build_ins and event == 'c_call':
            new_tree = Tree(arg.__name__, head)
            head.childrens.append(new_tree)
            head = new_tree
        elif event == 'return':
            head = head.parent
        elif build_ins and event == 'c_return':
            head = head.parent

    @wraps(__func__)
    def inner(*args, **kwargs):
        current_profiler = sys.getprofile()
        sys.setprofile(profiler)
        res = __func__(*args, **kwargs)
        sys.setprofile(current_profiler)
        func_trace = trace_tree.childrens[0]
        if as_list:
            return func_trace.to_list()
        return res

    return inner
