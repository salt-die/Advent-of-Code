from heapq import heappop, heappush

import aoc_lube
from aoc_lube.utils import int_grid

GRID = int_grid(aoc_lube.fetch(year=2023, day=17))
H, W = GRID.shape


def min_heatloss(mn, mx):
    heap = [(0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]
    heatlosses = {}
    while heap:
        heatloss, y, x, Δy, Δx = heappop(heap)
        if y == H - 1 and x == W - 1:
            return heatloss

        for Δy, Δx in ((-Δx, Δy), (Δx, -Δy)):
            Δheatloss = 0
            for d in range(1, mx + 1):
                v = y + Δy * d
                u = x + Δx * d

                if not (0 <= v < H and 0 <= u < W):
                    break

                Δheatloss += GRID[v, u]

                if d >= mn:
                    new_heatloss = heatloss + Δheatloss
                    if heatlosses.get((v, u, Δy, Δx), float("inf")) > new_heatloss:
                        heatlosses[v, u, Δy, Δx] = new_heatloss
                        heappush(heap, (new_heatloss, v, u, Δy, Δx))


aoc_lube.submit(2023, 17, 1, lambda: min_heatloss(1, 3))
aoc_lube.submit(2023, 17, 2, lambda: min_heatloss(4, 10))
