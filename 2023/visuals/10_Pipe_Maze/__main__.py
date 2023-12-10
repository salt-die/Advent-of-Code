import asyncio
from typing import NamedTuple

import aoc_lube
from aoc_theme import (
    AOC_GREEN_ON_BLUE,
    AOC_PRIMARY,
    AOC_SECONDARY,
    AOC_THEME,
    AocToggle,
)
from batgrl.app import App
from batgrl.colors import Color
from batgrl.gadgets.scroll_view import ScrollView
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

        def toggle_display(state):
            if state == "on":
                unicode_pipes.pos = ascii_pipes.pos
                sv.view = unicode_pipes
            else:
                ascii_pipes.pos = unicode_pipes.pos
                sv.view = ascii_pipes

        display_toggle = AocToggle("Unicode", toggle_display, toggle_state="on")

        delay = 0.1

        def toggle_delay(state):
            nonlocal delay
            if state == "on":
                delay = 0
            else:
                delay = 0.1

        delay_toggle = AocToggle("Fast Update", toggle_delay, pos=(1, 0))
        self.add_gadgets(sv, display_toggle, delay_toggle)

        def show_pos(pos):
            """Scroll to pos."""
            if (
                sv.is_grabbed
                or sv._horizontal_bar.is_grabbed
                or sv._vertical_bar.is_grabbed
            ):
                return
            y1, x1 = (
                unicode_pipes.pos
                if display_toggle.toggle_state == "on"
                else ascii_pipes.pos
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

        ascii_line = Text(size=(1, 1), default_color_pair=AOC_SECONDARY)
        unicode_line = Text(size=(1, 1), default_color_pair=AOC_SECONDARY)
        ascii_pipes.add_gadget(ascii_line)
        unicode_pipes.add_gadget(unicode_line)

        ascii_line.colors[..., 3:] = RED
        unicode_line.colors[..., 3:] = RED

        for y in range(H):
            ascii_line.y = y
            unicode_line.y = y

            inside = False
            for x in range(W):
                pos = ascii_line.pos = unicode_line.pos = y, x

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
                        ascii_line.colors[..., 3:] = GREEN
                        unicode_line.colors[..., 3:] = GREEN
                    else:
                        ascii_line.colors[..., 3:] = RED
                        unicode_line.colors[..., 3:] = RED

                await asyncio.sleep(delay)


if __name__ == "__main__":
    PipeApp(title="Pipe Maze", color_theme=AOC_THEME).run()
