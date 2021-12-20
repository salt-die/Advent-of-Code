from itertools import product

import cv2
import numpy as np

import aoc_helper
from aoc_helper.utils import extract_ints


class Scanner:
    def __init__(self, coords):
        self.coords = coords
        self.distances = np.array(
            list(map(set, np.linalg.norm(coords[:, None] - coords[None], axis=-1)))
        )


def parse_raw():
    raw = aoc_helper.day(19).split("\n\n")
    scanners = [ ]

    for scanner in raw:
        _, data = scanner.split("\n", 1)
        scanners.append(
            Scanner(
                np.fromiter(extract_ints(data), dtype=int).reshape(-1, 3)
            )
        )

    return scanners

SCANNERS = parse_raw()

def coalesce(a, b):
    js, ks = [ ], [ ]

    for (j, p), (k, q) in product(
        enumerate(a.distances),
        enumerate(b.distances),
    ):
        if len(p & q) >= 12:
            js.append(j)
            ks.append(k)

            if len(js) == 4:
                break
    else:
        return False

    M = cv2.estimateAffine3D(b.coords[ks], a.coords[js])[1].round().astype(int)
    orientation, translation = M[:, :3], M[:, 3]

    transformed = b.coords @ orientation.T + translation

    check = (a.coords[:, None] == transformed[None]).all(-1)
    where_a_equal_b, where_b_equal_a = np.where(check)
    b_not_equal_a_mask = ~check.any(0)

    a.distances[where_a_equal_b] |= b.distances[where_b_equal_a]
    a.distances = np.concatenate((a.distances, b.distances[b_not_equal_a_mask]))
    a.coords = np.concatenate((a.coords, transformed[b_not_equal_a_mask]))

    a.scanners.append(translation)

    return True

def coalesce_all():
    origin = SCANNERS[0]
    origin.scanners = [np.zeros(3, dtype=int)]

    unpaired = SCANNERS[1:]
    while unpaired:
        unpaired = [
            scanner
            for scanner in unpaired
            if not coalesce(origin, scanner)
        ]
    return origin

ORIGIN = coalesce_all()

def part_one():
    return len(ORIGIN.coords)

def part_two():
    scanners = np.array(ORIGIN.scanners)
    return np.abs(scanners[:, None] - scanners[None]).sum(axis=-1).max()

aoc_helper.submit(19, part_one)
aoc_helper.submit(19, part_two)
