import numpy as np

Io = [19, -10, 7]
Europa = [1, 2, -3]
Ganymede = [14, -4, 1]
Callisto = [8, 7, -6]

planets = [Io, Europa, Ganymede, Callisto]
combs = np.array([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])

state = np.zeros((4, 6), dtype=int)
state[:, :3] = np.array(planets)
intermediate = np.zeros((6, 2, 3), dtype=int) # For doing numpy operations in place.
for _ in range(1000):
    np.subtract(np.fliplr(state[combs, :3]), state[combs, :3], out=intermediate)
    np.sign(intermediate, out=intermediate)
    np.add.at(state[:, 3:], combs, intermediate)
    state[:, :3] += state[:, 3:]

print((np.abs(state[:, :3]).sum(axis=1) * np.abs(state[:, 3:]).sum(axis=1)).sum())

state = np.zeros((4, 6), dtype=int)
state[:, :3] = np.array(planets)

flags = [True] * 3
cycle_lengths = []
initial_state = state.copy()
cycle = 0 # System is reversible, initial state will be the first repeated
while any(flags):
    np.subtract(np.fliplr(state[combs, :3]), state[combs, :3], out=intermediate)
    np.sign(intermediate, out=intermediate)
    np.add.at(state[:, 3:], combs, intermediate)
    state[:, :3] += state[:, 3:]
    cycle += 1

    for axis, flag in enumerate(flags):
        if flag and np.array_equal(state[:, axis::3], initial_state[:, axis::3]):
            cycle_lengths.append(cycle)
            flags[axis] = False

print(np.lcm.reduce(cycle_lengths)) # Part 2
