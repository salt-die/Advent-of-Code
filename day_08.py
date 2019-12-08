import numpy as np

with open('input08', 'r') as data:
    data = np.array(list(data.read().strip())).reshape((-1, 6, 25))

fewest_zeros = min(data, key=lambda layer:np.sum(layer=='0'))
print(np.sum(fewest_zeros=='1') * np.sum(fewest_zeros=='2')) #Part 1

decoded = data[0]
for layer in data:
    decoded = np.where(decoded != '2', decoded, layer)

decoded = np.where(decoded == '1','M',' ') # To make it easier to see
for row in decoded:
    print(*row) # Part 2

#   M M M M   M       M M M M     M         M     M
#         M   M       M M     M   M         M     M
#       M       M   M   M M M     M         M M M M
#     M           M     M     M   M         M     M
#   M             M     M     M   M         M     M
#   M M M M       M     M M M     M M M M   M     M