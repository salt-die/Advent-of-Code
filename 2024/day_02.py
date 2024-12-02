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


# Alternatively, for a O(n) solution for part 2:
#
#
# def sign(n):
#     return 1 if n > 0 else -1 if n < 0 else 0
#
#
# def sign_of_seq(report):
#     a, b, c, d = report[:4]
#     return sign(sign(b - a) + sign(c - b) + sign(d - c))
#
#
# def damp_safe(report):
#     sgn = sign_of_seq(report)
#     if sgn == 0:
#         return False
#     for i, (a, b) in enumerate(sliding_window(report, 2)):
#         if sign(b - a) != sgn:
#             return (
#                 is_safe(
#                     report[:i] + report[i + 1 :]
#                 )  # Should be able to determine which of
#                 or is_safe(
#                     report[: i + 1] + report[i + 2 :]
#                 )  # these to use by the magnitude of b - a
#             )
#     if 0 < sgn * (b - a) < 4:
#         return is_safe(report[1:])
#     return is_safe(report[:-1])
#
#
# def part_two():
#     return sum(damp_safe(report) for report in DATA)
