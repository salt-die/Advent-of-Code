from itertools import product

with open('input', 'r') as data:
    data = list(map(int, data.read().split(',')))

def compute_data(memory):
    head_position = 0
    while True:
        try:
            op_code = memory[head_position]
        except IndexError:
            return -1

        if op_code not in (1, 2, 99):
            return -1

        if op_code == 99:
            return memory[0]

        try:
            address_1, address_2, output_address = data[head_position + 1:head_position + 4]
        except IndexError:
            return -1

        value_1, value_2 = memory[address_1], memory[address_2]
        memory[output_address] = value_1 + value_2 if op_code == 1 else value_1 * value_2
        head_position += 4

for i,j in product(range(100), repeat=2):
    new_data = data.copy()
    new_data[1], new_data[2] = i, j
    if compute_data(new_data) == 19690720:
        print(100 * i + j)
        break
