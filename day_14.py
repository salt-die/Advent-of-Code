from sympy import Symbol
from math import ceil
from collections import defaultdict

with open("input14") as data:
    data = data.readlines()

def parse(token,out=False):
    index = token.find(" ")
    symbols[x] = Symbol((x:= token[index + 1:]))
    if out:
        return symbols[x], int(token[:index])
    return int(token[:index]) * symbols[x]

symbols = {}
equations = {}
for equation in data:
    in_, out = equation.strip().split(" => ")
    symbol, coef = parse(out, out=True)
    equations[symbol] = sum([parse(token) for token in in_.split(", ")]), coef

def acquire(fuel):
    required = defaultdict(int)
    required[symbols['FUEL']] = fuel

    while True:
        for symbol, amount in required.items():
            if amount > 0 and symbol != symbols['ORE']:
                break
        else:
            break
        equation, coef = equations[symbol]
        ceiling_divide = ceil(required[symbol] / coef)
        required[symbol] -= coef * ceiling_divide
        for symbol in equation.free_symbols:
            required[symbol] += equation.coeff(symbol) * ceiling_divide
    return required[symbols['ORE']]

print(acquire(1)) # Part 1

fuel, cargo = 1, 1e12
while True:
    ore_required = acquire(fuel + 1)
    if ore_required > cargo:
        break
    else:
        # n == acquire(m) → 1e12 <= acquire(m * 1e12 / n)
        fuel = max(fuel + 1, (fuel + 1) * cargo // ore_required)

print(fuel) # Part 2
