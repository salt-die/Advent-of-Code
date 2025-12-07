import asyncio

import aoc_lube
from batgrl.app import App
from batgrl.colors import GREEN, rainbow_gradient
from batgrl.gadgets.scroll_view import ScrollView

from .aoc_theme import AocText

RAW = aoc_lube.fetch(year=2025, day=7)
START = RAW.index("S")
SPLITTERS = [
    [x for x, char in enumerate(row) if char == "^"] for row in RAW.splitlines()[1:]
]
GRADIENT = rainbow_gradient(len(SPLITTERS) + 1)


async def draw_beams(row, beams, grid):
    for beam in beams:
        grid.canvas["ord"][row, beam] = ord("╵")
        grid.canvas["fg_color"][row, beam] = GRADIENT[row]
    await asyncio.sleep(0.07)

    for beam in beams:
        grid.canvas["ord"][row, beam] = ord("|")
        grid.canvas["fg_color"][row, beam] = GRADIENT[row]
    await asyncio.sleep(0.07)


class Visual(App):
    async def on_start(self):
        assert self.root  # For type-checker

        grid = AocText()
        grid.set_text(RAW)
        sv = ScrollView(
            size_hint={"height_hint": 1.0, "width_hint": 1.0}, dynamic_bars=True
        )
        sv.view = grid
        self.add_gadget(sv)

        nsplits_label = AocText()
        nsplits_label.set_text("SPLITS: 0")
        self.add_gadget(nsplits_label)

        nsplits = 0
        BEAMS = {START}
        for y, row in enumerate(SPLITTERS):
            # sv.scroll_to_rect(
            #     pos=(y, sv.width // 2), size=(sv.height // 2, sv.width // 2)
            # )
            sv._horizontal_bar.pull_to_front()
            sv._vertical_bar.pull_to_front()
            await draw_beams(y, BEAMS, grid)

            for x in row:
                if x in BEAMS:
                    BEAMS.remove(x)
                    splitter = AocText(pos=(y + 1 + grid.y, x + grid.x))
                    grid.canvas["fg_color"][y + 1, x] = GREEN
                    sv.add_gadget(splitter)

                    splitter.default_fg_color = GREEN
                    splitter.set_text("^")

                    asyncio.create_task(
                        splitter.tween(
                            pos=(-1, -1),
                            easing="out_cubic",
                            on_complete=lambda splitter=splitter: sv.remove_gadget(
                                splitter
                            ),
                        )
                    )
                    BEAMS.update((x - 1, x + 1))
                    nsplits += 1

            nsplits_label.set_text(f"SPLITS: {nsplits}")

        await draw_beams(y + 1, BEAMS, grid)
