import asyncio
import string
from pathlib import Path

import numpy as np

from nurses_2.app import App
from nurses_2.colors import Color, ColorPair, ColorTheme, gradient
from nurses_2.widgets.slider import Slider
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.textbox import Textbox

AOC_GREEN = Color.from_hex("009900")
AOC_BRIGHT_GREEN = Color.from_hex("99ff99")
AOC_BLUE = Color.from_hex("0f0f23")
BRIGHTENED_BLUE = Color.from_hex("222244")
GREEN_ON_BLUE = ColorPair.from_colors(AOC_GREEN, AOC_BLUE)
AOC_THEME = ColorTheme(
    primary_fg=AOC_GREEN,
    primary_bg=BRIGHTENED_BLUE,
    primary_fg_light=AOC_BRIGHT_GREEN,
    primary_bg_light=AOC_BLUE,
    primary_fg_dark=AOC_GREEN,
    primary_bg_dark=AOC_BLUE,
    secondary_fg=AOC_BRIGHT_GREEN,
    secondary_bg=AOC_BLUE,
)
HEIGHT, WIDTH = 6, 40
LENGTH = HEIGHT * WIDTH

def load_font():
    font = (Path(__file__).parent.parent.parent / "letters.txt").read_text()
    font_array = np.array([list(line) for line in font.splitlines()])
    chars = f" {string.digits}!{string.ascii_lowercase}{string.ascii_uppercase}"
    return {char: font_array[:, i * 5: (i + 1) * 5] for i, char in enumerate(chars)}

LETTER_TO_ARRAY = load_font()


class CRTApp(App):
    async def on_start(self):
        crt = TextWidget(size=(HEIGHT, WIDTH), pos=(2, 0))
        crt.colors[..., 3:] = AOC_BLUE  # Background
        crt_fg = crt.colors[..., :3].reshape(-1, 3)  # Foreground
        crt_fg[:] = gradient(AOC_GREEN, AOC_BRIGHT_GREEN, LENGTH)

        buffer = fill_mask = None
        text_char = "#"
        fill_char = " "
        def update_banner(box):
            nonlocal buffer, fill_mask
            text = box.text.ljust(8)
            buffer = np.full((6, len(text) * 5), ".", object)
            for i, letter in enumerate(text):
                buffer[:, i * 5: (i + 1) * 5] = LETTER_TO_ARRAY.get(letter, ".")
            fill_mask = buffer == "."
            buffer[fill_mask] = fill_char
            buffer[~fill_mask] = text_char

        bannerbox = Textbox(
            pos=(0, 13),
            size=(1, 37),
            enter_callback=update_banner,
        )
        bannerbox.text = "ADVENT OF CODE "
        update_banner(bannerbox)

        chunk = 1
        def slider_update(n):
            nonlocal chunk
            chunk = int(n)

        slider = Slider(
            pos=(9, 30),
            size=(1, 10),
            min=1,
            max=10,
            fill_color=AOC_BRIGHT_GREEN,
            callback=slider_update,
            default_color_pair=GREEN_ON_BLUE,
        )

        def update_text(box):
            nonlocal text_char
            buffer[~fill_mask] = text_char = box.text
            box.text = ""

        textbox = Textbox(
            pos=(11, 16),
            size=(1, 2),
            max_chars=1,
            enter_callback=update_text,
        )

        def update_fill(box):
            nonlocal fill_char
            buffer[fill_mask] = fill_char = box.text
            box.text = ""

        fillbox = Textbox(
            pos=(11, 38),
            size=(1, 2),
            max_chars=1,
            enter_callback=update_fill,
        )

        container = TextWidget(
            size=(12, 40),
            pos_hint=(.5, .5),
            anchor="center",
            default_color_pair=GREEN_ON_BLUE,
        )
        container.add_text("Banner Text:")
        container.add_text("Pixels updated per iteration:", row=9)
        container.add_text("Text character:", row=11)
        container.add_text("Fill character:", row=11, column=22)
        container.add_widgets(bannerbox, crt, slider, textbox, fillbox)

        self.add_widget(container)

        while True:
            i = 0
            while i < LENGTH:
                y, x = divmod(i, WIDTH)
                canvasview = crt.canvas[y, x: x + chunk]
                clen = len(canvasview)
                canvasview[:] = buffer[y, x: x + clen]
                if clen < chunk and y < HEIGHT - 1:
                    crt.canvas[y + 1, :chunk - clen] = buffer[y + 1, :chunk - clen]
                crt_fg[:] = np.roll(crt_fg, chunk, axis=(0, ))  # Roll colors
                i += chunk
                await asyncio.sleep(0)

            buffer[:] = np.roll(buffer, -1, axis=(1,))
            fill_mask[:] = np.roll(fill_mask, -1, axis=(1,))


CRTApp(
    title="Day 10: Cathode-Ray Tube",
    background_color_pair=GREEN_ON_BLUE,
    color_theme=AOC_THEME,
).run()
