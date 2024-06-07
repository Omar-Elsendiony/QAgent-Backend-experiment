from source_code import *

def test_0():
    pass
    input_0 = [3, 4, 5, 5, 5, 5, 6]
    input_1 = 5
    assert find_in_sorted(input_0, input_1) == 3

def test_1():
    pass
    input_0 = [1, 2, 3, 4, 6, 7, 8]
    input_1 = 5
    assert find_in_sorted(input_0, input_1) == -1

def test_2():
    pass
    input_0 = [1, 2, 3, 4, 6, 7, 8]
    input_1 = 4
    assert find_in_sorted(input_0, input_1) == 3

def test_3():
    pass
    input_0 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    input_1 = 18
    assert find_in_sorted(input_0, input_1) == 8

def test_4():
    pass
    input_0 = [3, 5, 6, 7, 8, 9, 12, 13, 14, 24, 26, 27]
    input_1 = 0
    assert find_in_sorted(input_0, input_1) == -1

def test_5():
    pass
    input_0 = [3, 5, 6, 7, 8, 9, 12, 12, 14, 24, 26, 27]
    input_1 = 12
    assert find_in_sorted(input_0, input_1) == 6