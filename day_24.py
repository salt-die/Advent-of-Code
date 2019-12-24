from collections import defaultdict
import numpy as np
import scipy.ndimage as nd

KERNEL = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

with open('input24', 'r') as data:
    data = [[int(char == '#') for char in line] for line in data.read().splitlines()]

bugs = np.array(data)
states = set((bugs.tostring(), ))
while True:
    neighbor_count = nd.convolve(bugs, KERNEL, mode="constant")
    bugs = ((bugs & (neighbor_count == 1)) |
            (~bugs & np.isin(neighbor_count, [1, 2]))).astype(int)
    if (as_string := bugs.tostring()) in states:
        break
    states.add(as_string)

print((bugs.flatten() * np.logspace(0, 24, 25, base=2, dtype=int)).sum()) # Part 1: 18842609

levels = defaultdict(lambda:np.zeros_like(bugs), {0: np.array(data)})
levels[-1]; levels[1] # First outer and inner level
for _ in range(200):
    new = {}
    for level, bugs in tuple(levels.items()):
        neighbor_count = nd.convolve(bugs, KERNEL, mode="constant")
        for outer, inner in ((0, (1, 2)), ((..., 0), (2, 1)),
                             (4, (3, 2)), ((..., 4), (2, 3))):
            neighbor_count[outer] += levels[level - 1][inner]
            neighbor_count[inner] += levels[level + 1][outer].sum()

        new[level] = ((bugs & (neighbor_count == 1)) |
                      (~bugs & np.isin(neighbor_count, [1, 2]))).astype(int)
        new[level][2, 2] = 0 # Center stays empty
    levels.update(new)

print(sum(array.sum() for array in levels.values())) # Part 2: 2059
