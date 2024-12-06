import asyncio
from itertools import cycle

import aoc_lube
import numpy as np
from aoc_theme import AOC_THEME, AocButton, AocText, AocToggle
from batgrl.app import App
from batgrl.colors import Color, gradient
from batgrl.gadgets.scroll_view import ScrollView

PINK = Color.from_hex("dd58d7")
LIGHT_PINK = Color.from_hex("c997d8")
YELLOW = Color.from_hex("c8d326")
GREEN = Color.from_hex("0cd61a")
HEAD_COLORS = cycle(gradient(YELLOW, GREEN, 10) + gradient(GREEN, YELLOW, 10))
TAIL_COLORS = cycle(gradient(PINK, LIGHT_PINK, 6) + gradient(LIGHT_PINK, PINK, 6))

GRID = aoc_lube.fetch(year=2024, day=6)
HEAD = {(-1, 0): "^", (0, 1): ">", (1, 0): "v", (0, -1): "<"}
TAIL = {
    (-1, 0, -1, 0): "┃",
    (-1, 0, 0, 1): "┏",
    (-1, 0, 1, 0): "┃",
    (-1, 0, 0, -1): "┓",
    (0, 1, -1, 0): "┛",
    (0, 1, 0, 1): "━",
    (0, 1, 1, 0): "┓",
    (0, 1, 0, -1): "━",
    (1, 0, -1, 0): "┃",
    (1, 0, 0, 1): "┗",
    (1, 0, 1, 0): "┃",
    (1, 0, 0, -1): "┛",
    (0, -1, -1, 0): "┗",
    (0, -1, 0, 1): "━",
    (0, -1, 1, 0): "┏",
    (0, -1, 0, -1): "━",
}


class Grid(AocText):
    def on_mouse(self, mouse_event):
        if mouse_event.event_type == "mouse_down" and self.collides_point(
            mouse_event.pos
        ):
            y, x = self.to_local(mouse_event.pos)
            if self.canvas["char"][y, x] == "#":
                self.canvas["char"][y, x] = "."
            else:
                self.canvas["char"][y, x] = "#"


class GuardGallivantApp(App):
    async def on_start(self):
        delay = 0.05
        start_event = asyncio.Event()

        grid = Grid()
        grid.set_text(GRID)

        Y, X = np.argwhere(grid.canvas["char"] == "^").reshape(-1)
        grid.canvas["char"][Y, X] = "."

        path_overlay = AocText(size=grid.size, is_transparent=True, alpha=0)
        grid.add_gadget(path_overlay)

        grid_sv = ScrollView(
            pos=(1, 0),
            size_hint={
                "height_hint": 1.0,
                "width_hint": 1.0,
                "max_width": grid.width + 2,
                "max_height": grid.height + 2,
                "height_offset": -1,
            },
            dynamic_bars=True,
        )
        grid_sv.view = grid

        y, x = ly, lx = Y, X
        dy, dx = ldy, ldx = -1, 0

        start_button = AocButton("Start", start_event.set)
        stop_button = AocButton("Stop", start_event.clear)

        def reset():
            nonlocal y, x, ly, lx, dy, dx, ldy, ldx
            y, x = ly, lx = Y, X
            dy, dx = ldy, ldx = -1, 0
            start_event.clear()
            path_overlay.clear()
            grid.set_text(GRID)
            path_overlay.canvas["char"][y, x] = HEAD[dy, dx]
            path_overlay.canvas["fg_color"][y, x] = next(HEAD_COLORS)

        def clear():
            reset()
            grid.canvas["char"] = "."

        def toggle_turbo(state):
            nonlocal delay
            if state == "on":
                delay = 0.01
            else:
                delay = 0.05

        reset_button = AocButton("Reset", reset)
        clear_button = AocButton("Clear", clear)
        turbo_button = AocToggle(
            "TURBO",
            toggle_turbo,
            pos_hint={"x_hint": 1.0, "anchor": "right", "x_offset": -2},
        )
        stop_button.left = start_button.right
        reset_button.left = stop_button.right
        clear_button.left = reset_button.right

        header = AocText(
            size=(1, 1), size_hint={"width_hint": 1.0, "max_width": grid.width + 2}
        )
        header.add_gadgets(
            start_button, stop_button, reset_button, clear_button, turbo_button
        )
        self.add_gadgets(header, grid_sv)

        async def patrol():
            nonlocal y, x, ly, lx, dy, dx, ldy, ldx

            while start_event.is_set():
                if not (0 <= y < grid.height and 0 <= x < grid.width):
                    path_overlay.canvas["char"][ly, lx] = TAIL[ldy, ldx, dy, dx]
                    path_overlay.canvas["fg_color"][ly, lx] = next(TAIL_COLORS)
                    start_event.clear()
                    return

                if grid.canvas["char"][y, x] == "#":
                    y, x = ly, lx
                    ldy, ldx = dy, dx
                    dy, dx = dx, -dy
                else:
                    if y != ly or x != lx:
                        path_overlay.canvas["char"][ly, lx] = TAIL[ldy, ldx, dy, dx]
                        path_overlay.canvas["fg_color"][ly, lx] = next(TAIL_COLORS)
                        ldy, ldx = dy, dx
                    path_overlay.canvas["char"][y, x] = HEAD[dy, dx]
                    path_overlay.canvas["fg_color"][y, x] = next(HEAD_COLORS)
                    cy, cx = grid_sv.center
                    grid_sv.scroll_to_rect(
                        (y - cy, x - cx), (grid_sv.port_height, grid_sv.port_width)
                    )
                    ly, lx = y, x
                    y += dy
                    x += dx

                await asyncio.sleep(delay)

        while True:
            await start_event.wait()
            await patrol()


GuardGallivantApp(title="Guard Gallivant", color_theme=AOC_THEME).run()
