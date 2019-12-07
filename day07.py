from Computer import Computer
from itertools import permutations, cycle

with open('input07', 'r') as data:
    data = list(map(int, data.read().split(',')))

outs = []
for permutation in permutations('01234'):
    out = 0
    for i in range(5):
        tape = Computer(int_code=data)
        tape.compute(std_in=(int(permutation[i]), out))
        out = int(tape.out)
    outs.append(out)

print(max(outs)) # Part 1


outs = []
for permutation in permutations('56789'):
    feed = 0
    computers = [Computer(int_code=data) for _ in range(5)]
    amps = [c.compute_iter(std_in=int(digit)) for c, digit in zip(computers, permutation)]

    for comp in amps: # Push inputs
        next(comp)

    for amp, computer in cycle(zip(amps, computers)):
        computer.feed = feed

        try:
            while True:
                _, op, __ = next(amp)
                if op == '04':
                    feed = int(computer.out)
                    break
        except:
            outs.append(feed)
            break

print(max(outs)) # Part 2
