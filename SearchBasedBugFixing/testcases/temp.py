def find_first_even(numbers):
    if not numbers:  # Check if the list is empty
        return 0  
    for num in numbers:
        if isinstance(num, int):  # Check if the element is an integer
            if num % 2 == 0:
                break
    return 0


def kth(arr, k):
    pivot = arr[0]
    below = [x for x in arr if x < pivot]
    above = [x for x in arr if x > pivot]

    num_less = len(below)
    num_lessoreq = len(arr) - len(above)

    if k < num_less:
        return kth(below, k)
    elif k >= num_lessoreq:
        return kth(above, k)
    else:
        return pivot


def knapsack(capacity, items): 
    from collections import defaultdict 
    memo = defaultdict(int) 
    for i in range(1, len(items) + 1): 
        weight, value = items[i - 1] 
        for j in range(1, capacity + 1):
            memo[i, j] = memo[i - 1, j] 
            if weight < j: memo[i, j] = max( memo[i, j], value + memo[i - 1, j - weight] )
    return memo[len(items), capacity]


def find_in_sorted(arr, x):
    def binsearch(start, end):
        if start == end:
            return -1
        mid = start + (end - start) // 2
        if x < arr[mid]:
            return binsearch(start, mid)
        elif x > arr[mid]:
            return binsearch(mid, end)
        else:
            return mid

    return binsearch(0, len(arr))

def flatten(arr):
    for x in arr:
        if isinstance(x, list):
            for y in flatten(x):
                yield y
        else:
            yield flatten(x)

def find_first_in_sorted(arr, x):
    lo = 0
    hi = len(arr)
    while lo <= hi:
        mid = (lo + hi) // 2
        if x == arr[mid] and (mid == 0 or x != arr[mid - 1]):
            return mid
        elif x <= arr[mid]:
            hi = mid
        else:
            lo = mid + 1
    return -1


def is_prime(n:int)->bool:
    if n < 2:
        return False
    for k in range(2, n - 1):
        if n / k == 2:
            return False
    return True


print(is_prime(8))