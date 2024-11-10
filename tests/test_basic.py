from pydecorators.basic import timeit
from time import sleep


def test_timeit():
    
    @timeit
    def sleep_function(sleep_time):
        sleep(sleep_time)
        return 2
    
    sleep_time = 0.4
    function_result, function_time = sleep_function(sleep_time)
    assert function_result == 2
    assert abs(function_time - sleep_time) <= 1e-2
    

def test_timeit_accuracy():
    
    @timeit(1)
    def sleep_function(sleep_time):
        sleep(sleep_time)
        return 2
    
    sleep_time = 0.41
    function_result, function_time = sleep_function(sleep_time)
    assert function_result == 2
    assert function_time == 0.4
