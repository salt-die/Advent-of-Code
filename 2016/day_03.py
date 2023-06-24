import aoc_lube
import numpy as np

DATA = np.fromstring(aoc_lube.fetch(year=2016, day=3), dtype=int, sep=" ").reshape(-1, 3)

def nvalid(data):
    triangles = np.sort(data)
    return ((triangles[:, :2].sum(axis=1) - triangles[:, 2]) > 0).sum()

def part_one():
    return nvalid(DATA)

def part_two():
    return nvalid(DATA.T.reshape(-1, 3))

aoc_lube.submit(year=2016, day=3, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=3, part=2, solution=part_two)
