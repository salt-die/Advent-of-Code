import aoc_lube
from aoc_lube.utils import extract_ints, sliding_window

DATA = [
    list(extract_ints(line)) for line in aoc_lube.fetch(year=2024, day=2).splitlines()
]


def is_safe(report):
    a, b = report[:2]
    Δ = (-1) ** (a < b)
    return all(0 < Δ * (a - b) < 4 for a, b in sliding_window(report, 2))


def damp_safe(report):
    return any(is_safe(report[:i] + report[i + 1 :]) for i in range(len(report)))


def part_one():
    return sum(is_safe(report) for report in DATA)


def part_two():
    return sum(damp_safe(report) for report in DATA)


aoc_lube.submit(year=2024, day=2, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=2, part=2, solution=part_two)
