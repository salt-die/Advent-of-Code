with open('input', 'r') as numbers:
    numbers = list(map(int, numbers.readlines()))

print(sum(number//3 - 2 for number in numbers))

total = 0
for number in numbers:
    fuel = number // 3 - 2
    while fuel > 0:
        total += fuel
        fuel = fuel // 3 - 2

print(total)

#Alternate solution -- one-line non-recursive for-loop
from math import log
print(sum(sum(j for j in [number]
                for i in range(int(log(number, 3))+1)
                for j in [j//3 -2] if j > 0)
          for number in numbers))