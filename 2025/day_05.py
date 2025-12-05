import aoc_lube
from aoc_lube.utils import chunk, extract_ints
from mind_the_gaps import Gaps


def parse_raw():
    ranges, ingredients = aoc_lube.fetch(year=2025, day=5).split("\n\n")
    gap = Gaps()
    for start, end in chunk(extract_ints(ranges.replace("-", " ")), 2):
        gap |= Gaps([start, end])
    return gap, list(extract_ints(ingredients))


RANGES, INGREDIENTS = parse_raw()
print(RANGES, INGREDIENTS)


def part_one():
    return sum(ingredient in RANGES for ingredient in INGREDIENTS)


def part_two():
    ningredients = 0
    for a, b in chunk(RANGES.endpoints, 2):
        ningredients += b.value - a.value + 1
    return ningredients


aoc_lube.submit(year=2025, day=5, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=5, part=2, solution=part_two)
