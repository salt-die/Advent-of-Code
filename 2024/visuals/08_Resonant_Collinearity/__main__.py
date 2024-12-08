import asyncio
from itertools import combinations
from time import perf_counter

import numpy as np
from aoc_theme import AOC_THEME, AocButton, AocText
from batgrl.app import App
from batgrl.colors import WHITE, lerp_colors, rainbow_gradient
from batgrl.gadgets.behaviors.toggle_button_behavior import ToggleButtonBehavior
from batgrl.gadgets.text import Text
from batgrl.text_tools import new_cell

FREQ = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
COLORS = dict(zip(FREQ, rainbow_gradient(len(FREQ))))


def decay(distance):
    return np.e ** (-0.15 * distance)


def pode_color(freq, distance):
    color = COLORS[freq]
    p = np.cos(2.5 * perf_counter() * distance) / (5 / 2) + 0.4
    color = lerp_colors(color, WHITE, p)
    d = decay(distance)
    return tuple(int(d * n) for n in color)


def mark_podes(y, x, dy, dx, freq, canvas, distances):
    h, w = canvas.shape
    i = 0
    while 0 <= y < h and 0 <= x < w:
        if i < distances[y, x]:
            distances[y, x] = i
            canvas["char"][y, x] = freq if i == 0 else "#"
            canvas["fg_color"][y, x] = pode_color(freq, i)
        y += dy
        x += dx
        i += 1


class FreqToggle(ToggleButtonBehavior, Text):
    def __init__(self, freq, grid):
        self.freq = freq
        self.grid = grid
        super().__init__(size=(1, 1), group=0, is_transparent=True, alpha=0)
        self.set_text(freq, fg_color=COLORS[freq])
        if self.toggle_state == "on":
            self.update_on()
        else:
            self.update_normal()

    def on_toggle(self):
        if self.toggle_state == "on":
            self.grid.freq = self.freq

    def update_normal(self):
        if self.toggle_state != "on":
            self.canvas["fg_color"] = COLORS[self.freq]

    def update_hover(self):
        if self.toggle_state != "on":
            self.canvas["fg_color"] = lerp_colors(COLORS[self.freq], WHITE, 0.5)

    def update_on(self):
        self.canvas["fg_color"] = WHITE

    def update_off(self):
        if self.button_state == "normal":
            self.update_normal()
        else:
            self.update_hover()


class PodeGrid(AocText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_cell = new_cell(char=".")
        self.freq = "a"
        self.on_size()

    def on_size(self):
        super().on_size()
        self.podes = np.zeros(self.size, dtype="U1")

    def on_mouse(self, mouse_event):
        if (
            not self.collides_point(mouse_event.pos)
            or mouse_event.event_type != "mouse_down"
        ):
            return
        y, x = self.to_local(mouse_event.pos)
        if self.podes[y, x] != self.freq:
            self.podes[y, x] = self.freq
        else:
            self.podes[y, x] = ""


class ResonantCollinearityApp(App):
    async def on_start(self):
        grid = PodeGrid(
            pos=(1, 0),
            size_hint={"height_hint": 1.0, "width_hint": 1.0, "height_offset": -1},
        )
        header = AocText(size=(1, 31), size_hint={"width_hint": 1.0, "min_width": 31})
        header.add_str("Frequency:")
        for i, freq in enumerate(FREQ):
            toggle = FreqToggle(freq, grid)
            toggle.x = 11 + i
            header.add_gadget(toggle)

        def reset_grid():
            grid.podes[:] = ""

        reset = AocButton(
            "Reset", reset_grid, pos_hint={"x_hint": 1.0, "anchor": "right"}
        )
        header.add_gadget(reset)

        self.add_gadgets(header, grid)

        while True:
            grid.clear()
            distances = np.full(grid.size, float("inf"))
            for freq in FREQ:
                positions = np.argwhere(grid.podes == freq)
                if len(positions) == 1:
                    [[y, x]] = positions
                    grid.canvas["char"][y, x] = freq
                    distances[y, x] = 0
                    grid.canvas["fg_color"][y, x] = pode_color(freq, 0)

                for a, b in combinations(positions, r=2):
                    mark_podes(*a, *a - b, freq, grid.canvas, distances)
                    mark_podes(*b, *b - a, freq, grid.canvas, distances)

            await asyncio.sleep(0)


ResonantCollinearityApp(title="Resonant Collinearity", color_theme=AOC_THEME).run()
