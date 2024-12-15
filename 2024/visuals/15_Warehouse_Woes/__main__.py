import asyncio

import aoc_lube
import numpy as np
from aoc_lube.utils import Vec2
from aoc_theme import AOC_THEME, AocButton, AocText
from batgrl.app import App
from batgrl.colors import Color
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.slider import Slider
from batgrl.gadgets.tabs import Tabs

BROWN = Color.from_hex("44361e")
YELLOW = Color.from_hex("e5da0d")
DIRS = {"<": Vec2(0, -1), "^": Vec2(-1, 0), "v": Vec2(1, 0), ">": Vec2(0, 1)}


def parse_raw():
    map_, instructions = aoc_lube.fetch(year=2024, day=15).split("\n\n")
    grid = map_.splitlines()
    h, w = len(grid), len(grid[0])
    warehouse_1 = np.full((h, w), "#")
    warehouse_2 = np.full((h, 2 * w), "#")
    for y, line in enumerate(map_.splitlines()):
        for x, char in enumerate(line):
            if char == "@" or char == ".":
                if char == "@":
                    start = Vec2(y, x)
                chars = "..."
            elif char == "O":
                chars = "O[]"
            else:
                chars = "###"
            warehouse_1[y, x], warehouse_2[y, 2 * x], warehouse_2[y, 2 * x + 1] = chars

    return start, warehouse_1, warehouse_2, instructions.replace("\n", "")


START, WAREHOUSE_1, WAREHOUSE_2, INSTRUCTIONS = parse_raw()


def can_vertical_push(pos, dir, chars):
    adj_pos = Vec2(0, 1) if chars[pos] == "[" else Vec2(0, -1)
    new_pos = pos + dir
    if chars[new_pos] == "#" or chars[new_pos + adj_pos] == "#":
        return False

    if chars[new_pos] in "[]" and not can_vertical_push(new_pos, dir, chars):
        return False

    if chars[new_pos + adj_pos] in "[]" and not can_vertical_push(
        new_pos + adj_pos, dir, chars
    ):
        return False
    return True


def do_vertical_push(pos, dir, chars):
    adj_pos = Vec2(0, 1) if chars[pos] == "[" else Vec2(0, -1)
    new_pos = pos + dir
    if chars[new_pos] in "[]":
        do_vertical_push(new_pos, dir, chars)

    if chars[new_pos + adj_pos] in "[]":
        do_vertical_push(new_pos + adj_pos, dir, chars)

    chars[new_pos] = chars[pos]
    chars[new_pos + adj_pos] = chars[pos + adj_pos]
    chars[pos] = chars[pos + adj_pos] = "."


class WarehouseWoesApp(App):
    async def on_start(self):
        delays = [0.07, 0.07]
        events = [asyncio.Event(), asyncio.Event()]
        tabs = Tabs(size_hint={"height_hint": 1.0, "width_hint": 1.0})
        self.add_gadget(tabs)

        def recolor_foreground(warehouse):
            warehouse.canvas["fg_color"] = warehouse.default_fg_color
            warehouse.canvas["fg_color"][
                np.isin(warehouse.canvas["char"], ["O", "[", "]"])
            ] = BROWN

        async def do_part_i(warehouse, label, i):
            current_pos = START if i == 0 else Vec2(START.y, 2 * START.x)
            wh = warehouse.canvas["char"]
            for instruction in INSTRUCTIONS:
                label[0, 29:] = label[0, 28:-1]
                label[0, 28] = instruction
                direction = DIRS[instruction]
                wh[current_pos] = "."
                new_pos = current_pos + direction
                if wh[new_pos] == ".":
                    current_pos = new_pos
                elif wh[new_pos] == "#":
                    pass
                elif i == 0:
                    look_ahead = new_pos
                    while wh[look_ahead] == "O":
                        look_ahead += direction
                    if wh[look_ahead] != "#":
                        wh[look_ahead] = "O"
                        wh[new_pos] = "."
                        current_pos = new_pos
                elif direction.x:  # Horizontal push.
                    look_ahead = new_pos
                    while wh[look_ahead] in "[]":
                        look_ahead += direction
                    if wh[look_ahead] != "#":
                        while look_ahead != new_pos:
                            wh[look_ahead] = wh[look_ahead - direction]
                            look_ahead -= direction
                        wh[new_pos] = "."
                        current_pos = new_pos
                elif can_vertical_push(new_pos, direction, wh):
                    do_vertical_push(new_pos, direction, wh)
                    current_pos = new_pos

                recolor_foreground(warehouse)
                wh[current_pos] = "@"
                warehouse.canvas["fg_color"][current_pos] = YELLOW
                await events[i].wait()
                await asyncio.sleep(delays[i])

        tasks = []

        for i in range(2):
            start = AocButton("Start", events[i].set)
            stop = AocButton("Stop", events[i].clear)
            stop.left = start.right
            slider_label = AocText(
                size=(1, 13),
                pos_hint={"x_hint": 1.0, "anchor": "right", "x_offset": -10},
            )

            def create_updater(i, slider_label):
                def update_delay(value):
                    delays[i] = value
                    slider_label.add_str(f" Delay: {value:.2f}")

                return update_delay

            slider = Slider(
                size=(1, 10),
                min=0,
                max=0.3,
                start_value=0.07,
                callback=create_updater(i, slider_label),
                is_transparent=True,
                alpha=0,
                pos_hint={"x_hint": 1.0, "anchor": "right"},
            )
            wh = WAREHOUSE_1 if i == 0 else WAREHOUSE_2
            warehouse = AocText(size=wh.shape)
            warehouse.canvas["char"] = wh
            sv = ScrollView(
                pos=(1, 0),
                size_hint={"height_hint": 1.0, "height_offset": -1, "width_hint": 1.0},
                dynamic_bars=True,
            )
            sv.view = warehouse
            container = AocText(size_hint={"height_hint": 1.0, "width_hint": 1.0})
            container.add_gadgets(start, stop, slider_label, slider, sv)
            tabs.add_tab(f"Part {i + 1}", container)
            container.add_str(
                "Instructions:", truncate_str=True, pos=(0, stop.right + 1)
            )
            container.canvas["fg_color"][0, 28] = 255
            tasks.append(
                asyncio.create_task(do_part_i(warehouse, container.canvas["char"], i))
            )


WarehouseWoesApp(title="Warehouse Woes", color_theme=AOC_THEME).run()
