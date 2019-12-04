from itertools import groupby, tee
from glen import glen

def has_adjacent(number):
    return any(glen(n) > 1 for _, n in groupby(str(number)))

def has_adjacent_pair(number):
    return any(glen(n) == 2 for _, n in groupby(str(number)))

def is_non_decreasing(number):
    number = str(number)
    return all(first <= second for first, second in zip(number, number[1:]))

start, end = 134564, 585159

# Part 1
nondecreasing = filter(is_non_decreasing, range(start, end + 1))
passwords, copy = tee(filter(has_adjacent, nondecreasing))
print(glen(copy))

# Part 2
passwords = filter(has_adjacent_pair, passwords)
print(glen(passwords))