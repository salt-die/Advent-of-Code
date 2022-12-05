import asyncio
from itertools import cycle
from pathlib import Path

from nurses_2.app import App
from nurses_2.colors import ABLACK
from nurses_2.widgets.graphic_widget import GraphicWidget, Sprite
from nurses_2.widgets.scroll_view import ScrollView
from nurses_2.widgets.text_widget import TextWidget

import aoc_lube
from aoc_lube.utils import extract_ints, chunk

def parse_raw():
    stacks, commands = aoc_lube.fetch(year=2022, day=5).split("\n\n")

    stacks = stacks.splitlines()
    stacks = [
        [stacks[y][x] for y in range(7, -1, -1) if stacks[y][x] != " "]
        for x in range(1, 35, 4)
    ]

    return stacks, tuple(chunk(extract_ints(commands), 3))

STACKS, COMMANDS = parse_raw()
ASSETS = Path(__file__).parent.parent / "assets"
TILES_PATH = ASSETS / "boxes.png"
WH, WW = 13, 10  # World size
TH, TW = 18, 18  # Tile size
TILE_SHEET = Sprite.from_image(TILES_PATH)
BOXES = cycle((
    Sprite(TILE_SHEET.texture[:TH, :TW]),
    Sprite(TILE_SHEET.texture[:TH, TW:2 * TW]),
    Sprite(TILE_SHEET.texture[:TH, 4 * TW:5 * TW]),
    Sprite(TILE_SHEET.texture[TH:2 * TH, :TW]),
    Sprite(TILE_SHEET.texture[TH:2 * TH, TW:2 * TW]),
    Sprite(TILE_SHEET.texture[TH:2 * TH, 4 * TW:5 * TW]),
    Sprite(TILE_SHEET.texture[3 * TH:4 * TH, :TW]),
    Sprite(TILE_SHEET.texture[4 * TH:5 * TH, :TW]),
    Sprite(TILE_SHEET.texture[4 * TH:5 * TH, TW:2 * TW]),
    Sprite(TILE_SHEET.texture[4 * TH:5 * TH, 2 * TW:3 * TW]),
))


class Boxes(GraphicWidget):
    def __init__(self):
        super().__init__(
            size=((WH + WW // 2 + 1) * TH // 4, (WW + 1) * TW // 2),
            default_color=ABLACK,
        )
        letter_to_sprite = {}
        for stack in STACKS:
            for i, letter in enumerate(stack):
                if letter not in letter_to_sprite:
                    letter_to_sprite[letter] = next(BOXES)
                stack[i] = (letter, letter_to_sprite[letter])
        self._popped = None

    def iso_tile_to_uv(self, y, x):
        oy = self.height * 2 - TH
        return oy - (y + 1) * TH // 2 - x * TH // 4, (x + 1) * TW // 2

    def paint_boxes(self):
        self.texture[:] = self.default_color
        for x, stack in enumerate(reversed(STACKS)):
            for y, (_, sprite) in enumerate(stack):
                sprite.paint(self.texture, self.iso_tile_to_uv(y, WW - x - 2))

            if self._popped and self._popped._x == WW - x - 2:
                self._popped.paint(self.texture, (self._popped._u, self._popped._v))


class SupplyStacksApp(App):
    async def on_start(self):
        text_stack = TextWidget(size=(30, 27), pos_hint=(1.0, 1.0), anchor="bottom_right")
        sv = ScrollView(size_hint=(1.0, 1.0), show_vertical_bar=False, show_horizontal_bar=False, disable_ptf=True)
        sv.view = boxes = Boxes()
        self.add_widgets(sv, text_stack)

        def update_text():
            text_stack.canvas[:] = " "
            for i, stack in enumerate(STACKS):
                for j, (letter, _) in enumerate(stack):
                    text_stack.add_text(f"[{letter}]", row=j, column=i * 3)
            text_stack.canvas = text_stack.canvas[::-1]

        boxes.paint_boxes()
        update_text()
        for a, b, c in COMMANDS:
            for _ in range(a):
                _, boxes._popped = letter, sprite = STACKS[b - 1].pop()

                sprite._x = x = b - 1
                sprite._u, sprite._v = boxes.iso_tile_to_uv(len(STACKS[b - 1]), x)
                while sprite._u > -TH:
                    sprite._u -= 1
                    boxes.paint_boxes()
                    await asyncio.sleep(0)

                sprite._x = x = c - 1
                target_u, sprite._v = boxes.iso_tile_to_uv(len(STACKS[c - 1]), x)
                while sprite._u < target_u:
                    sprite._u += 1
                    boxes.paint_boxes()
                    await asyncio.sleep(0)

                STACKS[c - 1].append((letter, sprite))
                update_text()
                boxes.paint_boxes()


SupplyStacksApp(title="--- Day 5: Supply Stacks ---").run()
