from pytest import raises
from decorify.iterative import loop, retry, average


def test_loop_n():
    @loop(10)
    def add(a, b):
        return a+b
    assert add(1, 1) == [2] * 10


def test_loop_single_default():
    @loop
    def add(a, b):
        return a+b
    assert add(1, 1) == [2] * 5


def test_retry_3():
    tries = 0

    @retry(3)
    def t():
        nonlocal tries
        tries += 1
        if tries != 3:
            raise Exception
        return 'hello'

    assert t() == 'hello'
    assert tries == 3


def test_retry_failed():
    @retry(5)
    def division_by_zero():
        print(1/0)

    with raises(ZeroDivisionError):
        division_by_zero()


def test_avrage_n():
    @average(50)
    def add(a, b):
        return a+b
    print(add(2, 2))
    assert add(2, 2) == 4
