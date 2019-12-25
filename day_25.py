from computer import Computer

with open('input25', 'r') as data:
    data = list(map(int, data.read().split(',')))

brain = Computer(int_code=data)

for _, op, *_ in brain:
    if brain and brain.out[0] == ord('\n'):
        print(''.join(map(chr, reversed(brain.out))), end='')
        brain.out.clear()

    if op == '03' and not brain.feed:
        brain << map(ord, input('>>> ') + '\n')
