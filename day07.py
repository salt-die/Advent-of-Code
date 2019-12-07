from Computer import Computer
from itertools import permutations, cycle

with open('input07', 'r') as data:
    data = list(map(int, data.read().split(',')))

tape = Computer(int_code=data)
outs = []
for permutation in permutations('01234'):
    out = 0
    for i in range(5):
        tape.compute(feed=(int(permutation[i]), out))
        out = tape.pop()
    outs.append(out)

print(max(outs)) # Part 1

#Setup network
computers = [Computer(int_code=data) for _ in range(5)]
for i in range(5):
    computers[i] << computers[i - 1] # Connect computers[i - 1].out to computers[i].feed

outs = []
for permutation in permutations('56789'):
    programs = [computer.compute_iter(feed=int(digit))
                for computer, digit in zip(computers, permutation)]
    computers[0] << 0 # Feed in 0

    for program, computer in cycle(zip(programs, computers)):
        for _ in program:
            if computer.out:
                break
        else:
            outs.append(computers[-1].pop())
            break

print(max(outs)) # Part 2
