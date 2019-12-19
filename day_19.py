from computer import Computer
from itertools import product

with open('input19', 'r') as data:
    data = list(map(int, data.read().split(',')))

tape = Computer(int_code=data)
area = 0

for coordinate in product(range(50), repeat=2):
    tape.compute(feed=coordinate)
    area += tape.pop()

print(area) # Part 1: 114

# By inspection the slope of the outer lines is roughly 11/7 and 10/7 (original solution was
# plotted on a numpy array), so x-coordinate should be roughly in the 700 range to fit a
# 100x100 box in the tractor beam, begin search there:

def is_beam(x, y):
    tape.compute(feed=(x, y))
    return tape.pop()

def find_edge(x, y):
    while is_beam(x, y):
        x += 1
    return x - 1

x = 681
y = 1000
while True:
    x = find_edge(x, y)
    if is_beam(x - 99, y + 99):
        x -= 99
        break
    else:
        y += 1

print(x * 10000 + y) # Part 2: 10671712
