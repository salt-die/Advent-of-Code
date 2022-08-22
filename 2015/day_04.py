from hashlib import md5
from itertools import count

import aoc_helper

KEY = aoc_helper.day(4)

def suffix(prefix):
    for i in count():
        if (
            md5(f"{KEY}{i}".encode())
            .hexdigest()
            .startswith(prefix)
        ):
            return i

def part_one():
    return suffix("0" * 5)

def part_two():
    return suffix("0" * 6)

aoc_helper.submit(4, part_one)
aoc_helper.submit(4, part_two)
