from Computer import Computer

with open('input05', 'r') as data:
    data = list(map(int, data.read().split(',')))

tape = Computer(int_code=data, verbose=True)
tape.compute() #'1': 4887191
tape.compute() #'5': 3419022