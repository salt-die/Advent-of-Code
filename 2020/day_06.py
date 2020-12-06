import aoc_helper
from functools import reduce

raw = aoc_helper.day(6)
data = raw.split('\n\n')

def part_one():
    return sum(len(set(filter(str.isalpha, group))) for group in data)

def part_two():
    return sum(len(reduce(set.intersection, map(set, group.splitlines()))) for group in data)

aoc_helper.submit(6, part_one)
aoc_helper.submit(6, part_two)
