from source_code import *

def test_0():
    pass
    input_0 = 750
    input_1 = [[70, 135], [73, 139], [77, 149], [80, 150], [82, 156], [87, 163], [90, 173], [94, 184], [98, 192], [106, 201], [110, 210], [113, 214], [115, 221], [118, 229], [120, 240]]
    assert knapsack(input_0, input_1) == 1458

def test_1():
    pass
    input_0 = 26
    input_1 = [[12, 24], [7, 13], [11, 23], [8, 15], [9, 16]]
    assert knapsack(input_0, input_1) == 51