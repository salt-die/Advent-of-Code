import asyncio
import re
from pathlib import Path
from unicodedata import name

import aoc_lube
from batgrl.app import App
from batgrl.colors import GREEN, RED, WHITE, Color, ColorPair, lerp_colors
from batgrl.gadgets.animation import Animation
from batgrl.gadgets.text import Text
from batgrl.gadgets.texture_tools import read_texture

AOC_BLUE = Color.from_hex("0f0f23")
PRIMARY = ColorPair.from_colors(WHITE, AOC_BLUE)
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
        MAX_INPUT_LENGTH = max(len(line) for line in LINES)
        text = Text(default_color_pair=PRIMARY, size=(1, MAX_INPUT_LENGTH + 9))

        total_label = Text(
            default_color_pair=PRIMARY,
            size=(2, text.width),
            pos_hint={"y_hint": 1.0, "anchor": "bottom"},
        )
        total_label.add_str("      ┣━━━━━━━", pos=(-2, -14))
        total_label.add_str("TOTAL ┃     0 ", pos=(-1, -14))

        treb = Animation.from_textures(list(get_trebuchet_frames()))
        treb.left = text.right
        treb.play()

        def fix_size_and_pos():
            H, W = self.root.size
            treb.size = H, W - text.width
            text.bottom = self.root.bottom - 2

        fix_size_and_pos()
        text.subscribe(self.root, "size", fix_size_and_pos)
        self.add_gadgets(text, total_label, treb)

        digits = {
            k: v
            for v in "123456789"
            for k in [v, name(v).removeprefix("DIGIT ").lower()]
        }
        total = 0
        for line in LINES:
            text.height += 1
            text.y -= 1

            matches = [
                (m.start(1), m.end(1), m.group(1))
                for m in re.finditer(rf"(?=({"|".join(digits)}))", line)
            ]
            a = matches[0][2]
            b = matches[-1][2]
            ab = int(digits[a] + digits[b])
            total += ab

            text.add_str(f"{line:<{MAX_INPUT_LENGTH}} ┃    {ab} ", pos=(-1, 0))
            total_label.add_str(str(total).rjust(5), pos=(-1, -6))

            # Color matches
            for p in range(21):
                text.colors[-1, :-8, :3] = lerp_colors(WHITE, RED, p / 20)
                for a, b, _ in matches:
                    text.colors[-1, a:b, :3] = lerp_colors(WHITE, GREEN, p / 20)
                await asyncio.sleep(0.03)

            # Color first and last
            for p in range(21):
                text.colors[-1, :-8, :3] = lerp_colors(RED, AOC_BLUE, p / 25)
                for a, b, _ in matches:
                    text.colors[-1, a:b, :3] = lerp_colors(GREEN, AOC_BLUE, p / 25)
                text.colors[-1, matches[0][0] : matches[0][1], :3] = GREEN
                text.colors[-1, matches[-1][0] : matches[-1][1], :3] = GREEN
                await asyncio.sleep(0.03)


if __name__ == "__main__":
    TrebuchetApp(title="Trebuchet?!", background_color_pair=PRIMARY).run()
