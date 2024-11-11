from pydecorators.iterative import loop,retry,average


def test_loop_n():
    @loop(10)
    def add(a,b):
        return a+b
    assert add(1,1) == [2] * 10

def test_loop_single_default():
    @loop
    def add(a,b):
        return a+b
    assert add(1,1) == [2] * 5

def test_retry_3():
    tries = 0 
    @retry(3)
    def t():
        nonlocal tries
        tries+=1
        if tries != 3:
            raise Exception
        return None

    assert t() == None and tries == 3

# TODO test if numpyworks, check if ValueError shows properly

def test_avrage_n():
    @average(50)
    def add(a,b):
        return a+b
    print(add(2,2))
    assert add(2,2) == 4

