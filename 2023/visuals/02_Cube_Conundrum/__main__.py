import asyncio
import re
from collections import Counter
from math import prod
from pathlib import Path

import aoc_lube
from aoc_lube.utils import sliding_window_cycle
from aoc_theme import AOC_GREY, AOC_PRIMARY, AOC_SECONDARY
from batgrl.app import App
from batgrl.colors import WHITE, Color, lerp_colors
from batgrl.easings import in_out_exp
from batgrl.gadgets.braille_video_player import BrailleVideoPlayer
from batgrl.gadgets.gadget_base import GadgetBase
from batgrl.gadgets.text import Text

VIDEO = Path(__file__).parent / "cubes.gif"
CUBE = "■"
# Colors
RED = Color.from_hex("dd3330")
GREEN = Color.from_hex("22cc39")
BLUE = Color.from_hex("3268d3")


class CubeApp(App):
    async def on_start(self):
        video = BrailleVideoPlayer(
            source=VIDEO,
            size_hint={"height_hint": 1.0, "width_hint": 1.0},
            gray_threshold=4,
            default_color_pair=AOC_PRIMARY,
        )
        video.play()

        async def color_video():
            while True:
                for a, b in sliding_window_cycle([RED, GREEN, BLUE]):
                    for i in range(21):
                        video.colors[..., :3] = lerp_colors(a, b, in_out_exp(i / 20))
                        await asyncio.sleep(0.05)

        asyncio.create_task(color_video())

        container = GadgetBase(
            pos_hint={"y_hint": 0.5, "x_hint": 0.5},
            size=(12, 125),
            is_transparent=True,
        )

        input_line = Text(default_color_pair=AOC_PRIMARY, is_transparent=True)

        game_label = Text(
            size=(12, 70), default_color_pair=AOC_PRIMARY, is_transparent=True
        )
        game_label.add_str("Contained in ", (8, 0))
        game_label.add_str("?", (8, 53))
        game_label.add_str("Minimum containing set:", (9, 0))

        game_id_label = Text(pos=(0, 5), default_color_pair=AOC_SECONDARY)
        min_contained_set = Text(
            size=(1, 45),
            pos=(9, 24),
            default_color_pair=AOC_PRIMARY,
            is_transparent=True,
        )

        total_label = Text(
            size=(12, 60),
            pos=(0, 65),
            default_color_pair=AOC_PRIMARY,
            is_transparent=True,
        )
        total_label.canvas[:, 7]["char"] = "┃"
        total_label.add_str("━━━━━━━╋━━━━━━━", pos=(-2, 0))
        total_label.add_str("0", pos=(-1, 5))
        total_label.add_str("0", pos=(-1, 13))

        container.add_gadgets(
            game_label, total_label, input_line, min_contained_set, game_id_label
        )

        self.add_gadgets(video, container)

        def paint_set(counts, canvas, colors):
            n = 0
            for color, value in counts.items():
                len_ = len(value)
                canvas[n : n + len_]["char"] = CUBE
                colors[n : n + len_, :3] = (
                    BLUE if color == "blue" else GREEN if color == "green" else RED
                )
                n += len_

        # Paint part 1 maximum set
        part_one_max_count = {"red": 12 * CUBE, "green": 13 * CUBE, "blue": 14 * CUBE}
        paint_set(
            part_one_max_count, game_label.canvas[8, 13:], game_label.colors[8, 13:]
        )

        total_1 = total_2 = 0
        for line in aoc_lube.fetch(2023, 2).splitlines():
            # Set input text
            input_line.set_text(line.replace(": ", ":\n  ").replace("; ", "\n  "))
            input_line.colors[:] = input_line.default_color_pair
            # Highlight Game number
            game_id = re.search(r"(\d+)", line)
            input_line.colors[0, game_id.start(1) : game_id.end(1), :3] = WHITE
            game_id_label.set_text(game_id[1])
            # Reset game label and minimum contained set
            game_label.canvas[:7] = game_label.default_char
            min_contained_set.canvas[:] = min_contained_set.default_char

            game = line.split(": ")[1].split("; ")
            max_colors = {"red": "", "green": "", "blue": ""}
            for j, pull in enumerate(game):
                # Highlight current set
                input_line.colors[j + 1, :, :3] = WHITE
                input_line.canvas[j + 1, 0]["char"] = ">"

                colors = dict.fromkeys(max_colors, "")
                for n, color in re.findall(r"(\d+) (\w+)", pull):
                    colors[color] = int(n) * CUBE
                    if int(n) > len(max_colors[color]):
                        max_colors[color] = colors[color]

                paint_set(
                    colors, game_label.canvas[1 + j, 27:], game_label.colors[1 + j, 27:]
                )
                min_contained_set.canvas[:] = min_contained_set.default_char
                paint_set(
                    max_colors, min_contained_set.canvas[0], min_contained_set.colors[0]
                )

                await asyncio.sleep(0.15)

                # Reset previous highlights
                input_line.colors[1:] = input_line.default_color_pair
                input_line.canvas[1:, 0]["char"] = " "

            part_1 = Counter(max_colors) < Counter(part_one_max_count)

            # Highlight part 1 question
            game_label.colors[8, :13, :3] = WHITE
            game_label.colors[8, 53:, :3] = WHITE
            game_label.add_str("TRUE " if part_1 else "FALSE", (8, 55))

            if part_1:  # Add to part 1 total
                total_1 += int(game_id[1])
                total_label.canvas[:-3, :7] = total_label.canvas[1:-2, :7]
                total_label.canvas[-3, :7] = total_label.default_char
                await game_id_label.tween(
                    duration=0.5, pos=(9, 70 - game_id_label.width), easing="out_bounce"
                )
                total_label.add_str(game_id[1].rjust(5), pos=(-3, 1))
                total_label.add_str(str(total_1).rjust(5), pos=(-1, 1))
                game_id_label.pos = 0, 5
            else:
                await asyncio.sleep(0.5)

            # Remove part 1 question highlight
            game_label.canvas[8, 55:] = game_label.default_char
            game_label.colors[8, :13, :3] = AOC_GREY
            game_label.colors[8, 53:, :3] = AOC_GREY

            # Highlight part 2 question
            game_label.colors[9, :24, :3] = WHITE

            # Move part 2 powers
            total_label.canvas[:-3, 9:] = total_label.canvas[1:-2, 9:]
            total_label.colors[:-3, 9:] = total_label.colors[1:-2, 9:]
            total_label.canvas[-3, 9:] = total_label.default_char

            await min_contained_set.tween(
                duration=0.5, pos=(9, 80), easing="out_bounce"
            )
            min_contained_set.canvas[:] = min_contained_set.default_char
            min_contained_set.pos = 9, 24

            # Remove part 2 question highlight
            game_label.colors[9, :24, :3] = AOC_GREY

            # Add to part 2 total
            power = prod(len(v) for v in max_colors.values())
            total_2 += power
            total_label.add_str(str(power).rjust(5), pos=(-3, 9))
            total_label.add_str(str(total_2).rjust(5), pos=(-1, 9))
            paint_set(
                max_colors, total_label.canvas[-3, 15:], total_label.colors[-3, 15:]
            )


if __name__ == "__main__":
    CubeApp(title="Cube Conundrum", background_color_pair=AOC_PRIMARY).run()
