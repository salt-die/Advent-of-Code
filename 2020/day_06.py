import aoc_helper

raw = aoc_helper.day(6)
data = [list(map(set, group.splitlines())) for group in raw.split('\n\n')]

def combine_with(func):
    return sum(len(func(*group)) for group in data)

def part_one():
    return combine_with(set.union)

def part_two():
    return combine_with(set.intersection)

print(part_one(), part_two())
aoc_helper.submit(6, part_one)
aoc_helper.submit(6, part_two)
