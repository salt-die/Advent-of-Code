import asyncio
from pathlib import Path
from time import monotonic

import aoc_lube
import parse

from nurses_2.app import App
from nurses_2.clamp import clamp
from nurses_2.easings import lerp, out_bounce
from nurses_2.colors import ColorPair, BLACK, YELLOW, GREEN, RED
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.widget import Widget
from nurses_2.widgets.video_player import VideoPlayer

RANGES = tuple(parse.findall("{:d}-{:d},{:d}-{:d}", aoc_lube.fetch(year=2022, day=4)))
SKY_PATH = Path(__file__).parent.parent / "assets" / "sky.gif"
RED_ON_BLACK = ColorPair.from_colors(RED, BLACK)
GREEN_ON_BLACK = ColorPair.from_colors(GREEN, BLACK)
YELLOW_ON_BLACK = ColorPair.from_colors(YELLOW, BLACK)
DASH = "▬"
DURATION = 1

def ease(old, new, p):
    return clamp(round(lerp(old, new, out_bounce(p))), 1, 99)


class RangeApp(App):
    async def on_start(self):
        bg = VideoPlayer(source=SKY_PATH, size_hint=(1.0, 1.0))
        container = Widget(size=(15, 105), pos_hint=(.5, .5), anchor="center")

        inputs = TextWidget(size=(11, 11), pos=(0, 47))
        inputs.add_text("Assignments", underline=True)
        inputs.colors[1:-1, :5] = RED_ON_BLACK
        inputs.colors[1:-1, 6:] = GREEN_ON_BLACK
        inputs.colors[-1, :5] = RED_ON_BLACK.reversed()
        inputs.colors[-1, 6:] = GREEN_ON_BLACK.reversed()
        for i in range(9):
            inputs.add_text("{:>2}-{:>2},{:>2}-{:>2}".format(*RANGES[i]), row=-i - 2)

        ranges = TextWidget(size=(3, 105), pos=(12, 0))
        ranges.colors[0] = RED_ON_BLACK
        ranges.colors[1] = YELLOW_ON_BLACK
        ranges.colors[2] = GREEN_ON_BLACK

        container.add_widgets(inputs, ranges)
        self.add_widgets(bg, container)
        bg.play()

        def set_ranges(a, b, c, d):
            """
            Set the endpoints of the ranges.
            """
            ranges.canvas[:] = " "
            # Top range:
            ranges.canvas[0, a + 2: b + 3] = DASH
            ranges.add_text(f"{a:>2}", column=a - 1)
            ranges.add_text(f"{b:<2}", column=b + 4)
            # Bottom range:
            ranges.canvas[2, c + 2: d + 3] = DASH
            ranges.add_text(f"{c:>2}", row=2, column=c - 1)
            ranges.add_text(f"{d:<2}", row=2, column=d + 4)
            # Intersection:
            if a <= d and c <= b:
                start, end = max(a, c), min(b, d)
                ranges.canvas[1, start + 2: end + 3] = DASH
                ranges.add_text(f"{start:>2}", row=1, column=start - 1)
                ranges.add_text(f"{end:<2}", row=1, column=end + 4)

        old_a, old_b = old_c, old_d = 0, 99
        for i, (a, b, c, d) in enumerate(RANGES):
            # Roll assignments:
            inputs.canvas[2:] = inputs.canvas[1:-1]
            if i + 9 < len(RANGES):
                inputs.add_text("{:>2}-{:>2},{:>2}-{:>2}".format(*RANGES[i + 9]), row=1)
            else:
                inputs.canvas[1] = " "

            # Tween ranges:
            end_time = monotonic() + DURATION
            while (current_time := monotonic()) < end_time:
                p = 1 - (end_time - current_time) / DURATION
                set_ranges(
                    ease(old_a, a, p),
                    ease(old_b, b, p),
                    ease(old_c, c, p),
                    ease(old_d, d, p),
                )
                await asyncio.sleep(0)

            set_ranges(a, b, c, d)
            old_a, old_b, old_c, old_d = a, b, c, d
            await asyncio.sleep(1)


RangeApp(title="--- Day 4: Camp Cleanup ---").run()
