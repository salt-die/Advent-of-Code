from collections import Counter
from heapq import nsmallest
import re

import aoc_lube
from aoc_lube.utils import shift_cipher

def parse_raw():
    checksum_re = re.compile(r'(\d+)\[([a-z]{5})\]')
    for room in aoc_lube.fetch(year=2016, day=4).split():
        *names, idchecksum = room.split("-")
        sector_id, checksum = checksum_re.match(idchecksum).groups()
        yield "".join(names), int(sector_id), checksum

ROOMS = list(parse_raw())

def part_one():
    total = 0
    for name, sector_id, checksum in ROOMS:
        most_common = nsmallest(
            n=5,
            iterable=Counter(name).items(),
            key=lambda tup: (-tup[1], tup[0]),
        )
        if "".join(letter for letter, _ in most_common) == checksum:
            total += int(sector_id)
    return total

def part_two():
    for name, sector_id, _ in ROOMS:
        if "northpole" in shift_cipher(name, sector_id):
            return sector_id

aoc_lube.submit(year=2016, day=4, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=4, part=2, solution=part_two)
