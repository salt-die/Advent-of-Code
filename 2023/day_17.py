from heapq import heappop, heappush

import aoc_lube
from aoc_lube.utils import int_grid

GRID = int_grid(aoc_lube.fetch(year=2023, day=17))
H, W = GRID.shape


def min_heatloss(mn, mx):
    q = [(0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]
    heatlosses = {}
    while q:
        cost, y, x, dy, dx = heappop(q)
        if y == H - 1 and x == W - 1:
            return cost

        for dy, dx in ((-dx, dy), (dx, -dy)):
            new_heatloss = 0
            for d in range(1, mx + 1):
                v = y + dy * d
                u = x + dx * d

                if not (0 <= v < H and 0 <= u < W):
                    break

                new_heatloss += GRID[v, u]

                if d >= mn:
                    new_cost = cost + new_heatloss
                    if heatlosses.get((v, u, dy, dx), float("inf")) > new_cost:
                        heatlosses[v, u, dy, dx] = new_cost
                        heappush(q, (new_cost, v, u, dy, dx))


aoc_lube.submit(2023, 17, 1, lambda: min_heatloss(1, 3))
aoc_lube.submit(2023, 17, 2, lambda: min_heatloss(4, 10))
