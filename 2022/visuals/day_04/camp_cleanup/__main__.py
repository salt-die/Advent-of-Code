import asyncio
from pathlib import Path
from time import monotonic

import aoc_lube
import parse

from nurses_2.app import App
from nurses_2.easings import lerp, out_bounce
from nurses_2.colors import ColorPair, BLACK, YELLOW, GREEN, RED, WHITE_ON_BLACK, WHITE
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.widget import Widget
from nurses_2.widgets.video_player import VideoPlayer

RANGES = tuple(parse.findall("{:d}-{:d},{:d}-{:d}", aoc_lube.fetch(year=2022, day=4)))
SKY_PATH = Path(__file__).parent.parent / "assets" / "sky.gif"
RED_ON_BLACK = ColorPair.from_colors(RED, BLACK)
GREEN_ON_BLACK = ColorPair.from_colors(GREEN, BLACK)
YELLOW_ON_BLACK = ColorPair.from_colors(YELLOW, BLACK)
BLACK_ON_WHITE = ColorPair.from_colors(BLACK, WHITE)
DASH = "▬"
DURATION = 1

def ease(old, new, p):
    return round(lerp(old, new, out_bounce(p)))


class RangeApp(App):
    async def on_start(self):
        bg = VideoPlayer(source=SKY_PATH, size_hint=(1.0, 1.0))
        container = Widget(size=(14, 105), pos_hint=(.5, .5), anchor="center")

        ranges = TextWidget(size=(3, 105), pos=(11, 0))
        ranges.colors[0] = RED_ON_BLACK
        ranges.colors[2] = GREEN_ON_BLACK

        inputs = TextWidget(size=(11, 11), pos=(0, 47))
        inputs.add_text("Assignments", underline=True)
        inputs.colors[-1] = 0, 0, 0, 255, 255, 255
        for i in range(9):
            a, b, c, d = RANGES[i]
            inputs.add_text(f"{a:>2}-{b:>2},{c:>2}-{d:>2}", row=-i-2)


        container.add_widgets(inputs, ranges)
        self.add_widgets(bg, container)
        bg.play()

        old_a, old_b = old_c, old_d = 0, 99
        for i, (a, b, c, d) in enumerate(RANGES):
            # Roll assignemnts:
            inputs.canvas[2:] = inputs.canvas[1:-1]
            if i + 9 < len(RANGES):
                top_a, top_b, top_c, top_d = RANGES[i + 9]
                inputs.add_text(f"{top_a:>2}-{top_b:>2},{top_c:>2}-{top_d:>2}", row=1)
            else:
                inputs.canvas[1] = " "

            # Tween ranges:
            end_time = monotonic() + DURATION
            while (current_time := monotonic()) < end_time:
                p = 1 - (end_time - current_time) / DURATION
                _a = ease(old_a, a, p)
                _b = ease(old_b, b, p)
                _c = ease(old_c, c, p)
                _d = ease(old_d, d, p)

                ranges.canvas.T[:] = " ", DASH, " "
                ranges.colors[1] = WHITE_ON_BLACK

                ranges.canvas[0, _a + 2: _b + 3] = DASH
                ranges.add_text(f"{_a:>2}", column=_a - 1)
                ranges.add_text(f"{_b:<2}", column=_b + 4)

                ranges.canvas[2, _c + 2: _d + 3] = DASH
                ranges.add_text(f"{_c:>2}", row=2, column=_c - 1)
                ranges.add_text(f"{_d:<2}", row=2, column=_d + 4)

                if _a <= _d and _c <= _b:
                    start, end = max(_a, _c), min(_b, _d)
                    ranges.colors[1, start - 1: end + 6] = YELLOW_ON_BLACK
                    ranges.add_text(f"{start:>2} ", row=1, column=start - 1)
                    ranges.add_text(f"{end:>3}", row=1, column=end + 3)

                await asyncio.sleep(0)

            old_a, old_b, old_c, old_d = a, b, c, d
            await asyncio.sleep(1)


RangeApp(title="--- Day 4: Camp Cleanup ---").run()
