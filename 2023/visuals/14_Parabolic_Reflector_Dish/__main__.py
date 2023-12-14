import asyncio
from typing import Literal

import aoc_lube
import numpy as np
from aoc_theme import AOC_PRIMARY, AocButton, AocToggle
from batgrl.app import App
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.text import Text

EMPTY = "."
ROCK = "O"
WALL = "#"

GRID = np.array([list(line) for line in aoc_lube.fetch(2023, 14).splitlines()])
H, W = 20, 100
DIR_NAMES = {"n": "North", "s": "South", "w": "West ", "e": "East "}


class RollingRocks(Text):
    def __init__(self, rocks, **kwargs):
        super().__init__(**kwargs)
        self.rocks = rocks
        self.size = rocks.shape
        self.canvas["char"] = rocks

    async def roll(self, direction: Literal["n", "w", "s", "e"]):
        if direction == "n":
            rocks = self.rocks
            canvas = self.canvas["char"]
        elif direction == "w":
            rocks = self.rocks.T
            canvas = self.canvas["char"].T
        elif direction == "s":
            rocks = self.rocks[::-1]
            canvas = self.canvas["char"][::-1]
        elif direction == "e":
            rocks = self.rocks.T[::-1]
            canvas = self.canvas["char"].T[::-1]

        target = np.argwhere(rocks == ROCK)
        pos = target.astype(float)

        for i, (y, x) in enumerate(target):
            rocks[y, x] = "."
            while 0 < y and rocks[y - 1, x] == ".":
                y -= 1
            rocks[y, x] = "O"
            target[i] = y, x

        velocity = 0
        gravity = -1 / 100
        while (pos != target).any():
            velocity += gravity
            for i, (y, x) in enumerate(pos):
                canvas[int(y), int(x)] = EMPTY

                y += velocity
                pos[i, 0] = max(y, target[i][0])
                canvas[int(pos[i, 0]), int(x)] = ROCK
            await asyncio.sleep(0)


class ReflectorApp(App):
    async def on_start(self):
        direction_label = Text(
            size=(1, 13), pos_hint={"x_hint": 0.5}, default_color_pair=AOC_PRIMARY
        )
        rocks = RollingRocks(GRID[:H, :W], pos=(2, 0), default_color_pair=AOC_PRIMARY)
        container = Gadget(
            size=(H + 2, W),
            pos_hint={"y_hint": 0.5, "x_hint": 0.5},
            background_color_pair=AOC_PRIMARY,
        )
        container.add_gadgets(direction_label, rocks)
        self.add_gadget(container)

        direction = "e"
        button_event = asyncio.Event()

        auto_button = AocToggle("AUTO", lambda _: button_event.set(), pos=(4, 1))

        def dir_callback(dir):
            def callback():
                nonlocal direction
                direction = dir
                button_event.set()
                auto_button.toggle_state = "off"

            return callback

        def reset():
            global GRID
            nonlocal direction
            GRID = np.array(
                [list(line) for line in aoc_lube.fetch(2023, 14).splitlines()]
            )
            rocks.rocks = GRID[:H, :W]
            rocks.canvas["char"] = rocks.rocks
            direction = "e"
            if button_event.is_set():
                button_event.clear()

        north_button = AocButton("^", dir_callback("n"), pos=(0, 4))
        west_button = AocButton("<", dir_callback("w"), pos=(1, 0))
        south_button = AocButton("v", dir_callback("s"), pos=(2, 4))
        east_button = AocButton(">", dir_callback("e"), pos=(1, 8))

        reset_button = AocButton("RESET", reset, pos=(5, 2))

        button_container = Gadget(size=(6, 11), is_transparent=True)
        button_container.add_gadgets(
            north_button,
            west_button,
            south_button,
            east_button,
            auto_button,
            reset_button,
        )
        self.add_gadget(button_container)

        while True:
            while auto_button.toggle_state == "on":
                direction = {"n": "w", "w": "s", "s": "e", "e": "n"}[direction]
                direction_label.add_str(f"Falling {DIR_NAMES[direction]}")
                await rocks.roll(direction)

            direction_label.is_enabled = False

            await button_event.wait()

            direction_label.is_enabled = True

            if auto_button.toggle_state == "off":
                direction_label.add_str(f"Falling {DIR_NAMES[direction]}")
                await rocks.roll(direction)

            button_event.clear()


if __name__ == "__main__":
    ReflectorApp(
        title="Parabolic Reflector Dish", background_color_pair=AOC_PRIMARY
    ).run()
