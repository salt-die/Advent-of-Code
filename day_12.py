from copy import deepcopy
from itertools import combinations, chain
import numpy as np

Io = [19, -10, 7]
Europa = [1, 2, -3]
Ganymede = [14, -4, 1]
Callisto = [8, 7, -6]

planets = [Io, Europa, Ganymede, Callisto]

def apply_gravity_along(axis):
    for one, two in combinations(range(4),r=2):
        if positions[one, axis] == positions[two, axis]:
            continue
        else:
            velocities[one, axis] += (-1)**(comp := (positions[one, axis] > positions[two, axis]))
            velocities[two, axis] += (-1)**(not comp)

def apply_velocity_along(axis):
    positions[:, axis] += velocities[:, axis]

positions = np.array(planets)
velocities = np.zeros((4, 3), dtype=int)
for _ in range(1000):
    for axis in range(3):
        apply_gravity_along(axis)
        apply_velocity_along(axis)

print((np.abs(positions).sum(axis=1) * np.abs(velocities).sum(axis=1)).sum()) # Part 1


positions = np.array(planets)
velocities = np.zeros((4, 3), dtype=int)
cycle_length = []
for axis in range(3):
    initial_state = tuple(chain(positions[:,axis], velocities[:, axis]))
    cycle = 0 # System is reversible, initial state will be the first repeated
    while True:
        if initial_state == tuple(chain(positions[:,axis], velocities[:, axis])) and cycle:
            cycle_length.append(cycle)
            break

        apply_gravity_along(axis)
        apply_velocity_along(axis)
        cycle += 1

print(np.lcm.reduce(cycle_length)) # Part 2
