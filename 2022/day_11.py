from collections import deque
from heapq import nlargest
from math import lcm

import aoc_lube
from aoc_lube.utils import extract_ints

from q import q  # https://github.com/salt-die/q


class Monkey(q):
    items, op, test, a, b
    nitems = 0

    def throw(self, item):
        buddy = self.b if item % self.test else self.a
        MONKEYS[buddy].items.append(item)


def parse_raw():
    for data in aoc_lube.fetch(year=2022, day=11).split("\n\n"):
        _, items, op, test = data.split("\n", maxsplit=3)
        yield Monkey(
            deque(extract_ints(items)),
            eval(f"lambda old: {op.removeprefix('  Operation: new =')}"),
            *extract_ints(test),
        )

MONKEYS = list(parse_raw())
LCM = lcm(*(monkey.test for monkey in MONKEYS))

def do_rounds(n, stressed):
    for _ in range(n):
        for monkey in MONKEYS:
            items = monkey.items
            monkey.nitems += len(items)
            while items:
                item = monkey.op(items.popleft())
                monkey.throw(item % LCM if stressed else item // 3)

    a, b = nlargest(2, MONKEYS, key=lambda monkey: monkey.nitems)
    return a.nitems  * b.nitems

def part_one():
    return do_rounds(20, False)

def part_two():
    return do_rounds(10_000, True)

aoc_lube.submit(year=2022, day=11, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=11, part=2, solution=part_two)
