from itertools import groupby

def has_adjacent(number):
    number = str(number)
    for one, two in zip(number, number[1:]):
        if one == two:
            return True
    return False

def has_adjacent_pair(number):
    return [len(tuple(n)) for _, n in groupby(str(number))].count(2) >= 1

def is_non_decreasing(number):
    number = str(number)
    for one, two in zip(number, number[1:]):
        if int(one) > int(two):
            return False
    return True

start, end = 134564, 585159

# Part 1
passwords = [number for number in range(start, end + 1)
             if has_adjacent(number) and is_non_decreasing(number)]
print(len(passwords))

# Part 2
passwords = [number for number in passwords
             if has_adjacent_pair(number) and is_non_decreasing(number)]
print(len(passwords))