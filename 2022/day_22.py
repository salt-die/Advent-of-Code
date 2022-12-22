import re

import aoc_lube
# (FACE, DY, DX)     ->     (FACE, DY, DX,  Y,  X)
PORTALS_2D = {
    (0, -1, +0): lambda y, x: (4, -1,  0, -1,  x),
    (0, +1, +0): lambda y, x: (2,  1,  0,  0,  x),
    (0, +0, -1): lambda y, x: (1,  0, -1,  y, -1),
    (0, +0, +1): lambda y, x: (1,  0,  1,  y,  0),
    (1, -1, +0): lambda y, x: (1, -1,  0, -1,  x),
    (1, +1, +0): lambda y, x: (1,  1,  0,  0,  x),
    (1, +0, -1): lambda y, x: (0,  0, -1,  y, -1),
    (1, +0, +1): lambda y, x: (0,  0,  1,  y,  0),
    (2, -1, +0): lambda y, x: (0, -1,  0, -1,  x),
    (2, +1, +0): lambda y, x: (4,  1,  0,  0,  x),
    (2, +0, -1): lambda y, x: (2,  0, -1,  y, -1),
    (2, +0, +1): lambda y, x: (2,  0,  1,  y,  0),
    (3, -1, +0): lambda y, x: (5, -1,  0, -1,  x),
    (3, +1, +0): lambda y, x: (5,  1,  0,  0,  x),
    (3, +0, -1): lambda y, x: (4,  0, -1,  y, -1),
    (3, +0, +1): lambda y, x: (4,  0,  1,  y,  0),
    (4, -1, +0): lambda y, x: (2, -1,  0, -1,  x),
    (4, +1, +0): lambda y, x: (0,  1,  0,  0,  x),
    (4, +0, -1): lambda y, x: (3,  0, -1,  y, -1),
    (4, +0, +1): lambda y, x: (3,  0,  1,  y,  0),
    (5, -1, +0): lambda y, x: (3, -1,  0, -1,  x),
    (5, +1, +0): lambda y, x: (3,  1,  0,  0,  x),
    (5, +0, -1): lambda y, x: (5,  0, -1,  y, -1),
    (5, +0, +1): lambda y, x: (5,  0,  1,  y,  0),
}
PORTALS_3D = {
    (0, -1, +0): lambda y, x: (5,  0,  1,      x,  0),
    (0, +1, +0): lambda y, x: (2,  1,  0,      0,  x),
    (0, +0, -1): lambda y, x: (3,  0,  1, -y - 1,  0),
    (0, +0, +1): lambda y, x: (1,  0,  1,      y,  0),
    (1, -1, +0): lambda y, x: (5, -1,  0,     -1,  x),
    (1, +1, +0): lambda y, x: (2,  0, -1,      x, -1),
    (1, +0, -1): lambda y, x: (0,  0, -1,      y, -1),
    (1, +0, +1): lambda y, x: (4,  0, -1, -y - 1, -1),
    (2, -1, +0): lambda y, x: (0, -1,  0,     -1,  x),
    (2, +1, +0): lambda y, x: (4,  1,  0,      0,  x),
    (2, +0, -1): lambda y, x: (3,  1,  0,      0,  y),
    (2, +0, +1): lambda y, x: (1, -1,  0,     -1,  y),
    (3, -1, +0): lambda y, x: (2,  0,  1,      x,  0),
    (3, +1, +0): lambda y, x: (5,  1,  0,      0,  x),
    (3, +0, -1): lambda y, x: (0,  0,  1, -y - 1,  0),
    (3, +0, +1): lambda y, x: (4,  0,  1,      y,  0),
    (4, -1, +0): lambda y, x: (2, -1,  0,     -1,  x),
    (4, +1, +0): lambda y, x: (5,  0, -1,      x, -1),
    (4, +0, -1): lambda y, x: (3,  0, -1,      y, -1),
    (4, +0, +1): lambda y, x: (1,  0, -1, -y - 1, -1),
    (5, -1, +0): lambda y, x: (3, -1,  0,     -1,  x),
    (5, +1, +0): lambda y, x: (1,  1,  0,      0,  x),
    (5, +0, -1): lambda y, x: (0,  1,  0,      0,  y),
    (5, +0, +1): lambda y, x: (4, -1,  0,     -1,  y),
}
FACE_UV = ((0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (3, 0))
FACING_ENUM = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}

def parse_raw():
    map_, directions = aoc_lube.fetch(year=2022, day=22).split("\n\n")
    lines = map_.splitlines()
    L = len(lines) // 4
    floor = {(y, x): c for y, line in enumerate(lines) for x, c in enumerate(line)}
    faces =  [
        {(y, x): floor[u * L + y, v * L + x] for y in range(L) for x in range(L)}
        for u, v in FACE_UV
    ]
    return L, faces, re.findall(r"\d+|R|L", directions)

L, FACES, INSTRUCTIONS = parse_raw()

def move(face, dy, dx, y, x, portals):
    ny, nx = y + dy, x + dx
    if 0 <= ny < L and 0 <= nx < L:
        if FACES[face][ny, nx] == ".":
            return face, dy, dx, ny, nx
    else:
        nface, ndy, ndx, ny, nx = portals[face, dy, dx](y, x)
        ny %= L
        nx %= L

        if FACES[nface][ny, nx] == ".":
            return nface, ndy, ndx, ny, nx
    return face, dy, dx, y, x

def move_all(portals):
    face, dy, dx, y, x = 0, 0, 1, 0, 0
    for instruction in INSTRUCTIONS:
        match instruction:
            case "R":
                dy, dx = dx, -dy
            case "L":
                dy, dx = -dx, dy
            case distance:
                for _ in range(int(distance)):
                    face, dy, dx, y, x = move(face, dy, dx, y, x, portals)
    u, v = FACE_UV[face]
    return 1000 * (u * L + y + 1) + 4 * (v * L + x + 1) + FACING_ENUM[dy, dx]

def part_one():
    return move_all(PORTALS_2D)

def part_two():
    return move_all(PORTALS_3D)

aoc_lube.submit(year=2022, day=22, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=22, part=2, solution=part_two)
