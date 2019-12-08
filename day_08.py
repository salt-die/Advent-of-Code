import numpy as np

with open('input08', 'r') as data:
    data = np.array(list(data.read().strip())).reshape((-1, 6, 25))

fewest_zeros = min(data, key=lambda layer:''.join(map(''.join,layer)).count('0'))
digits = ''.join(map(''.join, fewest_zeros))
print(digits.count('1') * digits.count('2')) # Part 1

decoded= data[0]
for layer in data:
    decoded = np.where(decoded!='2', decoded, layer)
decoded = np.where(decoded=='1','M',' ') # To make it easier to see

for i in decoded:
    print(*i) # Part 2

#   M M M M   M       M M M M     M         M     M
#         M   M       M M     M   M         M     M
#       M       M   M   M M M     M         M M M M
#     M           M     M     M   M         M     M
#   M             M     M     M   M         M     M
#   M M M M       M     M M M     M M M M   M     M