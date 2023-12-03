import asyncio
import re
from itertools import cycle
from pathlib import Path

import aoc_lube
from aoc_theme import (
    AOC_BLUE,
    AOC_BRIGHT_GREEN,
    AOC_GREY,
    AOC_PRIMARY,
    AOC_SECONDARY,
    AOC_THEME,
    AOC_YELLOW,
)
from batgrl.app import App
from batgrl.colors import ColorPair, rainbow_gradient
from batgrl.gadgets.animation import Animation
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.text import Text

RAINBOW = cycle(rainbow_gradient(20))
RAW = aoc_lube.fetch(year=2023, day=3)
GRID = RAW.splitlines()
GEAR = Path(__file__).parent / "gear"
H, W = len(GRID), len(GRID[0])
MATCHES = [list(re.finditer(r"(\d+)", line)) for line in GRID]
SYMBOLS = {}
YELLOW_ON_BLUE = ColorPair.from_colors(AOC_YELLOW, AOC_BLUE)
GREEN_ON_BLUE = ColorPair.from_colors(AOC_BRIGHT_GREEN, AOC_BLUE)


def is_inbounds(y, x):
    return 0 <= y < H and 0 <= x < W


class GearApp(App):
    async def on_start(self):
        number_highlighter = Gadget(
            size=(1, 1),
            background_color_pair=AOC_SECONDARY,
            is_transparent=True,
        )

        symbol_highlighter = Gadget(
            size=(1, 1),
            background_color_pair=AOC_SECONDARY.reversed(),
            is_transparent=True,
        )
        neighborhood_box = Text(
            size=(5, 5), default_color_pair=AOC_SECONDARY, is_transparent=True
        )
        grid = Text(default_color_pair=AOC_PRIMARY)
        grid.set_text(RAW)
        grid.add_gadgets(number_highlighter, symbol_highlighter, neighborhood_box)

        sv = ScrollView(
            pos=(0, 19),
            size_hint={"height_hint": 1.0, "width_hint": 1.0, "width_offset": -19},
            disable_ptf=True,
        )
        sv.view = grid

        def show_number():
            """Scroll to show highlighted number."""
            gy, gx = grid.pos
            y, x = number_highlighter.pos
            ay, ax = gy + y, gx + x
            if ay - 1 < 0:
                sv._scroll_down(ay - 2)
            elif ay + 2 >= sv.port_height:
                sv._scroll_up(sv.port_height - ay - 3)

            if ax - 1 < 0:
                sv._scroll_right(ax - 2)
            elif ax + number_highlighter.width + 1 >= sv.port_width:
                sv._scroll_left(sv.port_width - ax - number_highlighter.width - 2)

        sv.subscribe(number_highlighter, "pos", show_number)

        table = Text(size=(20, 19), default_color_pair=AOC_PRIMARY)
        table.canvas["char"][:, 8] = "┃"
        table.add_str(" Part 1 ┃  Part 2")
        table.add_str("━━━━━━━━╋━━━━━━━━━━", pos=(1, 0))
        table.add_str("━━━━━━━━╋━━━━━━━━━━", pos=(-2, 0))

        animation = Animation(
            path=GEAR,
            size_hint={"height_hint": 1.0, "height_offset": -20},
            size=(10, 19),
            pos=(20, 0),
        )
        animation.play()

        number_a = Text(is_enabled=False, default_color_pair=AOC_SECONDARY)
        number_b = Text(is_enabled=False, default_color_pair=AOC_SECONDARY)

        self.add_gadgets(sv, table, animation, number_a, number_b)

        def clockwise(y, x1, x2):
            for x in range(x1 - 1, x2 + 1):
                yield y - 1, x

            yield y, x2

            for x in range(x1 - 1, x2 + 1)[::-1]:
                yield y + 1, x

            yield y, x1 - 1

        gears = {}
        gear_total = 0
        part_total = 0
        for y, line in enumerate(MATCHES):
            for match in line:
                x1, x2 = match.start(), match.end()
                number_highlighter.pos = y, x1
                number_highlighter.width = x2 - x1
                number_highlighter.is_enabled = True
                neighborhood_box.pos = y - 2, x1 - 2
                neighborhood_box.width = number_highlighter.width + 4
                neighborhood_box.canvas["char"][:] = " "
                neighborhood_box.add_border()
                neighborhood_box.is_enabled = True

                for u, v in clockwise(y, x1, x2):
                    if is_inbounds(u, v):
                        symbol_highlighter.pos = u, v

                        if GRID[u][v] != "." and not GRID[u][v].isdigit():
                            neighborhood_box.is_enabled = False
                            tweens = []
                            part = int(match[1])
                            if GRID[u][v] == "*":
                                if (u, v) in gears:
                                    part_b, y_b, x1_b, x2_b = gears[u, v]
                                    del gears[u, v]
                                    gear_ratio = part * part_b
                                    gear_total += gear_ratio

                                    # To make pairs easier to see, give them a unique color
                                    color = next(RAINBOW)
                                    grid.colors[y_b, x1_b:x2_b, :3] = color
                                    grid.colors[y, x1:x2, :3] = color

                                    table.canvas[2:-3, 10:18] = table.canvas[
                                        3:-2, 10:18
                                    ]
                                    table.colors[2:-3, 10:18] = table.colors[
                                        3:-2, 10:18
                                    ]
                                    table.canvas[-3, 10:18]["char"] = " "
                                    table.colors[-3, 10:18, :3] = color

                                    number_highlighter.is_enabled = False

                                    # Animate number to table
                                    number_b.set_text(str(gear_ratio).rjust(8))
                                    number_b.colors[..., :3] = color
                                    number_b.pos = number_highlighter.absolute_pos
                                    number_b.is_enabled = True

                                    def on_complete():
                                        table.add_str(
                                            str(gear_ratio).rjust(8), (-3, 10)
                                        )
                                        table.add_str(
                                            str(gear_total).rjust(8), (-1, 10)
                                        )
                                        number_b.is_enabled = False

                                    tweens.append(
                                        number_b.tween(
                                            duration=0.5,
                                            easing="out_bounce",
                                            pos=(17, 10),
                                            on_complete=on_complete,
                                        )
                                    )

                                else:
                                    grid.colors[u, v] = YELLOW_ON_BLUE
                                    gears[u, v] = part, y, x1, x2
                            else:
                                grid.colors[u, v] = GREEN_ON_BLUE

                            part_total += part
                            table.canvas[2:-3, 1:7] = table.canvas[3:-2, 1:7]
                            table.canvas[-3, 1:7]["char"] = " "

                            # Animate number to table
                            number_a.set_text(match[1].rjust(6))
                            number_a.colors[..., :3] = AOC_GREY
                            number_a.pos = number_highlighter.absolute_pos
                            number_a.is_enabled = True
                            tweens.append(
                                number_a.tween(
                                    duration=0.5,
                                    easing="out_bounce",
                                    pos=(17, 1),
                                )
                            )
                            await asyncio.gather(*tweens)
                            number_a.is_enabled = False

                            table.add_str(match[1].rjust(6), (-3, 1))
                            table.add_str(str(part_total).rjust(6), (-1, 1))
                            break
                        else:
                            await asyncio.sleep(0.05)


if __name__ == "__main__":
    GearApp(
        title="Gear Ratios", background_color_pair=AOC_PRIMARY, color_theme=AOC_THEME
    ).run()
