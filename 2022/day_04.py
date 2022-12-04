import parse

import aoc_lube

RANGES = tuple(parse.findall("{:d}-{:d},{:d}-{:d}", aoc_lube.fetch(year=2022, day=4)))

def part_one():
    return sum(a <= c and d <= b or c <= a and b <= d for a, b, c, d, in RANGES)

def part_two():
    return sum(a <= d and c <= b for a, b, c, d in RANGES)

aoc_lube.submit(year=2022, day=4, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=4, part=2, solution=part_two)
