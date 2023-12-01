import re
from unicodedata import name

import aoc_lube

LINES = aoc_lube.fetch(year=2023, day=1).splitlines()


def part_one():
    total = 0
    for line in LINES:
        a, *_, b = re.findall(r"\d", 2 * line)
        total += int(a + b)
    return total


def part_two():
    digits = {
        k: v for v in "123456789" for k in [v, name(v).removeprefix("UNIT ").lower()]
    }
    total = 0
    for line in LINES:
        a, *_, b = re.findall(rf"(?=({"|".join(digits)}))", 2 * line)
        total += int(digits[a] + digits[b])
    return total


aoc_lube.submit(year=2023, day=1, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=1, part=2, solution=part_two)
