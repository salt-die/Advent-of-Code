import re

import aoc_lube

RAW = aoc_lube.fetch(year=2024, day=3)
MUL_RE = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
COMMAND_RE = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")


def part_one():
    total = 0
    for match in MUL_RE.finditer(RAW):
        a, b = match.groups()
        total += int(a) * int(b)
    return total


def part_two():
    enabled = True
    total = 0
    for match in COMMAND_RE.finditer(RAW):
        if match[0] == "do()":
            enabled = True
        elif match[0] == "don't()":
            enabled = False
        elif enabled:
            a, b = match.groups()
            total += int(a) * int(b)
    return total


aoc_lube.submit(year=2024, day=3, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=3, part=2, solution=part_two)
