import aoc_lube
from aoc_lube.utils import extract_ints

import numpy as np
from scipy.ndimage import convolve, label, generate_binary_structure as kernel

DATA = np.fromiter(extract_ints(aoc_lube.fetch(year=2022, day=18)), int).reshape(-1, 3)
DATA -= DATA.min(axis=0) - 1
DROPLET = np.zeros(DATA.max(axis=0) + 2, int)
DROPLET[*DATA.T] = 1

def surface_area():
    nneighbors = convolve(DROPLET, kernel(3, 1)) * DROPLET
    return 7 * DROPLET.sum() - nneighbors.sum()

aoc_lube.submit(year=2022, day=18, part=1, solution=surface_area)

DROPLET[np.isin(label(1 - DROPLET)[0], (0, 1), invert=True)] = 1
aoc_lube.submit(year=2022, day=18, part=2, solution=surface_area)
