import re

import aoc_lube

LINES = aoc_lube.fetch(year=2023, day=1).splitlines()


def part_one():
    total = 0
    for line in LINES:
        a, *_, b = re.findall(r"\d", 2 * line)
        total += int(a + b)
    return total


def part_two():
    digits = "zero|one|two|three|four|five|six|seven|eight|nine"
    to_digit = {digit: str(i) for i, digit in enumerate(digits.split("|"))}
    total = 0
    for line in LINES:
        a, *_, b = re.findall(rf"(?=({digits}|\d))", 2 * line)
        total += int(to_digit.get(a, a) + to_digit.get(b, b))
    return total


aoc_lube.submit(year=2023, day=1, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=1, part=2, solution=part_two)
