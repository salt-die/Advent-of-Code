import aoc_lube
from aoc_lube.utils import extract_ints


class Block:
    def __init__(self, val):
        self.val = val

    def __rshift__(self, other):
        self.r = other
        other.l = self
        return other


def parse_raw():
    it = extract_ints(aoc_lube.fetch(year=2022, day=20))
    root = current = Block(next(it))
    for l, val in enumerate(it, start=1):
        current.o = Block(val)
        current = current >> current.o

    current.o = root
    return current >> root, l

ROOT, LEN = parse_raw()

def mix():
    current = ROOT
    while True:
        current.l >> current.r

        r = current.val % LEN
        l = LEN - r

        if l < r:
            for _ in range(l):
                current.l = current.l.l
            current.r = current.l.r
        else:
            for _ in range(r):
                current.r = current.r.r
            current.l = current.r.l

        current.l >> current >> current.r
        current = current.o

        if current is ROOT:
            break

def extract_coords():
    current = ROOT

    while True:
        if current.val == 0:
            break
        current = current.r

    for _ in range(3):
        for _ in range(1000):
            current = current.r
        yield current.val

def part_one():
    mix()
    return sum(extract_coords())

def part_two():
    current = ROOT
    while True:
        current.val *= 811589153
        current = current.r
        if current is ROOT:
            break

    for _ in range(10):
        mix()
    return sum(extract_coords())

aoc_lube.submit(year=2022, day=20, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=20, part=2, solution=part_two)
