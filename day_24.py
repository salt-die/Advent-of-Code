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

levels = np.pad(np.array(data)[None], [(100,), (0,), (0,)])
KERNEL3D = np.pad(KERNEL[None], [(1,),(0,),(0,)])
UP, dn = slice(1, None, None), slice(None, -1, None)

for _ in range(200):
    neighbor_count = nd.convolve(levels, KERNEL3D, mode='constant')
    neighbor_count[:, 2, 2] = 0
    for outer, inner in ((( 0,), (1, 2)), ((...,  0), (2, 1)),
                         ((-1,), (3, 2)), ((..., -1), (2, 3))):
        neighbor_count[(UP, *outer)] += levels[(dn, *inner, None)]
        neighbor_count[(dn, *inner)] += levels[(UP, *outer)].sum(axis=1)

    levels = ((levels & (neighbor_count == 1)) |
              (~levels & np.isin(neighbor_count, [1, 2]))).astype(int)

print(levels.sum()) # Part 2: 2059
