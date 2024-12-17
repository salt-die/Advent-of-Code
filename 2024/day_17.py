import aoc_lube
from aoc_lube.utils import extract_ints

A, _, _, *CODE = extract_ints(aoc_lube.fetch(year=2024, day=17))


def run_program(a):
    out = []
    while a:
        b = a % 8 ^ 3
        out.append(b ^ 5 ^ (a >> b) % 8)
        a //= 8
    return out


def part_one():
    return ",".join(map(str, run_program(A)))


def part_two():
    possible = [0]
    for i in range(len(CODE)):
        possible = [
            n * 8 + a
            for n in possible
            for a in range(8)
            if CODE[-i - 1 :] == run_program(n * 8 + a)
        ]
    return possible[0]


aoc_lube.submit(year=2024, day=17, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=17, part=2, solution=part_two)
