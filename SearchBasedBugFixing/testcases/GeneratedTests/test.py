from source_code import *

def test_0():
    pass
    input_0 = [1, 2, 6, 72, 7, 33, 4]
    assert quicksort(input_0) == [1, 2, 4, 6, 7, 33, 72]

def test_1():
    pass
    input_0 = [5, 4, 3, 2, 1]
    assert quicksort(input_0) == [1, 2, 3, 4, 5]

def test_2():
    pass
    input_0 = [10, 16, 6, 1, 14, 19, 15, 2, 9, 4, 18]
    assert quicksort(input_0) == [1, 2, 4, 6, 9, 10, 14, 15, 16, 18, 19]

def test_3():
    pass
    input_0 = [10, 16, 6, 1, 14, 19, 15, 2, 9, 4, 18, 17, 12, 3, 11, 8, 13, 5, 7]
    assert quicksort(input_0) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]