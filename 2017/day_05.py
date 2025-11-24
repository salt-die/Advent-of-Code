import aoc_lube
from aoc_lube.utils import extract_ints

DATA = list(extract_ints(aoc_lube.fetch(year=2017, day=5)))


def traverse(cond):
    offset = i = 0
    while 0 <= offset < len(DATA):
        new_offset = offset + DATA[offset]
        DATA[offset] += cond(DATA[offset])
        offset = new_offset
        i += 1
    return i


def part_one():
    return traverse(lambda jump: 1)


def part_two():
    return traverse(lambda jump: -1 if jump >= 3 else 1)


aoc_lube.submit(year=2017, day=5, part=1, solution=part_one)
aoc_lube.submit(year=2017, day=5, part=2, solution=part_two)
