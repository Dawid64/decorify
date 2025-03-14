from decorify.profiling import crawler, Tree, generate_ascii_tree, track_leaks, measure_memory_usage
import sys


def test_profiling_stack():
    def func_a():
        return sum([1, 1])

    @crawler(return_type='List')
    def func_b():
        return func_a() + func_a()

    assert func_b() == ['func_b', ['func_a'], ['func_a']]


def test_profiling_stack_build_ins():
    def func_a():
        return sum([1, 1])

    @crawler(c_calls=True, return_type='List')
    def func_b():
        return func_a() + func_a()

    assert func_b() == ['func_b', ['func_a', ['sum']], ['func_a', ['sum']]]


def test_profiling_tree():
    def func_a():
        return sum([1, 1])

    @crawler(return_type='Tree')
    def func_b():
        return func_a() + func_a()

    assert isinstance(func_b(), Tree)


def test_ascii_generator():
    sample = ['add_1', ['add_2', ['add_2', ['add_2', ['add_2', ['add_2'], ['add_2']], ['add_2']], [
        'add_2', ['add_2'], ['add_2']]], ['add_2', ['add_2', ['add_2'], ['add_2']], ['add_2']]]]
    ascii_tree = generate_ascii_tree(sample)
    assert isinstance(ascii_tree, str)

def test_track_leaks_ok():
    @track_leaks
    def func_a():
        return sum([1, 1])
    
    _, leaked = func_a()
    assert leaked == 0
  
def test_track_leaks_leak():
    # MAYBE create our own bad C mini extension with a memory leak and test it.
    @track_leaks
    def func_leak():
        try:
            raise Exception
        except Exception:
            # the traceback retains a reference to all the variables within 
            # this context.
            _, _, tb = sys.exc_info()
            return tb # thus returning here means that memory escapes this ctx
    # not a memory leak in the traditional sense, but a leak nonetheless
    
    _, leaked = func_leak() # Python probably here free'd the tb here
    # but older versions did not
    assert leaked == 3
    
def test_track_memory():
    
    @measure_memory_usage
    def func_a():
        return 1
    
    ret, memory = func_a()
    ret_size = sys.getsizeof(ret)
    assert memory >= ret_size
    
