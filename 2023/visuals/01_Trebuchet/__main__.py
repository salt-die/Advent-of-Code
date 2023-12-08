import asyncio
import re
from pathlib import Path
from unicodedata import name

import aoc_lube
try:
    from aoc_theme import AOC_BLUE, AOC_SECONDARY
except ImportError:
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from aoc_theme import AOC_BLUE, AOC_SECONDARY
from batgrl.app import App
from batgrl.colors import GREEN, RED, WHITE, lerp_colors
from batgrl.gadgets.animation import Animation
from batgrl.gadgets.text import Text
from batgrl.gadgets.texture_tools import read_texture

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
        # Line text and number
        text = Text(default_color_pair=AOC_SECONDARY, size=(1, MAX_INPUT_LENGTH + 9))

        # Total display and vertical separator
        total_label = Text(size=(2, 14), is_transparent=True)
        total_label.right = text.right
        total_label.add_str("      ┣━━━━━━━")
        total_label.add_str("TOTAL ┃     0 ", pos=(1, 0))

        # Treb animation
        treb = Animation.from_textures(list(get_trebuchet_frames()))
        treb.left = text.right
        treb.play()

        def fix_size_and_pos():
            """On terminal resize, move text, draw vertical separator, and resize treb."""
            H, W = self.root.size
            text.bottom = self.root.bottom - 2
            total_label_text = total_label.canvas[-2:].copy()
            total_label.canvas[-2:]["char"] = " "
            total_label.height = H
            total_label.canvas[-2:] = total_label_text
            total_label.canvas[:-2, -8]["char"] = "┃"
            treb.size = H, W - text.width

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

            text.add_str(f"{line:<{MAX_INPUT_LENGTH}}      {ab} ", pos=(-1, 0))
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
    TrebuchetApp(title="Trebuchet?!", background_color_pair=AOC_SECONDARY).run()
