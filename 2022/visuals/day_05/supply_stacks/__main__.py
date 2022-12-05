import asyncio
from collections import defaultdict
from itertools import cycle
from pathlib import Path

from nurses_2.app import App
from nurses_2.colors import ABLACK
from nurses_2.widgets.graphic_widget import GraphicWidget, Sprite
from nurses_2.widgets.scroll_view import ScrollView
from nurses_2.widgets.text_widget import TextWidget

import aoc_lube
from aoc_lube.utils import extract_ints, chunk

ASSETS = Path(__file__).parent.parent / "assets"
TILES_PATH = ASSETS / "boxes.png"
WH, WW = 13, 10  # World size
TH, TW = 18, 18  # Tile size
NSTACKS = 9
TILE_SHEET = Sprite.from_image(TILES_PATH).texture
BOXES = cycle((
    Sprite(TILE_SHEET[:TH, :TW]),
    Sprite(TILE_SHEET[:TH, TW:2 * TW]),
    Sprite(TILE_SHEET[:TH, 4 * TW:5 * TW]),
    Sprite(TILE_SHEET[TH:2 * TH, :TW]),
    Sprite(TILE_SHEET[TH:2 * TH, TW:2 * TW]),
    Sprite(TILE_SHEET[TH:2 * TH, 4 * TW:5 * TW]),
    Sprite(TILE_SHEET[3 * TH:4 * TH, :TW]),
    Sprite(TILE_SHEET[4 * TH:5 * TH, :TW]),
    Sprite(TILE_SHEET[4 * TH:5 * TH, TW:2 * TW]),
    Sprite(TILE_SHEET[4 * TH:5 * TH, 2 * TW:3 * TW]),
))

def parse_raw():
    stacks, commands = aoc_lube.fetch(year=2022, day=5).split("\n\n")
    stacks = stacks.splitlines()
    to_sprite = defaultdict(BOXES.__next__)
    stacks = [
        [(l, to_sprite[l]) for y in range(7, -1, -1) if (l := stacks[y][x]) != " "]
        for x in range(1, 35, 4)
    ]

    return stacks, tuple(chunk(extract_ints(commands), 3))

STACKS, COMMANDS = parse_raw()


class Boxes(GraphicWidget):
    def __init__(self):
        super().__init__(
            size=((WH + WW // 2 + 1) * TH // 4, WW * TW // 2 + 1),
            default_color=ABLACK,
        )

    def iso_tile_to_uv(self, y, x):
        OY = self.height * 2 - TH - 1  # y-origin
        return OY - y * TH // 2 - x * TH // 4, x * TW // 2 + 1

    def paint_boxes(self, popped, px, u, v):
        # We can probably do better than repainting the entire scene...
        self.texture[:] = self.default_color

        for x, stack in enumerate(reversed(STACKS)):  # These need to be painted in reverse order.
            x = NSTACKS - x - 1
            for y, (_, sprite) in enumerate(stack):
                sprite.paint(self.texture, self.iso_tile_to_uv(y, x))

            if px == x:
                popped.paint(self.texture, (u, v))


class SupplyStacksApp(App):
    async def on_start(self):
        text_stack = TextWidget(size=(30, 27), pos_hint=(1.0, 1.0), anchor="bottom_right")
        sv = ScrollView(
            size_hint=(1.0, 1.0),
            show_vertical_bar=False,
            show_horizontal_bar=False,
            disable_ptf=True,
        )
        sv.view = boxes = Boxes()
        sv.vertical_proportion = .8
        self.add_widgets(sv, text_stack)

        def update_text():
            text_stack.canvas[:] = " "
            for i, stack in enumerate(STACKS):
                for j, (letter, _) in enumerate(stack):
                    text_stack.add_text(f"[{letter}]", row=j, column=i * 3)
            text_stack.canvas = text_stack.canvas[::-1]

        for a, b, c in COMMANDS:
            b -= 1
            c -= 1
            for _ in range(a):
                update_text()

                letter, sprite = STACKS[b].pop()

                # Animate up
                u, v = boxes.iso_tile_to_uv(len(STACKS[b]), b)
                while u > -TH:
                    u -= 1
                    boxes.paint_boxes(sprite, b, u, v)
                    await asyncio.sleep(0)

                # Animate down
                target, v = boxes.iso_tile_to_uv(len(STACKS[c]), c)
                while u < target:
                    u += 1
                    boxes.paint_boxes(sprite, c, u, v)
                    await asyncio.sleep(0)

                STACKS[c].append((letter, sprite))


SupplyStacksApp(title="--- Day 5: Supply Stacks ---").run()
