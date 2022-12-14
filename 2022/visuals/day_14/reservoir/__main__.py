import asyncio
from collections import deque

import numpy as np

from nurses_2.app import App
from nurses_2.colors import Color, ColorPair, ColorTheme
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.scroll_view import ScrollView

import aoc_lube
from aoc_lube.utils import chunk, extract_ints, pairwise

AIR, ROCK, SAND = 0, 1, 2
MINX, MAXX, MAXY = 341, 659, 159  # From inspection
AIR_COLOR = Color.from_hex("211e1e")
ROCK_COLOR = Color.from_hex("64626b")
SAND_COLOR = Color.from_hex("af803a")
AOC_GREEN = Color.from_hex("009900")
AOC_BRIGHT_GREEN = Color.from_hex("99ff99")
AOC_BLUE = Color.from_hex("0f0f23")
AOC_GREY = Color.from_hex("cccccc")
GREY_ON_BLUE = ColorPair.from_colors(AOC_GREY, AOC_BLUE)
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

def create_cave():
    coordinates = (
        chunk(extract_ints(line), 2)
        for line in aoc_lube.fetch(year=2022, day=14).splitlines()
    )

    cave = np.zeros((MAXY + 1, MAXX - MINX + 1), int)

    for path in coordinates:
        for (x1, y1), (x2, y2) in pairwise(path):
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))
            cave[y1, x1 - MINX: x2 - MINX + 1] = ROCK
            cave[y1: y2 + 1, x1 - MINX] = ROCK

    cave[-1] = ROCK
    return cave


class ReservoirApp(App):
    async def on_start(self):
        cave = create_cave()

        cave_widget = TextWidget(size=cave.shape, default_color_pair=GREY_ON_BLUE)
        cave_widget.canvas[cave==AIR] = "."
        cave_widget.colors[..., :3][cave==AIR] = AIR_COLOR
        cave_widget.canvas[cave==ROCK] = "#"
        cave_widget.colors[..., :3][cave==ROCK] = ROCK_COLOR

        cave_view = ScrollView(size_hint=(1.0, 1.0), disable_ptf=True)
        cave_view.view = cave_widget
        cave_view.horizontal_proportion = .5

        sand_count_label = TextWidget(
            size=(1, 17),
            pos_hint=(None, .5),
            anchor="center",
            default_color_pair=GREY_ON_BLUE,
        )

        self.add_widgets(cave_view, sand_count_label)

        particles = deque()

        def update_cave(old, new):
            if old is not None:
                cave[old] = AIR
                cave_widget.canvas[old] = "."
                cave_widget.colors[old][:3] = AIR_COLOR

            cave[new] = SAND
            cave_widget.canvas[new] = "o"
            cave_widget.colors[new][:3] = SAND_COLOR
            particles.append(new)


        tick = sand_count = 0
        while cave[0, 500 - MINX] != SAND:
            if tick % 4 == 0:
                update_cave(None, (0, 500 - MINX))
                sand_count += 1
                sand_count_label.add_text(f"Sand count: {sand_count:<5}")

            for _ in range(len(particles)):
                pos = y, x = particles.popleft()
                for dx in (0, -1, 1):
                    if cave[y + 1, x + dx] == AIR:
                        update_cave(pos, (y + 1, x + dx))
                        break

            tick += 1
            await asyncio.sleep(0)


ReservoirApp(
    title="Regolith Reservoir",
    color_theme=AOC_THEME,
    background_color_pair=GREY_ON_BLUE,
).run()
