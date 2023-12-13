import asyncio
from pathlib import Path

import aoc_lube
import numpy as np
from aoc_theme import AOC_BLUE, AOC_GREY, AOC_PRIMARY, WHITE
from batgrl.app import App
from batgrl.colors import BLACK, Color, lerp_colors
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.text import Text

MIRRORS = Path(__file__).parent / "mirrors.gif"
DARK_GREY = lerp_colors(AOC_GREY, BLACK, 0.25)
BLUE_TO_WHITE = [lerp_colors(WHITE, AOC_BLUE, (i + 50) / 60) for i in range(10)]
RED = Color.from_hex("dd3330")
GREEN = Color.from_hex("22cc39")


class IncidenceApp(App):
    async def on_start(self):
        total_label = Text(pos=(2, 0), size=(17, 17), default_color_pair=AOC_PRIMARY)
        total_label.canvas[:, 8]["char"] = "┃"
        total_label.add_str("━━━━━━━━╋━━━━━━━━", pos=(-2, 0))
        total_label.add_str("0", pos=(-1, -2))
        total_label.add_str("0", pos=(-1, 6))

        pattern_label = Text(
            pos_hint={"y_hint": 0.5, "x_hint": 0.5}, default_color_pair=AOC_PRIMARY
        )
        pattern_container = Gadget(
            size=(17, 17), pos=(2, 18), background_color_pair=AOC_PRIMARY
        )
        pattern_container.add_gadget(pattern_label)

        anim_text = Text(
            default_color_pair=AOC_PRIMARY, is_enabled=False, is_transparent=True
        )

        info_label = Text(default_color_pair=AOC_PRIMARY)

        container = Gadget(
            size=(19, 35),
            background_color_pair=AOC_PRIMARY,
            pos_hint={"y_hint": 0.5, "x_hint": 0.5},
        )
        container.add_gadgets(total_label, pattern_container, info_label, anim_text)
        self.add_gadget(container)

        def color_pattern(label, transpose, i):
            label.colors[..., :3] = DARK_GREY
            label.colors[..., 3:] = AOC_PRIMARY.bg_color

            if transpose:
                colors = label.colors
                canvas = label.canvas
                stop = label.height
            else:
                colors = label.colors.swapaxes(0, 1)
                canvas = label.canvas.swapaxes(0, 1)
                stop = label.width

            r = 0
            while 0 <= i - r - 1 and i + r < stop:
                top_canvas = canvas[i - r - 1]
                top_colors = colors[i - r - 1]
                bottom_canvas = canvas[i + r]
                bottom_colors = colors[i + r]

                top_colors[..., 3:] = BLUE_TO_WHITE[r]
                top_colors[..., :3][top_canvas == bottom_canvas] = GREEN
                top_colors[..., :3][top_canvas != bottom_canvas] = RED

                bottom_colors[..., 3:] = BLUE_TO_WHITE[r]
                bottom_colors[..., :3][top_canvas == bottom_canvas] = GREEN
                bottom_colors[..., :3][top_canvas != bottom_canvas] = RED
                r += 1

        total_a = 0
        total_b = 0
        for pattern in aoc_lube.fetch(year=2023, day=13).split("\n\n"):
            pattern_label.set_text(pattern)
            pattern_label.apply_hints()

            pattern_arr = np.array([[*line] for line in pattern.splitlines()])
            for info, stop, arr, trans, score in zip(
                ("Column: {0:>2}", "Row: {0:>2}*100"),
                pattern_arr.shape[::-1],
                (pattern_arr.T, pattern_arr),
                (0, 1),
                (1, 100),
            ):
                for i in range(1, stop):
                    color_pattern(pattern_label, trans, i)
                    a = arr[:i][::-1]
                    b = arr[i:]
                    trim = min(len(a), len(b))
                    nneq = (a[:trim] != b[:trim]).sum()
                    info_label.set_text(f"{info.format(i)}  Smudges: {nneq:>3}")

                    if nneq == 0 or nneq == 1:
                        anim_text.set_text(f"{i:>6}")
                        anim_text.pos = 0, 4 if score == 1 else 1
                        anim_text.is_enabled = True

                        if nneq == 0:
                            total_a += i * score
                            total_label.canvas[:-3, :7] = total_label.canvas[1:-2, :7]
                            total_label.canvas[-3, :7]["char"] = " "
                            await anim_text.tween(
                                duration=0.5, easing="out_bounce", pos=(15, 1)
                            )
                            total_label.add_str(f"{total_a:>6}", (-1, 1))
                            total_label.add_str(f"{i * score:>6}", (-3, 1))
                        else:
                            total_b += i * score
                            total_label.canvas[:-3, 10:] = total_label.canvas[1:-2, 10:]
                            total_label.canvas[-3, 10:]["char"] = " "
                            await anim_text.tween(
                                duration=0.5, easing="out_bounce", pos=(15, 10)
                            )
                            total_label.add_str(f"{total_b:>6}", (-1, 10))
                            total_label.add_str(f"{i* score:>6}", (-3, 10))
                        anim_text.is_enabled = False

                    await asyncio.sleep(0.05)


if __name__ == "__main__":
    IncidenceApp(title="Point of Incidence", background_color_pair=AOC_PRIMARY).run()
