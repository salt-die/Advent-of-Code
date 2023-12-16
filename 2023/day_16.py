import aoc_lube

GRID = aoc_lube.fetch(year=2023, day=16).splitlines()
H, W = len(GRID), len(GRID[0])


def bounce(start):
    states = set()
    positions = set()
    stack = [start]
    while stack:
        y, x, dy, dx = stack.pop()
        if (y, x, dy, dx) in states:
            continue
        states.add((y, x, dy, dx))

        y += dy
        x += dx

        if not (0 <= y < H and 0 <= x < W):
            continue

        match GRID[y][x]:
            case "/":
                dy, dx = -dx, -dy
            case "\\":
                dy, dx = dx, dy
            case "|" if dx:
                stack.append((y, x, -1, 0))
                dy, dx = 1, 0
            case "-" if dy:
                stack.append((y, x, 0, -1))
                dy, dx = 0, 1

        positions.add((y, x))
        stack.append((y, x, dy, dx))

    return len(positions)


def part_one():
    return bounce((0, -1, 0, 1))


def grid_boundary_points():
    for y in range(H):
        yield y, -1, 0, 1
        yield y, W, 0, -1
    for x in range(W):
        yield -1, x, 1, 0
        yield H, x, -1, 0


def part_two():
    return max(map(bounce, grid_boundary_points()))


aoc_lube.submit(year=2023, day=16, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=16, part=2, solution=part_two)
