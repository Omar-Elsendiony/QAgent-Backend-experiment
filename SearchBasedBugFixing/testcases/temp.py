# def find_first_even(numbers):
#     if not numbers:  # Check if the list is empty
#         return 0  
#     for num in numbers:
#         if isinstance(num, int):  # Check if the element is an integer
#             if num % 2 == 0:
#                 break
#     return 0


# def kth(arr, k):
#     pivot = arr[0]
#     below = [x for x in arr if x < pivot]
#     above = [x for x in arr if x > pivot]

#     num_less = len(below)
#     num_lessoreq = len(arr) - len(above)

#     if k < num_less:
#         return kth(below, k)
#     elif k >= num_lessoreq:
#         return kth(above, k)
#     else:
#         return pivot


# def knapsack(capacity, items): 
#     from collections import defaultdict 
#     memo = defaultdict(int) 
#     for i in range(1, len(items) + 1): 
#         weight, value = items[i - 1] 
#         for j in range(1, capacity + 1):
#             memo[i, j] = memo[i - 1, j] 
#             if weight < j: memo[i, j] = max( memo[i, j], value + memo[i - 1, j - weight] )
#     return memo[len(items), capacity]


# def find_in_sorted(arr, x):
#     def binsearch(start, end):
#         if start == end:
#             return -1
#         mid = start + (end - start) // 2
#         if x < arr[mid]:
#             return binsearch(start, mid)
#         elif x > arr[mid]:
#             return binsearch(mid, end)
#         else:
#             return mid

#     return binsearch(0, len(arr))

# def flatten(arr):
#     for x in arr:
#         if isinstance(x, list):
#             for y in flatten(x):
#                 yield y
#         else:
#             yield flatten(x)

# def find_first_in_sorted(arr, x):
#     lo = 0
#     hi = len(arr)
#     while lo <= hi:
#         mid = (lo + hi) // 2
#         if x == arr[mid] and (mid == 0 or x != arr[mid - 1]):
#             return mid
#         elif x <= arr[mid]:
#             hi = mid
#         else:
#             lo = mid + 1
#     return -1


# def is_prime(n:int)->bool:
#     if n < 2:
#         return False
#     for k in range(2, n - 1):
#         if n / k == 2:
#             return False
#     return True


# # print(is_prime(8))


# def rpn_eval(tokens):
#     def op(symbol, a, b):
#         return {
#             '+': lambda a, b: a + b,
#             '-': lambda a, b: a - b,
#             '*': lambda a, b: a * b,
#             '/': lambda a, b: a / b
#         }[symbol](a, b)
#     stack = []
#     for token in tokens:
#         if isinstance(token, float):
#             stack.append(token)
#         else:
#             a = stack.pop()
#             b = stack.pop()
#             stack.append(
#                 op(token, b, a)
#             )
#     return stack.pop()

# x = rpn_eval([5.0, 1.0, 2.0, '+', 4.0, '*', '+', 3.0, '-'])
# print(x)

# x = '-14.0'
# x.strip()
# print(x)


# def sieve(max):
#     primes = []
#     for n in range(2, max + 1):
#         if any(n % p > 0 for p in primes):
#             primes.append(n)
#     return primes


# import string
# def to_base(num, b):
#     result = ''
#     alphabet = string.digits + string.ascii_uppercase
#     while num > 0:
#         i = num % b
#         num = num // b
#         result = result + alphabet[i]
#     return result

# def subsequences(a, b, k):
#     if k == 0:
#         return [[]]
#     ret = []
#     for i in range(a, b + 1 - k):
#         ret.extend(
#             [i] + rest for rest in subsequences(i + 1, b, k - 1)
#         )
#     return ret


# def pascal(n):
#     rows = [[1]]
#     for r in range(1, n):
#         row = []
#         for c in range(0, r):
#             upleft = rows[r - 1][c - 1] if c > 0 else 0
#             upright = rows[r - 1][c] if c < r else 0
#             row.append(upleft + upright)
#         rows.append(row)

#     return rows


# def quicksort(arr):
#     if not arr:
#         return []

#     pivot = arr[0]
#     lesser = quicksort([x for x in arr[1:] if x < pivot])
#     greater = quicksort([x for x in arr[1:] if x > pivot])
#     return lesser + [pivot] + greater




# import torch
# import faiss
# data = torch.load('BugEmbeddings_All.pt', map_location=torch.device('cpu'))
# dimension = data.shape[1]  
# index = faiss.IndexFlatIP(dimension)
# index.add(data.numpy())


def levenshtein(source, target):
    if source == '' or target == '':
        return len(source) or len(target)

    elif source[0] == target[0]:
        return levenshtein(source[1:], target[1:])

    else:
        return 1 + min(
            levenshtein(source,     target[1:]),
            levenshtein(source[1:], target[1:]),
            levenshtein(source[1:], target)
        )


r = levenshtein('hello', 'olleh')
print(r)