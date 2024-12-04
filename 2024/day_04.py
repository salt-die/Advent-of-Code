import aoc_lube
from aoc_lube.utils import GRID_NEIGHBORHOODS

BOARD = aoc_lube.fetch(year=2024, day=4).splitlines()
H, W = len(BOARD), len(BOARD[0])
MOORE = GRID_NEIGHBORHOODS[8]
DIAGS = MOORE[4:]


def is_word(y, x, dy, dx, word):
    for i, char in enumerate(word):
        j = y + i * dy
        k = x + i * dx
        if not (0 <= j < H and 0 <= k < W and BOARD[j][k] == char):
            return False
    return True


def is_x_mas(y, x):
    top_left = is_word(y, x, 1, 1, "MAS") or is_word(y, x, 1, 1, "SAM")
    top_right = is_word(y, x + 2, 1, -1, "MAS") or is_word(y, x + 2, 1, -1, "SAM")
    return top_left and top_right


def part_one():
    return sum(
        is_word(y, x, dy, dx, "XMAS")
        for y in range(H)
        for x in range(W)
        for dy, dx in MOORE
    )


def part_two():
    return sum(is_x_mas(y, x) for y in range(H) for x in range(W))


aoc_lube.submit(year=2024, day=4, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=4, part=2, solution=part_two)
