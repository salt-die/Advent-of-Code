import numpy as np

with open('input', 'r') as data:
    data = data.readlines()

wires = [[(d, int(''.join(num))) for d, *num in wire.split(',')] for wire in data]

directions = dict(zip('UDRL', map(np.array,([0, 1], [0, -1], [1, 0], [-1, 0]))))

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
closest = min(intersections, key=lambda arr:sum(np.abs(arr)))
print(sum(np.abs(closest)))

#Part 2
closest = min(intersections, key=lambda arr:sum(wire.index(arr) for wire in visits))
print(sum(wire.index(closest) for wire in visits))
