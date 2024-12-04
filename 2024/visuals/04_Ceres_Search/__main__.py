import asyncio

import aoc_lube
from aoc_lube.utils import GRID_NEIGHBORHOODS
from aoc_theme import AOC_THEME, AocText, AocToggle
from batgrl.app import App
from batgrl.colors import Color, gradient
from batgrl.gadgets.behaviors.movable import Movable
from batgrl.gadgets.scroll_view import ScrollView

RAW = aoc_lube.fetch(year=2024, day=4)
MOORE = GRID_NEIGHBORHOODS[8]
GREEN = Color.from_hex("22cc39")
RED = Color.from_hex("fc2f14")
GREY = Color.from_hex("cccccc")
GRADIENT = gradient(GREEN, RED, 4)


def is_xmas(grid, y, x, dy, dx):
    h, w = grid.shape
    for i, char in enumerate("XMAS"):
        j = y + i * dy
        k = x + i * dx
        if not (0 <= j < h and 0 <= k < w and grid[j, k] == char):
            return False
    return True


def update_hint(grid, hint, y, x, dy, dx):
    for i in range(4):
        j = y + i * dy
        k = x + i * dx
        hint["char"][j, k] = grid["char"][j, k]
        grid["fg_color"][j, k] = GRADIENT[i]
        hint["fg_color"][j, k] = GRADIENT[i]


class MovableAocText(Movable, AocText):
    def __init__(self, auto_toggle, **kwargs):
        self.auto_toggle = auto_toggle
        super().__init__(**kwargs)

    def grab(self, mouse_event):
        if self.auto_toggle.toggle_state == "on":
            self.auto_toggle.on_release()
        return super().grab(mouse_event)


class CeresSearchApp(App):
    async def on_start(self):
        found = set()
        found_label = AocText(size_hint={"width_hint": 1.0}, size=(1, 10))
        found_label.add_str("Found: 0", truncate_str=True)

        auto_event = asyncio.Event()

        def set_toggle_event(state):
            if state == "on":
                auto_event.set()
            else:
                auto_event.clear()

        toggle = AocToggle(
            "AUTO", set_toggle_event, pos_hint={"x_hint": 1.0, "anchor": "right"}
        )

        grid = AocText()
        grid.set_text(RAW)
        grid.height += 2
        grid.width += 2
        grid.canvas[1:, 1:] = grid.canvas[:-1, :-1]
        grid.canvas[0]["char"] = " "
        grid.canvas[:, 0]["char"] = " "

        search = MovableAocText(
            auto_toggle=toggle,
            is_transparent=True,
            alpha=0.5,
            size=(6, 6),
            disable_oob=True,
        )
        search.add_border("outer")
        search_hint = AocText(
            pos=(1, 1), size=(4, 4), is_visible=False, is_transparent=True, alpha=0.75
        )
        search.add_gadget(search_hint)

        async def animate_find(y, x, dy, dx):
            h = 4 if dy else 1
            w = 4 if dx else 1
            j = 3 if dy < 0 else 0
            k = 3 if dx < 0 else 0
            xmas = AocText(size=(h, w), is_transparent=True, alpha=0.0)
            self.add_gadget(xmas)
            for i, char in enumerate("XMAS"):
                xmas.canvas["char"][j + i * dy, k + i * dx] = char
                xmas.canvas["fg_color"][j + i * dy, k + i * dx] = GRADIENT[i]
            xmas.pos = y + 1 - j, x - k
            await xmas.tween(duration=0.75, pos=(1, 7), easing="in_out_back")
            found.add((y, x, dy, dx))
            found_label.add_str(f"Found: {len(found)}")
            self.root.remove_gadget(xmas)

        def on_pos():
            search_hint.clear()
            search_hint.is_visible = False
            y, x = search.pos
            grid_canvas = grid.canvas[y + 1 : y + 5, x + 1 : x + 5]
            hint_canvas = search_hint.canvas
            for i in range(4):
                for j in range(4):
                    for dy, dx in MOORE:
                        if is_xmas(grid_canvas["char"], i, j, dy, dx):
                            search_hint.is_visible = True
                            update_hint(grid_canvas, hint_canvas, i, j, dy, dx)
                            if (y + i, x + j, dy, dx) not in found:
                                asyncio.create_task(animate_find(y + i, x + j, dy, dx))

        search.bind("pos", on_pos)

        grid.add_gadget(search)
        sv = ScrollView(
            size_hint={"height_hint": 1.0, "width_hint": 1.0, "height_offset": -1},
            dynamic_bars=True,
            pos=(1, 0),
        )
        sv.view = grid

        self.add_gadgets(found_label, toggle, sv)

        auto_y = 0
        auto_x = 0
        while auto_y < grid.height - 5:
            await auto_event.wait()
            search.pos = auto_y, auto_x
            if (
                not sv.is_grabbed
                and not sv._horizontal_bar.is_grabbed
                and not sv._vertical_bar.is_grabbed
            ):
                sv.scroll_to_rect(search.pos, search.size)
            if auto_x < grid.width - 6:
                auto_x += 1
            else:
                auto_y += 1
                auto_x = 0
            await asyncio.sleep(0.05)


CeresSearchApp(title="Ceres Search", color_theme=AOC_THEME).run()
