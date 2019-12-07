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
        out = tape.out.pop()
    outs.append(out)

print(max(outs)) # Part 1

#setup network
computers = [Computer(int_code=data) for _ in range(5)]
for i in range(5):
    computers[i].connect(computers[i - 1])

outs = []
for permutation in permutations('56789'):
    programs = [computer.compute_iter(feed=int(digit))
                for computer, digit in zip(computers, permutation)]
    computers[0].feed.appendleft(0)

    for program, computer in cycle(zip(programs, computers)):
        for _ in program:
            if computer.out:
                break
        else:
            outs.append(computers[-1].out.pop())
            break

print(max(outs)) # Part 2
