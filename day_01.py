import numpy as np

with open('input01', 'r') as numbers:
    numbers = np.array(list(map(int, numbers.readlines())))

print(np.sum(numbers//3 - 2)) # Part 1

total = 0
fuel = numbers
while np.any(fuel):
    fuel = fuel // 3 - 2
    np.clip(fuel, 0, None, out=fuel)
    total += fuel

print(np.sum(total)) # Part 2

#Alternate solution -- one-line non-recursive for-loop
from math import log
print(sum(sum(j for j in [number]
                for _ in range(int(log(number, 3)) + 1)
                for j in [j // 3 - 2] if j > 0)
          for number in numbers))