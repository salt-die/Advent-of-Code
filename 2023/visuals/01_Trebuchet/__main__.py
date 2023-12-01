import asyncio
import re
from pathlib import Path

import aoc_lube
from batgrl.app import App
from batgrl.colors import GREEN, RED, WHITE, Color, ColorPair, lerp_colors
from batgrl.gadgets.animation import Animation
from batgrl.gadgets.text import Text
from batgrl.gadgets.texture_tools import read_texture

AOC_BLUE = Color.from_hex("0f0f23")
BLUISH = lerp_colors(AOC_BLUE, WHITE, 0.25)
AOC_GREY = Color.from_hex("cccccc")
AOC_PRIMARY = ColorPair.from_colors(AOC_GREY, AOC_BLUE)
AOC_SECONDARY = ColorPair.from_colors(WHITE, AOC_BLUE)
LINES = aoc_lube.fetch(year=2023, day=1).splitlines()


def get_trebuchet_frames():
    treb = read_texture(Path(__file__).parent / "trebuchet.png")
    h, w, _ = treb.shape
    qh = h // 4
    qw = w // 4
    for i in range(14):
        y, x = divmod(i, 4)
        yield treb[y * qh : (y + 1) * qh, x * qw : (x + 1) * qw]


class TrebuchetApp(App):
    async def on_start(self):
        text = Text(
            default_color_pair=AOC_SECONDARY,
            size=(20, max(len(line) for line in LINES) + 8),
        )
        text.add_str("TOTAL", pos=(-1, -14))
        text.canvas["char"][:, -8] = "┃"
        text.add_str("┣━━━━━━━", pos=(-2, -8))
        text.add_str("┃     0 ", pos=(-1, -8))

        treb = Animation.from_textures(
            list(get_trebuchet_frames()), size=(20, 80), pos=(0, 20)
        )
        treb.left = text.right
        treb.play()
        self.add_gadgets(text, treb)

        digits = "zero|one|two|three|four|five|six|seven|eight|nine"
        to_digit = {digit: str(i) for i, digit in enumerate(digits.split("|"))}
        total = 0
        for line in LINES:
            text.canvas[:-3] = text.canvas[1:-2]
            text.colors[:-3] = text.colors[1:-2]
            text.canvas[-3] = text.default_char
            text.colors[-3] = AOC_PRIMARY

            matches = [
                (m.start(1), m.end(1), m.group(1))
                for m in re.finditer(rf"(?=({digits}|\d))", line)
            ]
            a = matches[0][2]
            b = matches[-1][2]
            ab = int(to_digit.get(a, a) + to_digit.get(b, b))
            total += ab
            text.add_str(f"┃    {ab}", (-3, -8))
            text.add_str(str(total).rjust(5), (-1, -6))
            text.add_str(line, pos=(-3, 0))

            # Color matches
            for p in range(21):
                text.colors[-3, :-8, :3] = lerp_colors(AOC_GREY, RED, p / 20)
                for a, b, _ in matches:
                    text.colors[-3, a:b, :3] = lerp_colors(AOC_GREY, GREEN, p / 20)
                await asyncio.sleep(0.03)

            # Color first and last
            for p in range(21):
                text.colors[-3, :-8, :3] = lerp_colors(RED, AOC_BLUE, p / 25)
                for a, b, _ in matches:
                    text.colors[-3, a:b, :3] = lerp_colors(GREEN, AOC_BLUE, p / 25)
                text.colors[-3, matches[0][0] : matches[0][1], :3] = GREEN
                text.colors[-3, matches[-1][0] : matches[-1][1], :3] = GREEN
                await asyncio.sleep(0.03)


if __name__ == "__main__":
    TrebuchetApp(title="Trebuchet?!", background_color_pair=AOC_PRIMARY).run()
