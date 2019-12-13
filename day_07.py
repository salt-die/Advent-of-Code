from computer import Computer
from itertools import permutations, cycle

with open('input07', 'r') as data:
    data = list(map(int, data.read().split(',')))

tape = Computer(int_code=data)
outs = []
for permutation in permutations(range(5)):
    out = 0
    for i in range(5):
        tape.compute(feed=(permutation[i], out))
        out = tape.pop()
    outs.append(out)

print(max(outs)) # Part 1

computers = [Computer(int_code=data) for _ in range(5)]
for i in range(5): # Setup network
    computers[i] << computers[i - 1]

outs = []
for permutation in permutations(range(5, 10)):
    computers[0] << 0
    programs = [amp.compute_iter(feed=digit) for amp, digit in zip(computers, permutation)]

    for program, computer in cycle(zip(programs, computers)):
        for _ in program:
            if computer: # Produced output
                break
        else:
            outs.append(computers[-1].pop())
            break

print(max(outs)) # Part 2
