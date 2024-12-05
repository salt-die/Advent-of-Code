from functools import cmp_to_key

import aoc_lube
from aoc_lube.utils import chunk, extract_ints, sliding_window


def parse_raw():
    rules_in, pages_in = aoc_lube.fetch(year=2024, day=5).split("\n\n")
    rules = set(chunk(extract_ints(rules_in), 2))
    pages = [list(extract_ints(line)) for line in pages_in.splitlines()]
    return rules, pages


RULES, PAGES = parse_raw()


@cmp_to_key
def cmp(a, b):
    return -1 if (a, b) in RULES else 1


def is_sorted(page):
    return all(a < b for a, b in sliding_window(map(cmp, page)))


def part_one():
    return sum(page[len(page) // 2] for page in PAGES if is_sorted(page))


def part_two():
    return sum(
        sorted(page, key=cmp)[len(page) // 2] for page in PAGES if not is_sorted(page)
    )


aoc_lube.submit(year=2024, day=5, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=5, part=2, solution=part_two)
