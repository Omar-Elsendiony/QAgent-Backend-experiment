from source_code import *

def test_0():
    pass
    input_0 = 100
    input_1 = [[60, 10], [50, 8], [20, 4], [20, 4], [8, 3], [3, 2]]
    assert knapsack(input_0, input_1) == 19

def test_1():
    pass
    input_0 = 40
    input_1 = [[30, 10], [50, 5], [10, 20], [40, 25]]
    assert knapsack(input_0, input_1) == 30

def test_2():
    pass
    input_0 = 750
    input_1 = [[70, 135], [73, 139], [77, 149], [80, 150], [82, 156], [87, 163], [90, 173], [94, 184], [98, 192], [106, 201], [110, 210], [113, 214], [115, 221], [118, 229], [120, 240]]
    assert knapsack(input_0, input_1) == 1458