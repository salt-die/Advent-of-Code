from Computer import Computer
from itertools import permutations, cycle

with open('input07', 'r') as data:
    data = list(map(int, data.read().split(',')))

outs = []
for permutation in permutations('01234'):
    out = 0
    for i in range(5):
        tape = Computer(int_code=data)
        tape.compute(feed=(int(permutation[i]), out))
        out = tape.out.pop()
    outs.append(out)

print(max(outs)) # Part 1


outs = []
for permutation in permutations('56789'):
    #setup network
    computers = [Computer(int_code=data) for _ in range(5)]
    amps = [c.compute_iter(feed=int(digit)) for c, digit in zip(computers, permutation)]
    for computer1, computer2 in zip(computers, computers[1:]):
        computer2.connect(computer1.out)
    computers[0].connect(computers[-1].out)
    computers[0].feed.appendleft(0)

    for amp, computer in cycle(zip(amps, computers)):
        for _ in amp:
            if computer.out:
                break
        else:
            outs.append(computers[-1].out.pop())
            break

print(max(outs)) # Part 2
