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