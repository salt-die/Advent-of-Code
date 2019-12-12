import numpy as np

planets = [[19, -10, 7], [1, 2, -3], [14, -4, 1], [8, 7, -6]]
combs = np.array([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])
intermediate = np.zeros((6, 2, 3), dtype=np.int16) # For doing numpy operations in place.
initial = np.hstack((planets, np.zeros((4,3), dtype=np.int16)))

def update_state():
    np.subtract(np.fliplr(state[combs, :3]), state[combs, :3], out=intermediate)
    np.sign(intermediate, out=intermediate)
    np.add.at(state[:, 3:], combs, intermediate)
    state[:, :3] += state[:, 3:]
#== Part 1
state = initial.copy()
for _ in range(1000):
    update_state()

print((np.abs(state[:, :3]).sum(axis=1) * np.abs(state[:, 3:]).sum(axis=1)).sum())
#== Part 2
flags, cycle_lengths, state, cycle = [True] * 3, [], initial.copy(), 0
while any(flags):
    update_state()
    cycle += 1

    for i, flag in enumerate(flags):
        if flag and np.array_equal(state[:, i::3], initial[:, i::3]):
            cycle_lengths.append(cycle)
            flags[i] = False

print(np.lcm.reduce(cycle_lengths))
