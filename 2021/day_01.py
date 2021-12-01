import aoc_helper

RAW  = aoc_helper.day(1)
DATA = list(aoc_helper.utils.extract_ints(RAW))

def compare(n):
    return sum(x < y for x, y in zip(DATA, DATA[n:]))

def part_one():
    return compare(1)

def part_two():
    return compare(3)

aoc_helper.submit(1, part_one)
aoc_helper.submit(1, part_two)
