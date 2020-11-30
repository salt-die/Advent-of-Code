from sympy import Symbol, ceiling
from collections import defaultdict

with open("input14") as data:
    data = data.readlines()

def separate(term, out=False):
    coef, symbol = term.split()
    coef, symbol = int(coef), Symbol(symbol)
    if out:
        return coef, symbol
    return coef * symbol

equations = {}
for equation in data:
    in_, out = equation.strip().split(" => ")
    coef, symbol = separate(out, out=True)
    equations[symbol] = coef, sum(separate(term) for term in in_.split(", "))

ORE = Symbol('ORE')

def acquire(this_much):
    required = defaultdict(int, {Symbol('FUEL'):this_much})

    while True:
        for symbol, amount in required.items():
            if amount > 0 and symbol != ORE:
                break
        else:
            break

        coef, equation = equations[symbol]
        required[symbol] -= coef * (base_mats := ceiling(amount / coef))
        for symbol in equation.free_symbols:
            required[symbol] += equation.coeff(symbol) * base_mats

    return required[ORE]

print(acquire(1)) # Part 1

fuel, cargo = 1, 1e12
while True:
    ore = acquire(fuel + 1)
    if ore > cargo:
        break
    else:
        fuel = (fuel + 1) * cargo // ore

print(fuel) # Part 2
