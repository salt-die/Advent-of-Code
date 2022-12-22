import re
from operator import add, mul, sub, truediv

import aoc_lube
from sympy import Equality, Symbol, solve

NAMES = re.findall(r"(.*): (.*)", aoc_lube.fetch(year=2022, day=21))
OPS = {"+": add, "*": mul, "-": sub, "/": truediv}

class evaldict(dict):
    def __getitem__(self, item):
        value = super().__getitem__(item)
        if not isinstance(value, tuple):
            return value

        op, lhs, rhs = value
        value = op(self[lhs], self[rhs])
        self[item] = value
        return value

def part_one():
    equations = evaldict()

    for name, value in NAMES:
        if value.isdigit():
            equations[name] = int(value)
        else:
            lhs, op, rhs = value.split()
            equations[name] = OPS[op], lhs, rhs

    return round(equations["root"])

def part_two():
    equations = evaldict()

    for name, value in NAMES:
        if value.isdigit():
            equations[name] = Symbol("humn") if name == "humn" else int(value)
        else:
            lhs, op, rhs = value.split()
            equations[name] = Equality if name == "root" else OPS[op], lhs, rhs

    return round(solve(equations["root"])[0])

aoc_lube.submit(year=2022, day=21, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=21, part=2, solution=part_two)
