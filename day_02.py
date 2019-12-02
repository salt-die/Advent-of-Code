from itertools import product

with open('input', 'r') as data:
    data = list(map(int, data.read().split(',')))

class TuringTape:
    def __init__(self):
        self.op_from_op_code = {1:lambda x, y: x + y,
                                2:lambda x, y: x * y,
                                99:None}

    def compute_iter(self, noun, verb):
        head_position = 0
        memory = data.copy()
        memory[1:3] = noun, verb

        while True:
            try:
                op_code = memory[head_position]
            except IndexError:
                yield -1, -1
                break

            if op_code not in self.op_from_op_code:
                yield -1, -1
                break

            operator = self.op_from_op_code[op_code]

            if operator is None: #Halt
                yield memory[0], 0
                break

            argcount = operator.__code__.co_argcount

            try:
                *args, output_address = memory[head_position + 1:head_position + argcount + 2]
            except IndexError:
                yield -1, -1
                break

            memory[output_address] = operator(*(memory[arg] for arg in args))
            yield memory[output_address], output_address

            head_position += argcount + 2

    def compute(self, noun, verb):
        for result, _ in self.compute_iter(noun, verb):
            pass
        return result


#Part1
tape = TuringTape()
print(tape.compute(12, 2))

#Part2
for i, j in product(range(100), repeat=2):
    if tape.compute(i, j) == 19690720: #Date of moon landing
        print(100 * i + j)
        break
