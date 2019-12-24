from collections import defaultdict
import numpy as np
import scipy.ndimage as nd

KERNEL = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

with open('input24', 'r') as data:
    data = [[1 if char == '#' else 0 for char in line] for line in data.read().splitlines()]

def new_state(bugs):
    neighbor_count = nd.convolve(bugs, KERNEL, mode="constant")
    still_alive = np.where((bugs == 1) & (neighbor_count == 1), 1, 0)
    new_borns = np.where((bugs == 0) & ((neighbor_count == 2) | (neighbor_count == 1)), 1, 0)
    return still_alive + new_borns

bugs = np.array(data)
states = set((bugs.tostring(), ))
while True:
    bugs = new_state(bugs)
    if (as_string := universe.tostring()) in states:
        break
    states.add(as_string)

powers = np.nditer(universe, flags=['c_index'])
print(sum(2**powers.index for cooef in powers if cooef)) # Part 1: 18842609

levels = defaultdict(lambda:np.zeros_like(universe), {0: np.array(data)})
levels[-1]; levels[1] # First outer and inner level
def new_states():
    new = {}
    for level in list(levels):
        bugs = levels[level]
        neighbor_count = nd.convolve(bugs, KERNEL, mode="constant")
        for outer, inner in ((0, (1, 2)), ((..., 0), (2, 1)),
                             (4, (3, 2)), ((..., 4), (2, 3))):
            neighbor_count[outer] += levels[level - 1][inner]
            neighbor_count[inner] += levels[level + 1][outer].sum()

        still_alive = np.where((bugs == 1) & (neighbor_count == 1), 1, 0)
        new_borns = np.where((bugs == 0) & ((neighbor_count == 2) | (neighbor_count == 1)), 1, 0)
        new[level] = still_alive + new_borns
        new[level][2, 2] = 0 # Center stays empty
    levels.update(new)

for _ in range(200):
    new_states()

print(sum(array.sum() for array in levels.values())) # Part 2: 2059
