def find_first_even(numbers):
    if not numbers:  # Check if the list is empty
        return 0  
    for num in numbers:
        if isinstance(num, int):  # Check if the element is an integer
            if num % 2 == 0:
                break
    return 0

c = find_first_even([2,4, 9])  # Expected output: 0
print(c)

import keyword
if 'str' in keyword.kwlist:
    print('ok')

print(keyword.kwlist)