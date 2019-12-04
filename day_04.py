from itertools import groupby

def has_adjacent(number):
    return any(len(tuple(n)) > 1 for _, n in groupby(str(number)))

def has_adjacent_pair(number):
    return any(len(tuple(n)) == 2 for _, n in groupby(str(number)))

def is_non_decreasing(number):
    number = str(number)
    return all(int(first) <= int(second) for first, second in zip(number, number[1:]))

start, end = 134564, 585159

# Part 1
nondecreasing = filter(is_non_decreasing, range(start, end + 1))
passwords = tuple(filter(has_adjacent, nondecreasing))
print(len(passwords))

# Part 2
passwords = tuple(filter(has_adjacent_pair, passwords))
print(len(passwords))