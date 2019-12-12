from copy import deepcopy
from itertools import combinations
from functools import reduce
import numpy as np

Io = [19, -10, 7]
Europa = [1, 2, -3]
Ganymede = [14, -4, 1]
Callisto = [8, 7, -6]

planets = [Io, Europa, Ganymede, Callisto]

def apply_gravity_along(axis):
    for one, two in combinations(range(4),r=2):
        if positions[one][axis] == positions[two][axis]:
            continue
        else:
            velocities[one][axis] += (-1)**(positions[one][axis] > positions[two][axis])
            velocities[two][axis] += (-1)**(positions[one][axis] < positions[two][axis])

def apply_velocity_along(axis):
    for planet in range(4):
        positions[planet][axis] += velocities[planet][axis]

def energy():
    return sum(sum(map(abs, position)) * sum(map(abs, velocity))
               for position, velocity in zip(positions,velocities))


positions = deepcopy(planets)
velocities = [[0] * 3 for _ in range(4)]

for _ in range(1000):
    for axis in range(3):
        apply_gravity_along(axis)
        apply_velocity_along(axis)

print(energy()) # Part 1


positions = deepcopy(planets)
velocities = [[0] * 3 for _ in range(4)]
intervals = []

for axis in range(3):
    previous_states = set()
    cycle = 0
    while True:
        state = tuple((position[axis], velocity[axis])
                      for position, velocity in zip(positions, velocities))
        if state in previous_states:
            intervals.append(cycle)
            break
        else:
            previous_states.add(state)

        apply_gravity_along(axis)
        apply_velocity_along(axis)
        cycle += 1

print(reduce(np.lcm, intervals)) # Part 2
