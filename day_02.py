from itertools import product
from Computer import Computer

with open('input02', 'r') as data:
    data = list(map(int, data.read().split(',')))

#Part1
tape = Computer(int_code=data)
print(tape.compute(noun=12, verb=2))

#Part2
for i, j in product(range(100), repeat=2):
    if tape.compute(noun=i, verb=j) == 19690720: #Date of moon landing
        print(100 * i + j)
        break
