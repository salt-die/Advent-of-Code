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
        out = tape.out
    outs.append(out)

print(max(outs)) # Part 1


outs = []
for permutation in permutations('56789'):
    computers = [Computer(int_code=data) for _ in range(5)]
    amps = [c.compute_iter(feed=int(digit)) for c, digit in zip(computers, permutation)]
    feed = [0]

    for amp, computer in cycle(zip(amps, computers)):
        for _, op, __, after in amp:
            if op == '03' and not (computer.feed or after): #accepting input
                if feed: #feed input
                    computer.feed.append(feed.pop())
            elif op == '04':
                next(amp)
                feed.append(computer.out)
                break
        else:
            outs.append(feed.pop())
            break

print(max(outs)) # Part 2
