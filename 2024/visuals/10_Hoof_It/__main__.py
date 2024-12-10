import asyncio

import aoc_lube
import numpy as np
from aoc_lube.utils import grid_steps
from aoc_theme import AOC_THEME, AocText
from batgrl.app import App
from batgrl.colors import BLACK, WHITE, lerp_colors, rainbow_gradient
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.geometry.easings import out_elastic
from batgrl.text_tools import new_cell

GRAD = [lerp_colors(color, BLACK, 0.55) for color in rainbow_gradient(10)]


def gen_trails():
    grid = aoc_lube.fetch(year=2024, day=10).splitlines()
    H, W = len(grid), len(grid[0])
    maze = np.full((2 * H + 1, 2 * W + 1), new_cell(char="#"))
    for (y1, x1), (y2, x2) in grid_steps(4, H, W):
        a = grid[y1][x1]
        b = grid[y2][x2]
        maze["char"][2 * y1 + 1, 2 * x1 + 1] = a
        maze["fg_color"][2 * y1 + 1, 2 * x1 + 1] = GRAD[int(a)]
        maze["char"][2 * y2 + 1, 2 * x2 + 1] = b
        maze["fg_color"][2 * y2 + 1, 2 * x2 + 1] = GRAD[int(b)]
        if int(b) - int(a) == 1:
            maze["char"][y1 + y2 + 1, x1 + x2 + 1] = "."
            maze["fg_color"][y1 + y2 + 1, x1 + x2 + 1] = lerp_colors(
                GRAD[int(a)], GRAD[int(b)], 0.5
            )
    return maze


TRAILS = gen_trails()
N = 30
GLOWS = [
    [lerp_colors(color, WHITE, 0.3 * out_elastic(i / N)) for i in range(N)]
    for color in GRAD
]


async def trail_glow():
    offset = 0
    while True:
        for i in range(10):
            TRAILS["fg_color"][TRAILS["char"] == str(i)] = GLOWS[i][(i + offset) % N]
        offset -= 1
        await asyncio.sleep(0.05)


class HoofItApp(App):
    async def on_start(self):
        trails = AocText(size=TRAILS.shape)

        sv = ScrollView(
            size_hint={"height_hint": 1.0, "width_hint": 1.0}, dynamic_bars=True
        )
        sv.view = trails

        self.add_gadget(sv)
        TRAILS["fg_color"][TRAILS["char"] == "#"] = trails.default_fg_color
        TRAILS["bg_color"] = trails.default_bg_color
        trails.canvas = TRAILS

        await trail_glow()


HoofItApp(title="Hoof It", color_theme=AOC_THEME).run()
