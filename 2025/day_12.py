import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints


def parse_raw():
    *packages, regions = aoc_lube.fetch(year=2025, day=12).split("\n\n")
    areas = np.array([package.count("#") for package in packages])
    as_ints = map(extract_ints, regions.splitlines())
    fits = [(h * w, np.array(data)) for h, w, *data in as_ints]
    return areas, fits


AREA, FITS = parse_raw()


def part_one():
    return sum(area >= AREA @ region for area, region in FITS)


aoc_lube.submit(year=2025, day=12, part=1, solution=part_one)
