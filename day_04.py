from itertools import groupby
from glen import glen # generator length

def non_decreasing(start, end):
    number = list(str(start))

    # Generate first non-decreasing number
    for i, (digit1, digit2) in enumerate(zip(number, number[1:])):
        if digit1 > digit2:
            number = number[:i - 6]
            number.extend(digit1 for _ in range(6 - i))
            break

    end = list(str(end))
    while number < end:
        yield number
        for i, digit in enumerate(reversed(number), start=1):
            if digit != '9':
                number = number[:6 - i]
                number.extend(str(int(digit) + 1) for _ in range(i))
                break
        else:
            break

def has_adjacent(number):
    return any(glen(n) > 1 for _, n in groupby(number))

def has_pair(number):
    return any(glen(n) == 2 for _, n in groupby(number))

start, end = 134564, 585159

# Part 1
passwords = tuple(filter(has_adjacent, non_decreasing(start, end)))
print(len(passwords))

# Part 2
passwords = filter(has_pair, passwords)
print(glen(passwords))