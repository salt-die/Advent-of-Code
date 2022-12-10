import asyncio
from pathlib import Path

import numpy as np

from nurses_2.app import App
from nurses_2.colors import Color, ColorPair, ColorTheme, gradient
from nurses_2.widgets.slider import Slider
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.textbox import Textbox
from nurses_2.widgets.widget import Widget

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
    letters = np.array([list(line) for line in font.splitlines()])
    letters[letters=="."] = " "
    return {chr(i + ord("A")): letters[:, i * 5: (i + 1) * 5] for i in range(26)}

LETTER_TO_ARRAY = load_font()


class CRTApp(App):
    async def on_start(self):
        crt = TextWidget(size=(HEIGHT, WIDTH))
        crt.colors[..., 3:] = AOC_BLUE  # Background
        crt_fg = crt.colors[..., :3].reshape(-1, 3)  # Foreground
        crt_fg[:] = gradient(AOC_GREEN, AOC_BRIGHT_GREEN, LENGTH)

        banner = "ADVENT OF CODE "
        buffer = np.full((6, len(banner) * 5), " ", object)
        for i, letter in enumerate(banner):
            if letter in LETTER_TO_ARRAY:
                buffer[:, i * 5: (i + 1) * 5] = LETTER_TO_ARRAY[letter]
        fill_mask = buffer == " "

        slider_label = TextWidget(
            pos=(7, 0),
            size=(1, 30),
            default_color_pair=GREEN_ON_BLUE
        )
        slider_label.add_text(f"Pixels updated per iteration: ")

        chunk = 1
        def slider_update(n):
            nonlocal chunk
            chunk = int(n)

        slider = Slider(
            pos=(7, 30),
            size=(1, 8),
            min=1,
            max=8,
            fill_color=AOC_BRIGHT_GREEN,
            callback=slider_update,
            default_color_pair=GREEN_ON_BLUE,
        )

        fillbox_label = TextWidget(
            pos=(9, 0),
            size=(1, 16),
            default_color_pair=GREEN_ON_BLUE,
        )
        fillbox_label.add_text("Fill character: ")

        def update_fill(box):
            buffer[fill_mask] = box.text[:1]
            box.text = ""

        fillbox = Textbox(
            pos=(9, 16),
            size=(1, 2),
            max_chars=1,
            enter_callback=update_fill,
        )

        textbox_label = TextWidget(
            pos=(9, 19),
            size=(1, 16),
            default_color_pair=GREEN_ON_BLUE,
        )
        textbox_label.add_text("Text character: ")

        def update_text(box):
            buffer[~fill_mask] = box.text[:1]
            box.text = ""

        textbox = Textbox(
            pos=(9, 35),
            size=(1, 2),
            max_chars=1,
            enter_callback=update_text,
        )

        container = Widget(size=(10, 40), pos_hint=(.5, .5), anchor="center")
        container.add_widgets(
            crt,
            slider_label,
            slider,
            fillbox_label,
            fillbox,
            textbox_label,
            textbox,
        )

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
