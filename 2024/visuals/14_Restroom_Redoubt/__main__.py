import asyncio

import aoc_lube
import numpy as np
from aoc_lube.utils import Vec2, extract_ints
from aoc_theme import AOC_THEME, AocButton, AocText, AocToggle
from batgrl.app import App
from batgrl.colors import rainbow_gradient
from batgrl.gadgets.grid_layout import GridLayout
from batgrl.gadgets.progress_bar import ProgressBar
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.slider import Slider
from batgrl.text_tools import new_cell

DATA = np.fromiter(extract_ints(aoc_lube.fetch(year=2024, day=14)), int).reshape(-1, 2)
POS = DATA[::2, ::-1]
VEL = DATA[1::2, ::-1]
DIM = Vec2(103, 101)
COLORS = rainbow_gradient(len(POS))


class RestroomRedoubtApp(App):
    async def on_start(self):
        play = asyncio.Event()
        reverse = False
        time_scale = 1
        scales = np.geomspace(2, 0.0001, num=21)
        i = 0
        max_iteration = 103 * 101

        def do_reverse(state):
            nonlocal reverse
            reverse = state == "on"

        def update_delay(state):
            nonlocal time_scale
            time_scale = scales[int(state)]
            delay_label.add_str(f"Time Scale: {time_scale:4.4f}")

        second_label = AocText(size=(1, 17))
        delay_label = AocText(size=(1, 18))
        delay_slider = Slider(
            min=0,
            max=20,
            start_value=1,
            size=(1, 21),
            callback=update_delay,
            is_transparent=True,
            alpha=0,
        )
        play_button = AocButton("Play", play.set)
        stop_button = AocButton("Stop", play.clear)
        reverse_button = AocToggle("Reverse", do_reverse)
        progress = ProgressBar(
            size=(1, 10), pos_hint={"x_hint": 1.0, "x_offset": -2, "anchor": "right"}
        )

        grid = GridLayout(grid_columns=6, is_transparent=True, horizontal_spacing=2)
        grid.add_gadgets(
            second_label,
            delay_slider,
            delay_label,
            play_button,
            stop_button,
            reverse_button,
        )
        grid.size = grid.min_grid_size

        header = AocText(size=(1, 1), size_hint={"width_hint": 1.0})
        header.add_gadgets(grid, progress)

        bunny_hq = AocText(size=DIM, default_cell=new_cell(char="."))

        sv = ScrollView(
            size_hint={"height_hint": 1.0, "height_offset": -1, "width_hint": 1.0},
            pos=(1, 0),
            dynamic_bars=True,
        )
        sv.view = bunny_hq

        self.add_gadgets(header, sv)

        while True:
            bunny_hq.clear()
            second_label.add_str(f"Seconds: {i:8.2f}")
            for pos, vel, color in zip(POS, VEL, COLORS):
                new_pos = tuple(np.round((pos + i * vel)).astype(int) % DIM)
                bunny_hq.canvas["char"][new_pos] = "#"
                bunny_hq.canvas["fg_color"][new_pos] = color

            progress.progress = i / (max_iteration - 1)

            if play.is_set():
                await asyncio.sleep(0)
            else:
                await play.wait()

            if reverse:
                i = (i - time_scale) % max_iteration
            else:
                i = (i + time_scale) % max_iteration


RestroomRedoubtApp(title="Restroom Redoubt", color_theme=AOC_THEME).run()
