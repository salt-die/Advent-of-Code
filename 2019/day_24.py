import numpy as np
from scipy.signal import convolve

KERNEL = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

with open('input24', 'r') as data:
    data = [[char == '#' for char in line] for line in data.read().splitlines()]

bugs = np.array(data)
states = {bugs.tostring()}
while True:
    neighbor_count = convolve(bugs, KERNEL, mode='same')
    bugs = (bugs & (neighbor_count == 1)) | (~bugs & np.isin(neighbor_count, [1, 2]))
    if (as_string := bugs.tostring()) in states:
        break
    states.add(as_string)

print((bugs.flatten() * np.logspace(0, 24, 25, base=2, dtype=int)).sum()) # Part 1: 18842609

levels = np.pad(np.array(data)[None], [(100,), (0,), (0,)])
KERNEL3D = np.pad(KERNEL[None], [(1,), (0,), (0,)])
UP, dn = slice(1, None), slice(None, -1)

for _ in range(200):
    (neighbor_count := convolve(levels, KERNEL3D, mode='same'))[:, 2, 2] = 0
    for outer, inner in ((( 0,), (1, 2)), ((...,  0), (2, 1)),
                         ((-1,), (3, 2)), ((..., -1), (2, 3))):
        neighbor_count[(UP, *outer)] += levels[(dn, *inner, None)]
        neighbor_count[(dn, *inner)] += levels[(UP, *outer)].sum(axis=1)

    levels = (levels & (neighbor_count == 1)) | (~levels & np.isin(neighbor_count, [1, 2]))

print(levels.sum()) # Part 2: 2059
