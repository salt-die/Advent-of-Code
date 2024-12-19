from functools import cache

import aoc_lube


def parse_raw():
    towels, designs = aoc_lube.fetch(year=2024, day=19).split("\n\n")
    return towels.split(", "), designs.splitlines()


TOWELS, DESIGNS = parse_raw()


@cache
def ndesigns(design):
    return not design or sum(
        ndesigns(design.removesuffix(towel))
        for towel in TOWELS
        if design.endswith(towel)
    )


def part_one():
    return sum(ndesigns(design) > 0 for design in DESIGNS)


def part_two():
    return sum(ndesigns(design) for design in DESIGNS)


aoc_lube.submit(year=2024, day=19, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=19, part=2, solution=part_two)
