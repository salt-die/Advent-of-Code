from functools import cache
from operator import and_, or_, lshift, rshift

import aoc_helper

WIRES = { }
for line in aoc_helper.day(7).splitlines():
    *expr, _, wire = line.split()
    WIRES[wire] = expr

OPS = dict(AND=and_, OR=or_, LSHIFT=lshift, RSHIFT=rshift)

@cache
def eval_wire(wire: str):
    if wire.isnumeric():
        return int(wire)

    match WIRES[wire]:
        case [a]:
            return eval_wire(a)
        case ["NOT", a]:
            return ~eval_wire(a)
        case [a, OP, b]:
            return OPS[OP](eval_wire(a), eval_wire(b))

def part_one():
    return eval_wire("a")

def part_two():
    WIRES["b"] = [str(part_one())]
    eval_wire.cache_clear()
    return eval_wire("a")

aoc_helper.submit(7, part_one)
aoc_helper.submit(7, part_two)
