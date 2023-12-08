import asyncio
from collections import deque, defaultdict

import aoc_lube
import numpy as np
from nurses_2.app import App
from nurses_2.colors import Color, ColorPair, ColorTheme, rainbow_gradient
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.scroll_view import ScrollView

AOC_GREEN = Color.from_hex("009900")
AOC_BRIGHT_GREEN = Color.from_hex("99ff99")
AOC_BLUE = Color.from_hex("0f0f23")
AOC_GREY = Color.from_hex("cccccc")
FADELEN = 100
FADE = np.array([AOC_GREY] + rainbow_gradient(FADELEN))
DEFAULT_COLOR_PAIR = ColorPair.from_colors(AOC_GREY, AOC_BLUE)
AOC_THEME = ColorTheme(
    primary_fg=AOC_BRIGHT_GREEN,
    primary_bg=AOC_BRIGHT_GREEN,
    primary_fg_light=AOC_GREEN,
    primary_bg_light=AOC_GREEN,
    primary_fg_dark=AOC_BLUE,
    primary_bg_dark=AOC_BLUE,
    secondary_fg=AOC_BRIGHT_GREEN,
    secondary_bg=AOC_BRIGHT_GREEN,
)

ELVES = {
    complex(y + 15, x + 15)
    for y, line in enumerate(aoc_lube.fetch(year=2022, day=23).splitlines())
    for x, c in enumerate(line)
    if c == "#"
}
N, S, W, E = -1, 1, -1j, 1j
NE, SE, NW, SW = N + E, S + E, N + W, S + W
NEIGHBORS = N, NE, NW, S, SE, SW, W, E
ALL_CHECKS = deque(((N, NE, NW), (S, SE, SW), (W, NW, SW), (E, NE, SE)))

def do_round():
    moves = defaultdict(list)
    for elf in ELVES:
        if any(elf + dyx in ELVES for dyx in NEIGHBORS):
            for check in ALL_CHECKS:
                if all(elf + dyx not in ELVES for dyx in check):
                    moves[elf + check[0]].append(elf)
                    break

    for proposal, [elf, *other_elves] in moves.items():
        if not other_elves:
            ELVES.symmetric_difference_update((elf, proposal))

    ALL_CHECKS.rotate(-1)
    return bool(moves)


class UnstableDiffusion(App):
    async def on_start(self):
        elves = TextWidget(default_color_pair=DEFAULT_COLOR_PAIR, default_char=".", size=(150, 150))

        scroll_view = ScrollView(size_hint=(1.0, 1.0))
        scroll_view.view = elves

        self.add_widget(scroll_view)

        def where_elves():
            elf_grid = np.zeros((150, 150), bool)
            for elf in ELVES:
                elf_grid[round(elf.real), round(elf.imag)] = True

            elves.canvas[:] = "."
            elves.canvas[elf_grid] = "#"

            return elf_grid

        grid = where_elves()
        heat = 0 * grid
        while True:
            elves_moved = do_round()
            new_grid = where_elves()
            heat = np.clip(heat - 1, 0, None)
            heat[grid != new_grid] = FADELEN
            elves.colors[..., :3] = FADE[heat]
            grid = new_grid

            if not elves_moved:
                break

            await asyncio.sleep(0)


UnstableDiffusion(title="Unstable Diffusion", color_theme=AOC_THEME).run()
