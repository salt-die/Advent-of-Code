import aoc_helper
from aoc_helper.utils import sliding_window

A, H, K, N, Z = map(ord, "ahknz")

def incr(ords):
    for i in range(7, -1, -1):
        if ords[i] == Z:
            ords[i] = A
        else:
            ords[i] += 1 + (ords[i] in {H, K, N})
            break

def is_valid(ords):
    has_increasing = ndoubles = 0

    for a, b, c in sliding_window(ords, 3):
        has_increasing |= a + 2 == b + 1 == c
        ndoubles += a == b != c

    ndoubles += a != b == c

    return has_increasing and ndoubles >= 2

def get_next_valid(password):
    ords = list(map(ord, password))

    incr(ords)
    while not is_valid(ords):
        incr(ords)

    return "".join(map(chr, ords))

def part_one():
    return get_next_valid(aoc_helper.day(11))

def part_two():
    return get_next_valid(part_one())

aoc_helper.submit(11, part_one)
aoc_helper.submit(11, part_two)
