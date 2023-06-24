from collections import Counter
from itertools import chain
import re

import aoc_lube
from aoc_lube.utils import shift_cipher

RAW = aoc_lube.fetch(year=2016, day=4)
IDCHECKSUM_RE = re.compile(r'(\d+)\[([a-z]{5})\]')

def part_one():
    total = 0
    for room in RAW.split():
        *names, idchecksum = room.split("-")
        counts = Counter(chain.from_iterable(names)).items()
        most_common = sorted(counts, key=lambda tup: (-tup[1], tup[0]))[:5]
        [(sector_id, checksum)] = IDCHECKSUM_RE.findall(idchecksum)
        if "".join(letter for letter, _ in most_common) == checksum:
            total += int(sector_id)
    return total

def part_two():
    for room in RAW.split():
        *names, idchecksum = room.split("-")
        [(sector_id, _)] = IDCHECKSUM_RE.findall(idchecksum)
        if "northpole" in set(shift_cipher(name, int(sector_id)) for name in names):
            return sector_id

aoc_lube.submit(year=2016, day=4, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=4, part=2, solution=part_two)
