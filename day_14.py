from sympy import Symbol
from math import ceil
from collections import defaultdict

with open("input14") as data:
    data = data.readlines()

def parse(token,out=False):
    index = token.find(" ")
    coeff, symbol = int(token[:index]), Symbol(token[index + 1:])
    if out:
        return coeff, symbol
    return coeff * symbol

equations = {}
for equation in data:
    in_, out = equation.strip().split(" => ")
    coef, symbol = parse(out, out=True)
    equations[symbol] = coef, sum(parse(token) for token in in_.split(", "))

FUEL, ORE = Symbol('FUEL'), Symbol('ORE')

def acquire(this_much):
    required = defaultdict(int)
    required[FUEL] = this_much

    while True:
        for symbol, amount in required.items():
            if amount > 0 and symbol != ORE:
                break
        else:
            break
        coef, equation = equations[symbol]
        ceiling_divide = ceil(required[symbol] / coef)
        required[symbol] -= coef * ceiling_divide
        for symbol in equation.free_symbols:
            required[symbol] += equation.coeff(symbol) * ceiling_divide
    return required[ORE]

print(acquire(1)) # Part 1

fuel, cargo = 1, 1e12
while True:
    ore_required = acquire(fuel + 1)
    if ore_required > cargo:
        break
    else:
        # n == acquire(m) → p <= acquire(m * p / n)
        fuel = max(fuel + 1, (fuel + 1) * cargo // ore_required)

print(fuel) # Part 2
