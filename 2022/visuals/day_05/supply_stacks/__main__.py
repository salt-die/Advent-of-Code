import asyncio
from itertools import cycle
from pathlib import Path

from nurses_2.app import App
from nurses_2.colors import ABLACK
from nurses_2.widgets.graphic_widget import GraphicWidget, read_texture, composite
from nurses_2.widgets.scroll_view import ScrollView
from nurses_2.widgets.text_widget import TextWidget

import aoc_lube
from aoc_lube.utils import extract_ints, chunk

WH, WW = 13, 10  # world size
TH, TW = 18, 18  # tile size
HH, HW = TH // 2, TW // 2  # half tile size
OY, OX = (WH + WW // 2 + 1) * TH // 2 - TH - 1, 1  # origin
NSTACKS = 9

def init_stacks():
    tile_sheet = read_texture(Path(__file__).parent.parent / "assets" / "boxes.png")
    boxes = cycle((
        tile_sheet[:TH, :TW],
        tile_sheet[:TH, TW:2 * TW],
        tile_sheet[:TH, 4 * TW:5 * TW],
        tile_sheet[TH:2 * TH, :TW],
        tile_sheet[TH:2 * TH, TW:2 * TW],
        tile_sheet[TH:2 * TH, 4 * TW:5 * TW],
        tile_sheet[3 * TH:4 * TH, :TW],
        tile_sheet[4 * TH:5 * TH, :TW],
        tile_sheet[4 * TH:5 * TH, TW:2 * TW],
        tile_sheet[4 * TH:5 * TH, 2 * TW:3 * TW],
    ))
    stacks, commands = aoc_lube.fetch(year=2022, day=5).split("\n\n")
    stacks = stacks.splitlines()
    stacks = [
        [(l, next(boxes)) for y in range(7, -1, -1) if (l := stacks[y][x]) != " "]
        for x in range(1, 35, 4)
    ]

    return stacks, tuple(chunk(extract_ints(commands), 3))

STACKS, COMMANDS = init_stacks()


class Boxes(GraphicWidget):
    def __init__(self):
        super().__init__(
            size=((WH + WW // 2 + 1) * HH // 2, WW * HW + OX),
            default_color=ABLACK,
        )
        # Paint all boxes.
        for x, stack in enumerate(reversed(STACKS)):
            for y, (_, texture) in enumerate(stack):
                composite(texture, self.texture, self.iso_tile_to_uv(y, NSTACKS - x - 1), mask_mode=True)

    def iso_tile_to_uv(self, y, x):
        """
        Transform (y, x) tile-coordinate to (u, v) texture-coordinate.
        """
        return OY - y * HH - x * HH // 2, OX + x * HW

    def repaint_column(self, popped, x, u, v):
        self.texture[:, v: v + TW] = self.default_color

        if x != NSTACKS - 1:
            # Paint half column behind
            for y, (_, texture) in enumerate(STACKS[x + 1]):
                composite(texture[:, :HW], self.texture, self.iso_tile_to_uv(y, x + 1), mask_mode=True)

        # Paint column
        for y, (_, texture) in enumerate(STACKS[x]):
            composite(texture, self.texture, self.iso_tile_to_uv(y, x), mask_mode=True)

        composite(popped, self.texture, (u, v), mask_mode=True)

        if x != 0:
            # Paint half column in front
            for y, (_, texture) in enumerate(STACKS[x - 1]):
                au, av = self.iso_tile_to_uv(y, x - 1)
                composite(texture[:, HW:], self.texture, (au, av + HW), mask_mode=True)


class SupplyStacksApp(App):
    async def on_start(self):
        text_stack = TextWidget(
            size=(53, 27),  # Note `53` is max length of a stack during move operations.
            pos_hint=(1.0, 1.0),
            anchor="bottom_right",
        )
        for i, stack in enumerate(STACKS):
            for j, (letter, _) in enumerate(stack):
                text_stack.add_text(f"[{letter}]", row=-j - 1, column=i * 3)

        sv = ScrollView(
            size_hint=(1.0, 1.0),
            show_vertical_bar=False,
            show_horizontal_bar=False,
            disable_ptf=True,
        )
        sv.view = boxes = Boxes()
        sv.vertical_proportion = .8

        self.add_widgets(sv, text_stack)

        for a, b, c in COMMANDS:
            b -= 1
            c -= 1
            b_stack = STACKS[b]
            c_stack = STACKS[c]
            b_len = len(b_stack)
            c_len = len(c_stack)

            for _ in range(a):
                letter, sprite = b_stack.pop()
                b_len -= 1

                # Animate up
                u, v = boxes.iso_tile_to_uv(b_len, b)
                while u > -TH:
                    u -= 1
                    boxes.repaint_column(sprite, b, u, v)
                    await asyncio.sleep(0)

                # Animate down
                target, v = boxes.iso_tile_to_uv(c_len, c)
                while u < target:
                    u += 1
                    boxes.repaint_column(sprite, c, u, v)
                    await asyncio.sleep(0)

                text_stack.add_text("   ", row=-b_len - 1, column=b * 3)
                text_stack.add_text(f"[{letter}]", row=-c_len - 1, column=c * 3)

                STACKS[c].append((letter, sprite))
                c_len += 1


SupplyStacksApp(title="--- Day 5: Supply Stacks ---").run()
