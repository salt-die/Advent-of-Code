import asyncio
from typing import NamedTuple

import aoc_lube
from aoc_theme import (
    AOC_BRIGHT_GREEN,
    AOC_BRIGHT_GREEN_ON_BLUE,
    AOC_GREEN_ON_BLUE,
    AOC_PRIMARY,
    AOC_SECONDARY,
    AOC_THEME,
)
from batgrl.app import App
from batgrl.colors import Color
from batgrl.gadgets.behaviors.toggle_button_behavior import ToggleButtonBehavior
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.slider import Slider
from batgrl.gadgets.text import Text

GREEN = Color.from_hex("22cc39")
RED = Color.from_hex("dd3330")


class P(NamedTuple):
    y: int
    x: int

    def __add__(a, b):
        return P(a.y + b.y, a.x + b.x)


N, E, S, W = P(-1, 0), P(0, 1), P(1, 0), P(0, -1)
Δs = {"|": (N, S), "J": (N, W), "L": (N, E), "7": (S, W), "F": (S, E), "-": (W, E)}


def parse_raw():
    grid = {}
    for y, line in enumerate(aoc_lube.fetch(year=2023, day=10).splitlines()):
        for x, char in enumerate(line):
            grid[pos := P(y, x)] = char
            if char == "S":
                grid[pos] = "|"  # by inspection
                yield pos

    yield y + 1, x + 1
    yield grid


START, (H, W), GRID = parse_raw()
ASCII_PIPES = aoc_lube.fetch(year=2023, day=10)
UNICODE_PIPES = ASCII_PIPES.translate(str.maketrans("|JL7F-", "│┘└┐┌─"))
HEAVY_PIPES = dict(zip("|JL7F-", "┃┛┗┓┏━"))


class AocToggle(ToggleButtonBehavior, Text):
    def __init__(self, label, callback):
        super().__init__(toggle_state="on")
        self.set_text(f"[[ ] {label}]")
        self.update_on()
        self.update_normal()
        self.callback = callback

    def update_hover(self):
        self.colors[:] = AOC_BRIGHT_GREEN_ON_BLUE

    def update_normal(self):
        self.colors[:] = AOC_GREEN_ON_BLUE

    def update_on(self):
        self.canvas[0, 2]["char"] = "x"

    def update_off(self):
        self.canvas[0, 2]["char"] = " "

    def on_release(self):
        self.callback(self.toggle_state)


class PipeApp(App):
    async def on_start(self):
        ascii_pipes = Text(default_color_pair=AOC_PRIMARY)
        ascii_pipes.set_text(ASCII_PIPES)
        ascii_pipes.colors[START] = AOC_GREEN_ON_BLUE

        unicode_pipes = Text(default_color_pair=AOC_PRIMARY)
        unicode_pipes.set_text(UNICODE_PIPES)
        unicode_pipes.colors[START] = AOC_GREEN_ON_BLUE

        sv = ScrollView(
            size_hint={"height_hint": 1.0, "width_hint": 1.0}, disable_ptf=True
        )
        sv.view = unicode_pipes

        def toggle_callback(state):
            if state == "on":
                sv.view = unicode_pipes
            else:
                sv.view = ascii_pipes

        button = AocToggle("Toggle Unicode", toggle_callback)

        delay_label = Text(pos=(1, 0), default_color_pair=AOC_GREEN_ON_BLUE)
        delay_label.set_text("Update delay:".ljust(20))

        delay = 0.1

        def update_delay(t):
            nonlocal delay
            delay = t

        delay_slider = Slider(
            pos=(1, 14),
            size=(1, 6),
            min=0,
            max=0.2,
            start_value=0.1,
            callback=update_delay,
            default_color_pair=AOC_GREEN_ON_BLUE,
            handle_color_pair=AOC_GREEN_ON_BLUE,
            fill_color=AOC_BRIGHT_GREEN,
        )

        self.add_gadgets(sv, button, delay_label, delay_slider)

        def show_pos(pos):
            """Scroll to pos."""
            if (
                sv.is_grabbed
                or sv._horizontal_bar.is_grabbed
                or sv._vertical_bar.is_grabbed
            ):
                return
            y1, x1 = (
                unicode_pipes.pos if button.toggle_state == "on" else ascii_pipes.pos
            )
            y2, x2 = pos
            abs_y, abs_x = y1 + y2, x1 + x2

            if abs_y < 0:
                sv._scroll_down(abs_y - 1)
            elif abs_y >= sv.port_height:
                sv._scroll_up(sv.port_height - abs_y - 1)

            if abs_x < 0:
                sv._scroll_right(abs_x - 1)
            elif abs_x >= sv.port_width:
                sv._scroll_left(sv.port_width - abs_x - 1)

        stack = [START]
        cycle = set()
        while stack:
            cycle.add(pos := stack.pop())
            stack.extend(pos + Δ for Δ in Δs[GRID[pos]] if pos + Δ not in cycle)
            ascii_pipes.colors[pos] = AOC_SECONDARY
            ascii_pipes.canvas[pos]["bold"] = True
            unicode_pipes.colors[pos] = AOC_SECONDARY
            unicode_pipes.canvas[pos]["char"] = HEAVY_PIPES[GRID[pos]]
            show_pos(pos)
            await asyncio.sleep(delay)

        ascii_line = Text(
            size=(1, 1), default_char="-", default_color_pair=AOC_PRIMARY.reversed()
        )
        unicode_line = Text(
            size=(1, 1), default_char="─", default_color_pair=AOC_PRIMARY.reversed()
        )
        ascii_pipes.add_gadget(ascii_line)
        unicode_pipes.add_gadget(unicode_line)
        inside_label = Text(pos=(2, 0), size=(1, 20), default_color_pair=AOC_PRIMARY)

        self.add_gadget(inside_label)
        inside_label.add_str("OUTSIDE PIPE".center(20))
        inside_label.colors[..., :3] = RED
        ascii_line.colors[..., 3:] = RED
        unicode_line.colors[..., 3:] = RED

        for y in range(H):
            ascii_line.y = y
            unicode_line.y = y

            inside = False
            for x in range(W):
                pos = ascii_line.pos = unicode_line.pos = y, x
                ascii_line.canvas[:] = ascii_pipes.canvas[pos]
                unicode_line.canvas[:] = unicode_pipes.canvas[pos]

                if pos not in cycle:
                    if inside:
                        ascii_pipes.colors[y, x, :3] = GREEN
                        unicode_pipes.colors[y, x, :3] = GREEN

                    else:
                        ascii_pipes.colors[y, x, :3] = RED
                        unicode_pipes.colors[y, x, :3] = RED

                elif GRID[pos] in "|F7":
                    inside = not inside
                    if inside:
                        inside_label.add_str(" INSIDE PIPE".center(20))
                        inside_label.colors[..., :3] = GREEN
                        ascii_line.colors[..., 3:] = GREEN
                        unicode_line.colors[..., 3:] = GREEN
                    else:
                        inside_label.add_str("OUTSIDE PIPE".center(20))
                        inside_label.colors[..., :3] = RED
                        ascii_line.colors[..., 3:] = RED
                        unicode_line.colors[..., 3:] = RED

                show_pos(pos)

                await asyncio.sleep(delay)


if __name__ == "__main__":
    PipeApp(title="Pipe Maze", color_theme=AOC_THEME).run()
