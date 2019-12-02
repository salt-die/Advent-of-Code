with open('input', 'r') as data:
    data = list(map(int, data.read().split(',')))

from itertools import product
pristine_data = data.copy()

for i,j in product(range(100), repeat=2):
    data = pristine_data.copy()
    data[1:3] = [i, j]

    c = 0
    try:
        while 1:
            op = data[c]
            if op == 99:
                break
            pos1, pos2, out = data[c + 1:c + 4]
            val1, val2 = data[pos1], data[pos2]
            data[out] = val1 + val2 if op == 1 else val1 * val2
            c += 4

    except IndexError:
        continue

    if data[0] == 19690720:
        print(100*i + j)
        break
