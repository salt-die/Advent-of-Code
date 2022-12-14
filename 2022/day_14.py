import aoc_lube
from aoc_lube.utils import extract_ints, chunk, pairwise

AIR, ROCK, SAND = 0, 1, 2


class CaveDict(dict):
    def __missing__(self, key):
        if key[1] == self.bottom:
            self[key] = ROCK
        else:
            self[key] = AIR

        return self[key]


def parse_raw():
    coordinates = (
        chunk(extract_ints(line), 2)
        for line in aoc_lube.fetch(year=2022, day=14).splitlines()
    )

    cave = CaveDict()

    for path in coordinates:
        for (x1, y1), (x2, y2) in pairwise(path):
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))

            for y in range(y1, y2 + 1):
                cave[x1, y] = 1

            for x in range(x1, x2 + 1):
                cave[x, y1] = 1

    cave.bottom = max(y for _, y in cave) + 2
    return cave

CAVE = parse_raw()

def fill_cave(bottom):
    while CAVE[500, 0] != SAND:
        x = 500
        for y in range(bottom):
            for dx in (0, -1, 1):
                if CAVE[x + dx, y + 1] == AIR:
                    x += dx
                    break
            else:
                CAVE[x, y] = SAND
                break
        else:
            break

    return sum(floor == SAND for floor in CAVE.values())

def part_one():
    return fill_cave(CAVE.bottom - 2)

def part_two():
    return fill_cave(CAVE.bottom)

aoc_lube.submit(year=2022, day=14, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=14, part=2, solution=part_two)
