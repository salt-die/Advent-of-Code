from Computer import Computer

with open('input05', 'r') as data:
    data = list(map(int, data.read().split(',')))

tape = Computer(int_code=data)
tape.compute() #Type '1'
tape.compute() #Type '5'