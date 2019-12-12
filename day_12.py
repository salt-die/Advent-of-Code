import numpy as np

Io = [19, -10, 7]
Europa = [1, 2, -3]
Ganymede = [14, -4, 1]
Callisto = [8, 7, -6]

planets = [Io, Europa, Ganymede, Callisto]

combs = np.array([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])

positions = np.array(planets)
velocities = np.zeros((4, 3), dtype=int)
intermediate = np.zeros((6, 2, 3), dtype=int) # For doing numpy operations in place.
for _ in range(1000):
    np.subtract(np.fliplr(positions[combs]), positions[combs], out=intermediate)
    np.sign(intermediate, out=intermediate)
    np.add.at(velocities, combs, intermediate)
    positions += velocities

print((np.abs(positions).sum(axis=1) * np.abs(velocities).sum(axis=1)).sum())

positions = np.array(planets)
velocities = np.zeros((4, 3), dtype=int)
intermediate = np.zeros((6, 2), dtype=int)
cycle_length = []
for axis in range(3):
    initial_pos = positions[:, axis].copy()
    initial_vel = velocities[:, axis].copy()
    cycle = 0 # System is reversible, initial state will be the first repeated
    while True:
        np.subtract(np.fliplr(positions[combs, axis]), positions[combs, axis], out=intermediate)
        np.sign(intermediate, out=intermediate)
        np.add.at(velocities[:, axis], combs, intermediate)
        positions[:, axis] += velocities[:, axis]
        cycle += 1

        if (np.array_equal(velocities[:, axis], initial_vel) and
            np.array_equal(positions[:, axis], initial_pos)):
            cycle_length.append(cycle)
            break

print(np.lcm.reduce(cycle_length)) # Part 2
