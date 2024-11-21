from functools import wraps
import traceback
import sys
from typing import List, Optional
from decorify.base import decorator


def generate_ascit_tree(item, prefix='', is_last=False, is_root=True):
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
        text += generate_ascit_tree(child, child_prefix,
                                    is_child_last, is_root=False)
    return text


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
            return [self.name]
        return [self.name, *[child.to_list() for child in self.childrens]]

    def __repr__(self):
        return generate_ascit_tree(self.to_list())


@decorator
def crawler(build_ins: bool = False, as_list: bool = False, as_tree: bool = False, __func__=None):
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
        nonlocal trace_tree, head
        func_trace = trace_tree.childrens[0]
        trace_tree = Tree('Base')
        head = trace_tree
        if as_tree:
            return func_trace
        if as_list:
            return func_trace.to_list()
        return res

    return inner
