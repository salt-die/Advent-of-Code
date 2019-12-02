from itertools import product
from Computer import Computer

with open('input', 'r') as data:
    data = list(map(int, data.read().split(',')))

#Part1
tape = Computer(data)
print(tape.compute(12, 2))

#Part2
for i, j in product(range(100), repeat=2):
    if tape.compute(i, j) == 19690720: #Date of moon landing
        print(100 * i + j)
        break
