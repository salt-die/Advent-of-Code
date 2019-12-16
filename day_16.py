from itertools import cycle, repeat
from functools import reduce

with open('input16', 'r') as data:
    data = data.read().strip()

def phase(number):
    new_number = []
    for i, digit in enumerate(number, start=1):
        coefficients = (coef for base in cycle((0,1,0,-1)) for coef in repeat(base, i))
        next(coefficients)
        new_number.append(abs(sum(digit * next(coefficients) for digit in number)) % 10)
    return new_number

number = list(map(int, data))
for _ in range(100):
    number = phase(number)

print(''.join(map(str, number[:8]))) # Part 1

number = (list(map(int, data)) * 10000)[int(data[:7]):] # Slice at offset

for i in range(100):
    sum_ = reduce(lambda x, y: (x + y) % 10, number) # We could use sum, but this is memory efficient.
    for j, digit in enumerate(number): # Would be more optimal to loop over reversed(number).
        number[j] = sum_
        sum_ = (sum_ - digit) % 10

print(''.join(map(str, number[:8]))) # Part 2
