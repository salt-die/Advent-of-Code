import aoc_lube
from aoc_lube.utils import shiftmod

def part_one():
    number = sum(
        sum(("=-012".find(c) - 2) * 5**i for i, c in enumerate(reversed(line)))
        for line in aoc_lube.fetch(year=2022, day=25).splitlines()
    )

    digits = ""
    while number:
        number, digit = number // 5, shiftmod(number, 5, -2)
        number += digit < 0
        digits += "012=-"[digit]

    return digits[::-1]

aoc_lube.submit(year=2022, day=25, part=1, solution=part_one)
