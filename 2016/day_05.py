import aoc_lube
from hashlib import md5
from itertools import count, islice

DOOR_ID = aoc_lube.fetch(year=2016, day=5)

def interesting():
    for i in count():
        hash_ = md5(f"{DOOR_ID}{i}".encode()).hexdigest()
        if hash_.startswith("00000"):
            yield hash_

def part_one():
    return "".join(hash_[5] for hash_ in islice(interesting(), 8))

def part_two():
    password = {}
    for hash_ in interesting():
        pos = int(hash_[5], 16)
        if 8 <= pos or pos in password:
            continue

        password[pos] = hash_[6]
        if len(password) == 8:
            return "".join(char for _, char in sorted(password.items()))

aoc_lube.submit(year=2016, day=5, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=5, part=2, solution=part_two)
