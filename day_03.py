import numpy as np

with open('input', 'r') as data:
    data = data.readlines()

directions = dict(zip('UDRL', map(np.array,([0, 1], [0, -1], [1, 0], [-1, 0]))))

wires = [[(directions[d], int(''.join(num))) for d, *num in wire.split(',')] for wire in data]

visits = []
for wire in wires:
    visited = []
    current_location = np.array([0, 0])
    visited.append(tuple(current_location))
    for direction, number in wire:
        visited.extend(tuple(current_location + i * direction) for i in range(1, number + 1))
        current_location += number * direction
    visits.append(visited)

intersections = set(visits[0]) & set(visits[1])
intersections.remove((0, 0))

#Part 1
closest = min(intersections, key=lambda arr:sum(np.abs(arr)))
print(sum(np.abs(closest)))

#Part 2
closest = min(intersections, key=lambda arr:sum(wire.index(arr) for wire in visits))
print(sum(wire.index(closest) for wire in visits))
