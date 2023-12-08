from hashlib import md5
from itertools import count, islice

import aoc_lube

DOOR_ID = aoc_lube.fetch(year=2016, day=5)

def interesting():
    for i in count():
        hash_ = md5(f"{DOOR_ID}{i}".encode()).hexdigest()
        if hash_.startswith("00000"):
            yield hash_[5:7]

def part_one():
    return "".join(a for a, _ in islice(interesting(), 8))

def part_two():
    password = {}
    for a, b in interesting():
        pos = int(a, 16)
        if pos >= 8 or pos in password:
            continue

        password[pos] = b
        if len(password) == 8:
            return "".join(char for _, char in sorted(password.items()))

aoc_lube.submit(year=2016, day=5, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=5, part=2, solution=part_two)
