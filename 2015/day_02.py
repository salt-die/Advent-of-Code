import aoc_helper
from aoc_helper.utils import extract_ints, chunk

RAW = aoc_helper.day(2)
DATA = tuple(map(sorted, chunk(extract_ints(RAW), n=3)))

def part_one():
    return sum(
        3 * l * w + 2 * w * h + 2 * l * h
        for l, w, h in DATA
    )

def part_two():
    return sum(
        2 * (l + w) + l * w * h
        for l, w, h in DATA
    )

aoc_helper.submit(2, part_one)
aoc_helper.submit(2, part_two)

print(part_one(), part_two())
