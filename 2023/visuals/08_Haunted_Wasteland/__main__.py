import asyncio
import re
from pathlib import Path

import aoc_lube
import numpy as np
from aoc_lube.utils import chunk
from aoc_theme import (
    AOC_BLUE,
    AOC_BRIGHT_GREEN,
    AOC_GREEN_ON_BLUE,
    AOC_GREY,
    AOC_PRIMARY,
    AOC_SECONDARY,
    WHITE,
)
from batgrl.app import App
from batgrl.colors import ColorPair, lerp_colors
from batgrl.gadgets.animation import Animation
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.slider import Slider
from batgrl.gadgets.text import Text, add_text
from batgrl.gadgets.texture_tools import read_texture

DARK_GREY = lerp_colors(AOC_GREY, AOC_BLUE, 0.5)
PATH_COLOR_PAIR = ColorPair.from_colors(DARK_GREY, AOC_BLUE)


def ghost_textures():
    texture = read_texture(Path(__file__).parent / "ghost.png")
    w = texture.shape[1] // 4
    return [texture[:, i * w : (i + 1) * w] for i in range(4)]


def parse_raw():
    instructions, network = aoc_lube.fetch(year=2023, day=8).split("\n\n")
    yield list(instructions)
    yield {a: b for a, *b in chunk(re.findall(r"\w+", network), 3)}


INSTRUCTIONS, NETWORK = parse_raw()
N_INSTR = len(INSTRUCTIONS)
TAPE = """\
┬───┬───┬───┬───┬───┬───┬───┬───┬───
│   │   │   │   │   │   │   │   │
┴───┴───┴───┴───┴───┴───┴───┴───┴───"""
DISPLAY_W = 9
PATH = """\
    {0}
    / \\
  {1} {2}
"""


class HauntedApp(App):
    async def on_start(self):
        instruction_label = Text(pos=(1, 0), default_color_pair=AOC_PRIMARY)
        instruction_label.set_text(TAPE)
        instruction_label.colors[1, 18, :3] = WHITE
        for i in range(DISPLAY_W):
            instruction_label.canvas[1, 2 + i * 4]["char"] = INSTRUCTIONS[i - 4]

        instruction_highlight = Text(
            size=(5, 1),
            pos=(0, 18),
            default_color_pair=AOC_SECONDARY,
            is_transparent=True,
        )
        instruction_highlight.canvas[0, 0]["char"] = "⎵"
        instruction_highlight.canvas[-1, 0]["char"] = "⎴"

        path = Text(size=(15, 36), pos=(5, 0), default_color_pair=PATH_COLOR_PAIR)
        path.colors[0, :, :3] = WHITE

        steps_label = Text(
            pos=(20, 0),
            pos_hint={"x_hint": 0.5},
            default_color_pair=AOC_PRIMARY,
        )

        container = Gadget(
            size=(24, 36), pos_hint={"y_hint": 0.5, "x_hint": 0.5}, is_transparent=True
        )
        container.add_gadgets(
            instruction_label, instruction_highlight, path, steps_label
        )
        delay = 0.1

        delay_label = Text(default_color_pair=AOC_PRIMARY)

        def update_delay(new_delay):
            nonlocal delay
            delay = new_delay
            delay_label.set_text(f"Update delay: {delay:0.2f}")

        update_delay(0.1)

        delay_slider = Slider(
            pos=(1, 0),
            size=(1, 20),
            min=0,
            max=0.5,
            start_value=0.1,
            callback=update_delay,
            default_color_pair=AOC_GREEN_ON_BLUE,
            handle_color_pair=AOC_GREEN_ON_BLUE,
            fill_color=AOC_BRIGHT_GREEN,
        )
        ghost_animation = Animation.from_textures(
            ghost_textures(),
            frame_durations=0.2,
            interpolation="linear",
            size_hint={"height_hint": 1.0, "width_hint": 0.3},
            pos_hint={"x_hint": 1.0, "anchor": "right"},
        )
        ghost_animation.play()

        self.add_gadgets(container, delay_label, delay_slider, ghost_animation)

        steps = 0
        current_node = "AAA"
        while True:
            steps_label.set_text(f"\n Steps \n {steps:>5} \n")
            steps_label.add_border()
            steps_label.apply_hints()

            old = path.canvas[11:, 13:].copy()
            add_text(
                path.canvas[11:, 13:], PATH.format(current_node, *NETWORK[current_node])
            )
            path.canvas[11:, 13:][old["char"] != " "] = old[old["char"] != " "]
            await asyncio.sleep(delay)

            current_instruction = INSTRUCTIONS[steps % N_INSTR]
            dx = -1 if current_instruction == "L" else 1
            for i in range(1, 3):
                path.colors[11 + i, 17 + i * dx : 20 + i * dx, :3] = WHITE
                await asyncio.sleep(delay)

            for _ in range(2):
                path.canvas = np.roll(path.canvas, (-1, -dx), (0, 1))
                path.canvas[-1]["char"] = " "
                path.colors = np.roll(path.colors, (-1, -dx), (0, 1))
                path.colors[-1] = PATH_COLOR_PAIR
                await asyncio.sleep(delay)

            current_node = NETWORK[current_node][current_instruction == "R"]

            instruction_label.colors[1, 18, :3] = AOC_GREY
            for i in range(4):
                instruction_label.canvas = np.roll(instruction_label.canvas, -1, 1)
                if i == 2:
                    instruction_label.canvas[1, -1]["char"] = INSTRUCTIONS[
                        (steps + 5) % N_INSTR
                    ]
                await asyncio.sleep(delay)
            instruction_label.colors[1, 18, :3] = WHITE

            steps += 1


if __name__ == "__main__":
    HauntedApp(title="Haunted Wasteland", background_color_pair=AOC_PRIMARY).run()
