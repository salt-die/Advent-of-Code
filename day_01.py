with open('day_01_input.txt', 'r') as numbers:
    numbers = [int(line) for line in numbers.readlines()]

print(sum([number//3 - 2 for number in numbers]))

grand_total = 0
for number in numbers:
    fuel = number // 3 - 2
    while fuel > 0:
        grand_total += fuel
        fuel = fuel // 3 - 2

print(grand_total)