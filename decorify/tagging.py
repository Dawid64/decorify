from decorify.base import _DecoratorMetaClass
from collections import defaultdict


class Tag(metaclass=_DecoratorMetaClass):
    """
    Tagging class to tag functions with a specific name.
    """
    _tags = defaultdict(list)

    def __init__(self, name: str = 'default'):
        self.name = name

    def __call__(self, __func__):
        self._tags[self.name].append(__func__)
        del self
        return __func__

    def __repr__(self):
        return f'Tag({self.name}={list(map(lambda x: x.__name__, self._tags[self.name]))})'

    def apply(self, *args, **kwargs):
        return [func(*args, **kwargs) for func in self._tags[self.name]]
