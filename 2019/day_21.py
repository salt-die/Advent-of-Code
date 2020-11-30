from computer import Computer

with open('input21', 'r') as data:
    data = list(map(int, data.read().split(',')))

brain = Computer(int_code=data)

instructions = '''NOT A J
NOT B T
AND D T
OR T J
NOT C T
AND D T
OR T J
WALK
'''
# NOT A OR (NOT B AND D) OR (NOT C AND D)
brain << map(ord, instructions)

for _ in brain:
    if brain and brain.out[0] == ord('\n'):
        print(''.join(map(chr, reversed(brain.out))), end='')
        brain.out.clear()

print(brain.last()) # Part 1

instructions = '''NOT C T
AND D T
OR H J
OR E J
AND T J
OR B T
OR E T
NOT T T
AND D T
OR T J
NOT A T
OR T J
RUN
'''
# (NOT C AND D AND (H OR E)) OR (NOT (B OR E) AND D) OR NOT A
brain << map(ord, instructions)

for _ in brain:
    if brain and brain.out[0] == ord('\n'):
        print(''.join(map(chr, reversed(brain.out))), end='')
        brain.out.clear()

print(brain.last()) # Part 2

