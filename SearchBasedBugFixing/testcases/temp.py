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


def lcs_length(s, t):
    from collections import Counter
    dp = Counter()
    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i, j] = dp[i - 1, j] + 1
    return max(dp.values()) if dp else 0


def is_prime(n:int)->bool:
    if n < 2:
        return False
    for k in range(2, n - 1):
        if n / k == 2:
            return False
    return True


print(is_prime(8))