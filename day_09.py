from computer import Computer

with open('input09', 'r') as data:
    data = list(map(int, data.read().split(',')))

tape = Computer(int_code=data)
for value in (1, 2): #Part 1 and Part 2
    tape.compute(feed=value)
    print(tape.pop())