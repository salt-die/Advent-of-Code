import asyncio
from cmath import log

import aoc_lube
import numpy as np
from aoc_lube.utils import GRID_NEIGHBORHOODS, grid_steps
from aoc_theme import AOC_THEME, AocText, AocToggle
from batgrl.app import App
from batgrl.colors import BLACK, WHITE, lerp_colors, rainbow_gradient
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.geometry.easings import out_elastic
from batgrl.text_tools import new_cell

GRAD = [lerp_colors(color, BLACK, 0.55) for color in rainbow_gradient(10)]


def line_char(y, x, maze):
    h, w = maze.shape
    return " ╺╻┏╸━┓┳╹┗┃┣┛┻┫╋"[
        sum(
            2 ** round(log(complex(x + dx, y + dy) - complex(x, y), 1j).real % 4)
            for dy, dx in GRID_NEIGHBORHOODS[4]
            if 0 <= y + dy < h
            and 0 <= x + dx < w
            and maze["char"][y + dy, x + dx] != "#"
        )
    ]


def gen_trails():
    grid = aoc_lube.fetch(year=2024, day=10).splitlines()
    H, W = len(grid), len(grid[0])
    maze = np.full((2 * H + 1, 2 * W + 1), new_cell(char="#"))
    maze2 = np.full((2 * H + 1, 2 * W + 1), new_cell(char=" "))

    for (y1, x1), (y2, x2) in grid_steps(4, H, W):
        a = grid[y1][x1]
        b = grid[y2][x2]
        maze["char"][2 * y1 + 1, 2 * x1 + 1] = a
        maze["fg_color"][2 * y1 + 1, 2 * x1 + 1] = GRAD[int(a)]
        maze["char"][2 * y2 + 1, 2 * x2 + 1] = b
        maze["fg_color"][2 * y2 + 1, 2 * x2 + 1] = GRAD[int(b)]
        if int(b) - int(a) == 1:
            maze["char"][y1 + y2 + 1, x1 + x2 + 1] = "."
    for y in range(2 * H + 1):
        for x in range(2 * W + 1):
            maze2["char"][y, x] = line_char(y, x, maze)

    maze2["fg_color"] = maze["fg_color"]
    maze2["char"][maze["char"] == "#"] = " "
    maze2["char"][maze["char"] == "0"] = "○"
    maze2["char"][maze["char"] == "9"] = "▽"
    return maze, maze2


TRAILS, UNICODE = gen_trails()
N = 30
GLOWS = [
    [lerp_colors(color, WHITE, 0.3 * out_elastic(i / N)) for i in range(N)]
    for color in GRAD
]


def smooth_colors():
    h, w = TRAILS.shape
    for y, x in np.argwhere(TRAILS["char"] == "."):
        color = np.zeros(3, int)
        n = 0
        for dy, dx in GRID_NEIGHBORHOODS[4]:
            if (
                0 <= y + dy < h
                and 0 <= x + dx < w
                and TRAILS["char"][y + dy, x + dx] != "#"
            ):
                color += TRAILS["fg_color"][y + dy, x + dx]
                n += 1
        if n:
            TRAILS["fg_color"][y, x] = color // n


async def trail_glow():
    offset = 0
    while True:
        for i in range(10):
            TRAILS["fg_color"][TRAILS["char"] == str(i)] = GLOWS[i][(i + offset) % N]
        smooth_colors()
        UNICODE["fg_color"] = TRAILS["fg_color"]
        offset -= 1
        await asyncio.sleep(0.05)


class HoofItApp(App):
    async def on_start(self):
        unicode = AocText(size=TRAILS.shape, is_enabled=False)
        trails = AocText(size=TRAILS.shape)
        trails.add_gadget(unicode)

        def toggle_display(state):
            unicode.is_enabled = state == "on"

        button = AocToggle(
            "Lines Only", toggle_display, pos_hint={"x_hint": 1.0, "anchor": "right"}
        )
        header = AocText(size=(1, 1), size_hint={"width_hint": 1.0})
        header.add_gadget(button)

        sv = ScrollView(
            pos=(1, 0),
            size_hint={"height_hint": 1.0, "width_hint": 1.0, "height_offset": -1},
            dynamic_bars=True,
        )
        sv.view = trails

        self.add_gadgets(header, sv)
        TRAILS["fg_color"][TRAILS["char"] == "#"] = trails.default_fg_color
        TRAILS["bg_color"] = trails.default_bg_color
        trails.canvas = TRAILS
        unicode.canvas = UNICODE
        UNICODE["bg_color"] = TRAILS["bg_color"]

        await trail_glow()


HoofItApp(title="Hoof It", color_theme=AOC_THEME).run()
