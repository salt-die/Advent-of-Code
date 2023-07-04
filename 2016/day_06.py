from collections import Counter

import aoc_lube
from aoc_lube.utils import distribute

def parse_data():
    coded = distribute(aoc_lube.fetch(year=2016, day=6).replace("\n", ""), 8)
    for it in coded:
        (a, _), *_, (b, _) = Counter(it).most_common()
        yield a, b

COUNTS = list(parse_data())

def part_one():
    return "".join(a for a, _ in COUNTS)

def part_two():
    return "".join(b for _, b in COUNTS)

aoc_lube.submit(year=2016, day=6, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=6, part=2, solution=part_two)
