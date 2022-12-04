import asyncio
from pathlib import Path
from time import monotonic

import aoc_lube
import parse

from nurses_2.app import App
from nurses_2.easings import lerp, out_cubic
from nurses_2.colors import ColorPair, BLACK, YELLOW, GREEN, RED, WHITE_ON_BLACK, WHITE
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.widget import Widget
from nurses_2.widgets.video_player import VideoPlayer

RANGES = tuple(parse.findall("{:d}-{:d},{:d}-{:d}", aoc_lube.fetch(year=2022, day=4)))
SKY_PATH = Path(__file__).parent.parent / "assets" / "sky.gif"
A_COLORPAIR = ColorPair.from_colors(RED, BLACK)
B_COLORPAIR = ColorPair.from_colors(GREEN, BLACK)
AB_COLORPAIR = ColorPair.from_colors(YELLOW, BLACK)
BLACK_ON_WHITE = ColorPair.from_colors(BLACK, WHITE)
DASH = "▬"
DURATION = 1


class RangeApp(App):
    async def on_start(self):
        bg = VideoPlayer(source=SKY_PATH, size_hint=(1.0, 1.0))
        container = Widget(size=(14, 105), pos_hint=(.5, .5), anchor="center")

        ranges = TextWidget(size=(3, 105), pos=(11, 0))
        ranges.colors[0] = A_COLORPAIR
        ranges.colors[2] = B_COLORPAIR

        inputs = TextWidget(size=(11, 11), pos=(0, 47))
        inputs.add_text("Assignments", underline=True)
        inputs.colors[-1] = BLACK_ON_WHITE
        for i in range(9):
            a, b, c, d = RANGES[i]
            inputs.add_text(f"{a:>2}-{b:>2},{c:>2}-{d:>2}", row=-i-2)


        container.add_widgets(inputs, ranges)
        self.add_widgets(bg, container)
        bg.play()

        old_a, old_b = old_c, old_d = 0, 99

        def set_ranges(a, b, c, d):
            ranges.canvas[0] = " "
            ranges.canvas[1] = DASH
            ranges.canvas[2] = " "

            ranges.colors[1] = WHITE_ON_BLACK

            ranges.canvas[0, a + 2: b + 3] = DASH
            ranges.add_text(f"{a:>2}", column=a - 1)
            ranges.add_text(f"{b:<2}", column=b + 4)

            ranges.canvas[2, c + 2: d + 3] = DASH
            ranges.add_text(f"{c:>2}", row=2, column=c - 1)
            ranges.add_text(f"{d:<2}", row=2, column=d + 4)

            if a <= d and c <= b:
                start, end = max(a, c), min(b, d)
                ranges.colors[1, start - 1: end + 6] = AB_COLORPAIR
                ranges.add_text(f"{start:>2} ", row=1, column=start - 1)
                ranges.add_text(f"{end:>3}", row=1, column=end + 3)

        async def tween_range(a, b, c, d):
            nonlocal old_a, old_b, old_c, old_d
            end_time = monotonic() + DURATION

            while (current_time := monotonic()) < end_time:
                p = 1 - (end_time - current_time) / DURATION

                set_ranges(*(
                    round(lerp(old, new, out_cubic(p)))
                    for old, new in ((old_a, a), (old_b, b), (old_c, c), (old_d, d))
                ))

                await asyncio.sleep(0)

            set_ranges(a, b, c, d)
            old_a, old_b, old_c, old_d = a, b, c, d

        for i, (a, b, c, d) in enumerate(RANGES):
            inputs.canvas[2:] = inputs.canvas[1:-1]

            if i + 9 < len(RANGES):
                top_a, top_b, top_c, top_d = RANGES[i + 9]
                inputs.add_text(f"{top_a:>2}-{top_b:>2},{top_c:>2}-{top_d:>2}", row=1)
            else:
                inputs.canvas[1] = " "

            await tween_range(a, b, c, d)
            await asyncio.sleep(1)


RangeApp(title="--- Day 4: Camp Cleanup ---").run()
