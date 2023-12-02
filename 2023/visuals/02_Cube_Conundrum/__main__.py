import asyncio
import re
from math import prod
from pathlib import Path

import aoc_lube
from aoc_lube.utils import sliding_window_cycle
from batgrl.app import App
from batgrl.colors import Color, ColorPair, lerp_colors
from batgrl.gadgets.braille_video_player import BrailleVideoPlayer
from batgrl.gadgets.text import Text, add_text

VIDEO = Path(__file__).parent / "cubes.gif"
AOC_BLUE = Color.from_hex("0f0f23")
AOC_GREY = Color.from_hex("cccccc")
AOC_PRIMARY = ColorPair.from_colors(AOC_GREY, AOC_BLUE)
RED = Color.from_hex("dd3330")
GREEN = Color.from_hex("22cc39")
BLUE = Color.from_hex("3268d3")
CUBE = "■"
MAX_COLOR = 20
MAX_GAME = 45
TITLE = """\
{name:^70}
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃         Red          ┃        Green         ┃         Blue         ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩"""
SEP = "├──────────────────────┼──────────────────────┼──────────────────────┤"

MAX_COLORS_TITLE = """\
┢━━━━━━━━━━━━━━━━━━━━━━╈━━━━━━━━━━━━━━━━━━━━━━╈━━━━━━━━━━━━━━━━━━━━━━┪
┃       Max Red        ┃      Max Green       ┃       Max Blue       ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩"""
CUBES = "│ {red:^20} │ {green:^20} │ {blue:^20} │"
TOTAL = """\
       │ {power:>5}
━━━━━━━╈━━━━━━━
 TOTAL ┃ {total:>5} """


def parse_raw():
    for line in aoc_lube.fetch(year=2023, day=2).splitlines():
        yield line.split(": ")[1].split("; ")


GAMES = list(parse_raw())


class CubeApp(App):
    async def on_start(self):
        video = BrailleVideoPlayer(
            source=VIDEO,
            size=(24, 40),
            pos=(-2, 95),
            gray_threshold=4,
            default_color_pair=AOC_PRIMARY,
        )
        video.play()

        async def color_video():
            while True:
                for a, b in sliding_window_cycle([RED, GREEN, BLUE]):
                    for i in range(21):
                        video.colors[..., :3] = lerp_colors(a, b, i / 20)
                        await asyncio.sleep(0.05)

        asyncio.create_task(color_video())

        game_label = Text(size=(19, 70), default_color_pair=AOC_PRIMARY)
        game_label.colors[2::2, 1:23, :3] = RED
        game_label.colors[2::2, 24:46, :3] = GREEN
        game_label.colors[2::2, 47:69, :3] = BLUE
        game_label.canvas[1:, -8]["char"] = "┃"
        for i in range(5, 19, 2):
            game_label.add_str(SEP, pos=(i, 0))

        add_text(game_label.canvas[-4:], MAX_COLORS_TITLE)

        total_label = Text(
            default_color_pair=AOC_PRIMARY,
            size=(20, 68),
            pos=(1, 62),
            is_transparent=True,
        )
        add_text(total_label.canvas[-3:], TOTAL.format(total=0, power=""))
        self.add_gadgets(game_label, video, total_label)

        total = 0
        for i, game in enumerate(GAMES, start=1):
            add_text(game_label.canvas, TITLE.format(name=f"Game {i}"))

            max_colors = {"red": "", "blue": "", "green": ""}
            for j in range(4, 16, 2):
                game_label.add_str(CUBES.format(**max_colors), pos=(j, 0))

            for j, pull in enumerate(game):
                colors = dict.fromkeys(max_colors, "")
                for n, color in re.findall(r"(\d+) (\w+)", pull):
                    colors[color] = int(n) * CUBE
                    if int(n) > len(max_colors[color]):
                        max_colors[color] = colors[color]

                game_label.add_str(CUBES.format(**colors), (4 + 2 * j, 0))
                power = prod(len(v) for v in max_colors.values())
                game_label.add_str(CUBES.format(**max_colors), pos=(-1, 0))
                await asyncio.sleep(0.15)

            total_label.canvas[:-3, 9:] = total_label.canvas[1:-2, 9:]
            total_label.colors[:-3, 9:] = total_label.colors[1:-2, 9:]
            total += power
            add_text(total_label.canvas[-3:], TOTAL.format(total=total, power=power))
            n = 15
            for color, value in max_colors.items():
                len_ = len(value)
                total_label.canvas[-3, n : n + len_]["char"] = CUBE
                total_label.colors[-3, n : n + len_, :3] = (
                    BLUE if color == "blue" else GREEN if color == "green" else RED
                )
                n += len_
            total_label.canvas[-3, n:] = total_label.default_char


if __name__ == "__main__":
    CubeApp(title="Cube Conundrum", background_color_pair=AOC_PRIMARY).run()
