def find_first_even(numbers):
    if not numbers:  # Check if the list is empty
        return 0  
    for num in numbers:
        if isinstance(num, int):  # Check if the element is an integer
            if num % 2 == 0:
                break
    return 0


def is_prime(n:int)->bool:
    if n < 2:
        return False
    for k in range(2, n - 1):
        if n / k == 2:
            return False
    return True


print(is_prime(8))