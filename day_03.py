import numpy as np

with open('input', 'r') as data:
    data = data.readlines()

wires = [[(d, int(''.join(num))) for d, *num in wire.split(',')] for wire in data]

directions={'U': np.array([0, 1]),
            'D': np.array([0, -1]),
            'R': np.array([1, 0]),
            'L': np.array([-1, 0])}

visits = []
for wire in wires:
    visited = []
    current_location = np.array([0,0])
    visited.append(tuple(current_location))
    for direction, number in wire:
        for _ in range(number):
            current_location += directions[direction]
            visited.append(tuple(current_location))
    visits.append(visited)

intersections = set(visits[0]) & set(visits[1])
intersections.remove((0, 0))

#Part 1
x, y = min(intersections, key=lambda x:abs(x[0]) + abs(x[1]))
print(abs(x) + abs(y))

#Part 2
closest = min(intersections, key=lambda x:visits[0].index(x) + visits[1].index(x))
print(visits[0].index(closest) + visits[1].index(closest))