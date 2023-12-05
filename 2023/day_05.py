import aoc_lube
from aoc_lube.utils import chunk, extract_ints
from mind_the_gaps import Endpoint, Gaps, x


def parse_raw():
    seeds, *groups = aoc_lube.fetch(year=2023, day=5).split("\n\n")
    yield list(extract_ints(seeds))
    for group in groups:
        yield [
            (Gaps([src <= x, x < src + length]), dst - src)
            for dst, src, length in chunk(extract_ints(group), 3)
        ]


seeds, *groups = parse_raw()


def offset_gaps(gaps, offset):
    return Gaps([Endpoint(e.value + offset, e.boundary) for e in gaps.endpoints])


def min_location(seeds):
    for group in groups:
        tmp_gaps = Gaps()
        for mapping, offset in group:
            if intersect := seeds & mapping:
                seeds -= mapping
                tmp_gaps |= offset_gaps(intersect, offset)
        seeds = tmp_gaps | seeds
    return seeds.endpoints[0].value


def part_one():
    seed_gaps = Gaps()
    for seed in seeds:
        seed_gaps |= Gaps([seed, seed])
    return min_location(seed_gaps)


def part_two():
    seed_gaps = Gaps()
    for a, b in chunk(seeds, 2):
        seed_gaps |= Gaps([a <= x, x < a + b])
    return min_location(seed_gaps)


aoc_lube.submit(year=2023, day=5, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=5, part=2, solution=part_two)
