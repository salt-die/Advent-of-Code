from itertools import cycle, repeat

with open('input16', 'r') as data:
    data = data.read().strip()

BASE = (0,1,0,-1)

def phase(number):
    new_number = []
    for i, digit in enumerate(number, start=1):
        multiplier = (repeated_factor for factor in cycle(BASE)
                                      for repeated_factor in repeat(factor, i))
        next(multiplier)
        new_number.append(abs(sum(digit * next(multiplier) for digit in number)) % 10)
    return new_number

number = list(map(int, data))
for _ in range(100):
    number = phase(number)

print(''.join(map(str, number[:8]))) # Part 1

offset = int(data[:7])
number = list(map(int, data)) * 10000

for i in range(100):
    partial_sum = sum(number[offset:])
    for j, digit in enumerate(number[offset:], start=offset):
        number[j] = abs(partial_sum) % 10
        partial_sum -= digit

print(''.join(map(str, number[offset: offset + 8]))) # Part 2