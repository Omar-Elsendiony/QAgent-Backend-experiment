def find_first_even(numbers):
    if not numbers:  # Check if the list is empty
        return 0  
    for num in numbers:
        if isinstance(num, int):  # Check if the element is an integer
            if num % 2 == 0:
                break
    return 0