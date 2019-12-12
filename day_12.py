import numpy as np

planets = [[19, -10, 7], [1, 2, -3], [14, -4, 1], [8, 7, -6]]
combs = np.array([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])
intermediate = np.zeros((6, 2, 3), dtype=np.int16) # For doing numpy operations in place.

def update_state():
    np.subtract(np.fliplr(state[combs, :3]), state[combs, :3], out=intermediate)
    np.sign(intermediate, out=intermediate)
    np.add.at(state[:, 3:], combs, intermediate)
    state[:, :3] += state[:, 3:]

state = np.hstack((planets, np.zeros((4,3), dtype=np.int16)))
for _ in range(1000):
    update_state()
print((np.abs(state[:, :3]).sum(axis=1) * np.abs(state[:, 3:]).sum(axis=1)).sum()) # Part 1

state = np.hstack((planets, np.zeros((4,3), dtype=np.int16)))
flags, cycle_lengths, initial, cycle = np.array([True] * 3), [], state.copy(), 0
is_equal = np.vectorize(lambda i: np.array_equal(state[:, i::3], initial[:, i::3]))
while flags.any():
    update_state()
    cycle += 1

    if is_equal(np.nonzero(flags)).any():
        cycle_lengths.append(cycle)
        flags[flags] = ~is_equal(*np.nonzero(flags))

print(np.lcm.reduce(cycle_lengths)) # Part 2
