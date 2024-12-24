from collections import deque
from operator import and_, or_, xor

import aoc_lube
from aoc_lube.utils import chunk


def parse_raw():
    init_in, adder_in = aoc_lube.fetch(year=2024, day=24).split("\n\n")
    init = dict(
        (a, int(b)) for a, b in chunk(init_in.replace("\n", ": ").split(": "), 2)
    )
    adder = deque(
        (a, op, b, result) if a < b else (b, op, a, result)
        for a, op, b, _, result in chunk(adder_in.replace("\n", " ").split(), 5)
    )
    return init, adder


INITIAL, ADDER = parse_raw()
OPS = {"AND": and_, "OR": or_, "XOR": xor}


def part_one():
    while ADDER:
        a, op, b, result = ADDER.popleft()
        if a in INITIAL and b in INITIAL:
            INITIAL[result] = OPS[op](INITIAL[a], INITIAL[b])
        else:
            ADDER.append((a, op, b, result))
    return int("".join(str(INITIAL[f"z{45 - i:02}"]) for i in range(46)), 2)


def is_or_operand(out):
    return any(op == "OR" and out in (a, b) for a, op, b, _ in ADDER)


def part_two():
    swapped = []
    for a, op, _, out in ADDER:
        if op == "XOR" and a[0] != "x" and out[0] != "z":
            swapped.append(out)
        elif op == "XOR" and is_or_operand(out):
            swapped.append(out)
        elif op != "XOR" and out[0] == "z" and out != "z45":
            swapped.append(out)
        elif op == "AND" and a != "x00" and not is_or_operand(out):
            swapped.append(out)
    return ",".join(sorted(swapped))


aoc_lube.submit(year=2024, day=24, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=24, part=2, solution=part_two)
