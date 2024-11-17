import time
from decorify.tagging import Tag


def test_tagging():
    @Tag('name')
    def remo(a, b):
        return a + b

    @Tag('name')
    def demo(a, b):
        return a * b

    @Tag
    def dif(a, b):
        return a - b

    assert demo in Tag('name').tolist()
    assert remo in Tag('name').tolist()
    assert dif in Tag().tolist()


def test_tag_mp():
    Tag.clear()

    @Tag('name')
    def remo(a, b):
        return a + b

    @Tag('name')
    def demo(a, b):
        return a * b
    res = Tag('name').call_all(1, 2)
    assert res == [3, 2]
