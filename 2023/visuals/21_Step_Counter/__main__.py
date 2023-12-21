import asyncio

import aoc_lube
from aoc_lube.utils import GRID_NEIGHBORHOODS
from aoc_theme import AOC_GREEN_ON_BLUE, AOC_PRIMARY, AOC_THEME, AocButton
from batgrl.app import App
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.text import Text
from batgrl.gadgets.textbox import Textbox

RAW = aoc_lube.fetch(year=2023, day=21)


def parse_raw():
    grid = RAW.splitlines()
    yield len(grid)

    coords = {}
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char != "#":
                coords[y, x] = 1

            if char == "S":
                yield y, x

    yield coords


H, START, GARDEN = parse_raw()


class StepApp(App):
    async def on_start(self):
        visited = Text(default_color_pair=AOC_GREEN_ON_BLUE, is_transparent=True)

        grid = Text(default_color_pair=AOC_PRIMARY)
        grid.set_text(RAW)
        grid.add_gadget(visited)
        visited.size = grid.size

        sv = ScrollView(
            size_hint={"height_hint": 1.0, "width_hint": 1.0}, disable_ptf=True
        )
        sv.view = grid

        steps_input = Textbox(pos=(1, 8), size=(1, 4), max_chars=3)
        steps_input.text = "64"

        reset_event = asyncio.Event()
        reset_button = AocButton("RESET", reset_event.set, pos=(3, 6))

        info_panel = Text(size=(5, 19), default_color_pair=AOC_PRIMARY)
        info_panel.add_border()
        info_panel.add_str("STEPS:", pos=(1, 1))
        info_panel.add_str("VISITED:", pos=(2, 1))
        info_panel.add_gadgets(reset_button, steps_input)

        self.add_gadgets(sv, info_panel)

        while True:
            steps_input.is_enabled = False
            nodes = [START]
            try:
                steps = int(steps_input.text)
            except ValueError:
                steps = 64

            for i in range(steps):
                visited.canvas["char"] = " "
                info_panel.add_str(str(i + 1).rjust(3), (1, 8))

                new_nodes = set()
                for y, x in nodes:
                    for dy, dx in GRID_NEIGHBORHOODS[4]:
                        v = y + dy
                        u = x + dx
                        if (v % H, u % H) in GARDEN:
                            new_nodes.add((v, u))
                            v %= H
                            u %= H
                            visited.canvas["char"][v, u] = (
                                "S" if (v, u) == START else "."
                            )
                nodes = new_nodes
                info_panel.add_str(str(len(nodes)).rjust(8), pos=(2, 9))

                if reset_event.is_set():
                    reset_event.clear()
                    break

                await asyncio.sleep(0.1)

            else:
                steps_input.is_enabled = True
                await reset_event.wait()
                reset_event.clear()


if __name__ == "__main__":
    StepApp(
        title="Step Counter", background_color_pair=AOC_PRIMARY, color_theme=AOC_THEME
    ).run()
