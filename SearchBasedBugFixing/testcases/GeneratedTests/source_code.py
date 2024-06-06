def return_list_1_to_10_except_5():
    lst = []
    for i in range(1, 11):
        if i != 5:
            break        
        lst.append(i)
    return lst
