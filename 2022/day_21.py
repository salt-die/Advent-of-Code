import re
from operator import add, mul, sub, truediv

import aoc_lube
from sympy import Equality, Symbol, solve

OPS = {"+": add, "*": mul, "-": sub, "/": truediv, "==": Equality}
EQUATIONS = {
    name: int(value) if value.isdigit() else value.split()
    for name, value in re.findall(r"(.*): (.*)", aoc_lube.fetch(year=2022, day=21))
}

def evaluate(name):
    value = EQUATIONS[name]
    if not isinstance(value, list):
        return value

    lhs, op, rhs = value
    return OPS[op](evaluate(lhs), evaluate(rhs))

def part_one():
    return round(evaluate("root"))

def part_two():
    EQUATIONS["humn"] = Symbol("humn")
    EQUATIONS["root"][1] = "=="
    return round(solve(evaluate("root"))[0])

aoc_lube.submit(year=2022, day=21, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=21, part=2, solution=part_two)
