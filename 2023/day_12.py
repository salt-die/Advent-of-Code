from functools import cache

import aoc_lube


def parse_raw():
    for line in aoc_lube.fetch(year=2023, day=12).splitlines():
        springs, s = line.split()
        yield springs, tuple(map(int, s.split(",")))


DATA = parse_raw()


def total_combinations(springs, groups):
    @cache
    def combinations(i, j, r):
        if j == len(groups):
            return springs.count("#", i) == 0
        if i == len(springs):
            return j == len(groups) - 1 and r == groups[j]

        n = 0
        if springs[i] != ".":
            n += combinations(i + 1, j, r + 1)
        if springs[i] != "#":
            if r == groups[j]:
                n += combinations(i + 1, j + 1, 0)
            elif r == 0:
                n += combinations(i + 1, j, 0)
        return n

    return combinations(0, 0, 0)


def part_one():
    return sum(total_combinations(springs, groups) for springs, groups in DATA)


def part_two():
    return sum(
        total_combinations("?".join([springs] * 5), groups * 5)
        for springs, groups in DATA
    )


aoc_lube.submit(year=2023, day=12, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=12, part=2, solution=part_two)
