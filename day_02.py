from itertools import product

with open('input', 'r') as data:
    data = list(map(int, data.read().split(',')))

class TuringTape:
    def __init__(self):
        self.op_code_to_function = {1:lambda x, y: x + y,
                                    2:lambda x, y: x * y,
                                    99:None}

    def compute_data(self, noun, verb):
        head_position = 0
        memory = data.copy()
        memory[1:3] = [noun, verb]

        while True:
            try:
                op_code = memory[head_position]
            except IndexError:
                return -1

            if op_code not in self.op_code_to_function:
                return -1

            operator = self.op_code_to_function[op_code]

            if operator is None: #Halt
                return memory[0]

            argcount = operator.__code__.co_argcount

            try:
                *args, output_address = memory[head_position + 1:head_position + argcount + 2]
            except IndexError:
                return -1

            memory[output_address] = operator(*(memory[arg] for arg in args))
            head_position += argcount + 2

#Part1
tape = TuringTape()
print(tape.compute_data(12, 2))

#Part2
for i, j in product(range(100), repeat=2):
    if tape.compute_data(i, j) == 19690720: #Date of moon landing
        print(100 * i + j)
        break
