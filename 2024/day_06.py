import aoc_lube

GRID = aoc_lube.fetch(year=2024, day=6).splitlines()
START = next(
    (y, x) for y, line in enumerate(GRID) for x, char in enumerate(line) if char == "^"
)
H = len(GRID)
W = len(GRID[0])


def patrol(oy=-1, ox=-1):
    seen = set()
    y, x = START
    dy, dx = -1, 0
    while True:
        if not (0 <= y < H and 0 <= x < W):
            return False, len(seen)
        if GRID[y][x] == "#" or (y == oy and x == ox):
            y -= dy
            x -= dx
            dy, dx = dx, -dy
        elif (y, x, dy, dx) in seen:
            return True, len(seen)
        else:
            seen.add((y, x, dy, dx))
            y += dy
            x += dx


def part_one():
    return patrol()[1]


def part_two():
    return sum(patrol(y, x)[0] for y in range(H) for x in range(W) if GRID[y][x] == ".")


aoc_lube.submit(year=2024, day=6, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=6, part=2, solution=part_two)
