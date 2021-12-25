import aoc_helper
from aoc_helper.utils import extract_ints

X_ADDS = extract_ints("".join(aoc_helper.day(24).splitlines()[5::18]))
Y_ADDS = extract_ints("".join(aoc_helper.day(24).splitlines()[15::18]))

def find_deltas():
    """
    Find deltas between digits.
    """
    stack  = [ ]
    deltas = [ ]

    for i, (x, y) in enumerate(zip(X_ADDS, Y_ADDS)):
        if x >= 0:
            stack.append((i, y))
        else:
            j, y = stack.pop()
            deltas.append((j, i, x + y))

    return deltas

DELTAS = find_deltas()

def satisfy(target):
    digits = [target] * 14

    for i, j, delta in DELTAS:
        if 1 <= target - delta <= 9:
            digits[i], digits[j] = target - delta, target
        else:
            digits[i], digits[j] = target, target + delta

    return "".join(map(str, digits))

def part_one():
    return satisfy(9)

def part_two():
    return satisfy(1)

aoc_helper.submit(24, part_one)
aoc_helper.submit(24, part_two)
