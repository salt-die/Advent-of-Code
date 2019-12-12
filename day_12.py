"""
Warning: This solution is slow due to the number of arrays we create.  Std library solutions
recommended, but this was to practice numpy implementation.  We can also pass all combinations
of indices at once in apply_gravity_along, but I haven't figured out the masking needed yet.
"""
from copy import deepcopy
from itertools import combinations, chain
import numpy as np

Io = [19, -10, 7]
Europa = [1, 2, -3]
Ganymede = [14, -4, 1]
Callisto = [8, 7, -6]

planets = [Io, Europa, Ganymede, Callisto]

def apply_gravity_along(axis):
    for comb in combinations(range(4), r=2):
        if np.ptp(positions[comb, axis]):
            velocities[comb, axis] += (-1)**((arr := positions[comb, axis]) - arr[::-1] > 0)

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
        if (all(init_val == state_val
                for init_val, state_val in zip(initial_state, chain(positions[:, axis], velocities[:, axis])))
           and cycle):
            cycle_length.append(cycle)
            break

        apply_gravity_along(axis)
        apply_velocity_along(axis)
        cycle += 1

print(np.lcm.reduce(cycle_length)) # Part 2
