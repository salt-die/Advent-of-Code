import asyncio

import aoc_lube
import numpy as np
from batgrl.app import App
from batgrl.colors import GREEN, RED, Color, gradient
from batgrl.gadgets.graphics import Graphics
from batgrl.gadgets.scroll_view import ScrollView
from scipy.ndimage import convolve

from .aoc_theme import AOC_THEME, AocText, AocToggle

RAW = aoc_lube.fetch(year=2025, day=4)
DATA = np.array([[int(c == "@") for c in row] for row in RAW.splitlines()])
KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

PRIMARY_FG = Color.from_hex(AOC_THEME["primary_fg"])
GRAD = gradient(PRIMARY_FG, GREEN, RED, PRIMARY_FG, n=100)


async def remove_rolls(grid, braille, to_remove):
    for color in GRAD:
        grid.canvas["fg_color"][to_remove] = color
        braille.texture[:135, :135, :3][to_remove] = color
        await asyncio.sleep(0.01)
    grid.canvas["ord"][to_remove] = ord(".")
    braille.texture[:135, :135][to_remove] = 0


class Visual(App):
    async def on_start(self):
        grid = AocText()
        grid.set_text(RAW)  # 135, 135
        braille = Graphics(blitter="braille", size=(34, 68), is_enabled=False)
        braille.texture[:135, :135, 3][DATA.astype(bool)] = 255
        braille.texture[:135, :135, :3][DATA.astype(bool)] = grid.default_fg_color

        def on_toggle(toggle_state):
            braille.is_enabled = toggle_state == "on"
            sv.is_enabled = toggle_state == "off"

        toggle = AocToggle(
            "Braille",
            callback=on_toggle,
            pos_hint={"x_hint": 1.0, "anchor": "right", "x_offset": -2},
        )

        sv = ScrollView(
            size_hint={"height_hint": 1.0, "width_hint": 1.0}, dynamic_bars=True
        )
        sv.view = grid
        self.add_gadgets(sv, braille, toggle)

        rolls = DATA.copy()
        total_removed = 0
        while True:
            neighbors = convolve(rolls, KERNEL, mode="constant")
            to_remove = np.logical_and(rolls, neighbors < 4)

            nremoved = to_remove.sum()
            if nremoved == 0:
                break

            await remove_rolls(grid, braille, to_remove)

            total_removed -= nremoved
            rolls -= to_remove
            await asyncio.sleep(0.1)
