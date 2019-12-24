from itertools import product
from computer import Computer

with open('input02', 'r') as data:
    data = list(map(int, data.read().split(',')))

#Part1
tape = Computer(int_code=data)
tape.int_code[1:3] = 12, 2
tape.compute()
print(tape.read(0))

#Part2
for i, j in product(range(100), repeat=2):
    tape.int_code[1:3]= i, j
    tape.compute()
    if tape.read(0) == 19690720: #Date of moon landing
        print(100 * i + j)
        break
