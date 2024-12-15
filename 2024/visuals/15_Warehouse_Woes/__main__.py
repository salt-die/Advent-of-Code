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
        part_1_event = asyncio.Event()
        part_2_event = asyncio.Event()

        start_1 = AocButton("Start", part_1_event.set)
        stop_1 = AocButton("Stop", part_1_event.clear)
        stop_1.left = start_1.right
        warehouse_1 = AocText(size=WAREHOUSE_1.shape)
        warehouse_1.canvas["char"] = WAREHOUSE_1
        sv1 = ScrollView(
            pos=(1, 0),
            size_hint={"height_hint": 1.0, "height_offset": -1, "width_hint": 1.0},
            dynamic_bars=True,
        )
        sv1.view = warehouse_1
        container_1 = AocText(size_hint={"height_hint": 1.0, "width_hint": 1.0})
        container_1.add_gadgets(start_1, stop_1, sv1)

        start_2 = AocButton("Start", part_2_event.set)
        stop_2 = AocButton("Stop", part_2_event.clear)
        stop_2.left = start_2.right
        warehouse_2 = AocText(size=WAREHOUSE_2.shape)
        warehouse_2.canvas["char"] = WAREHOUSE_2
        sv2 = ScrollView(
            pos=(1, 0),
            size_hint={"height_hint": 1.0, "height_offset": -1, "width_hint": 1.0},
            dynamic_bars=True,
        )
        sv2.view = warehouse_2
        container_2 = AocText(size_hint={"height_hint": 1.0, "width_hint": 1.0})
        container_2.add_gadgets(start_2, stop_2, sv2)

        tabs = Tabs(size_hint={"height_hint": 1.0, "width_hint": 1.0})
        tabs.add_tab("Part 1", container_1)
        tabs.add_tab("Part 2", container_2)

        delay = 0.2

        slider_label = AocText(
            size=(1, 11), pos_hint={"x_hint": 1.0, "anchor": "right", "x_offset": -11}
        )

        def update_delay(value):
            nonlocal delay
            delay = value
            slider_label.add_str(f"Delay: {delay:.2f}")

        slider = Slider(
            size=(1, 10),
            min=0,
            max=0.3,
            start_value=0.2,
            callback=update_delay,
            is_transparent=True,
            alpha=0,
            pos_hint={"x_hint": 1.0, "anchor": "right"},
        )

        self.add_gadgets(tabs, slider_label, slider)
        container_1.add_str(
            "Instructions:", truncate_str=True, pos=(0, stop_1.right + 1)
        )
        container_1.canvas["fg_color"][0, 28] = 255
        container_2.add_str(
            "Instructions:", truncate_str=True, pos=(0, stop_2.right + 1)
        )
        container_2.canvas["fg_color"][0, 28] = 255

        def recolor_foreground(warehouse):
            warehouse.canvas["fg_color"] = warehouse.default_fg_color
            warehouse.canvas["fg_color"][
                np.isin(warehouse.canvas["char"], ["O", "[", "]"])
            ] = BROWN

        async def do_part_one():
            current_pos = START
            wh = warehouse_1.canvas["char"]
            for instruction in INSTRUCTIONS:
                container_1.canvas["char"][0, 29:] = container_1.canvas["char"][
                    0, 28:-1
                ]
                container_1.canvas["char"][0, 28] = instruction
                direction = DIRS[instruction]
                warehouse_1.canvas["char"][current_pos] = "."
                new_pos = current_pos + direction
                if wh[new_pos] == ".":
                    current_pos = new_pos
                elif wh[new_pos] == "#":
                    continue

                look_ahead = new_pos
                while wh[look_ahead] == "O":
                    look_ahead += direction
                if wh[look_ahead] == "#":
                    continue
                wh[look_ahead] = "O"
                wh[new_pos] = "."
                current_pos = new_pos

                recolor_foreground(warehouse_1)
                warehouse_1.canvas["char"][current_pos] = "@"
                warehouse_1.canvas["fg_color"][current_pos] = YELLOW
                await part_1_event.wait()
                await asyncio.sleep(delay)

        async def do_part_two():
            current_pos = Vec2(START.y, 2 * START.x)
            wh = warehouse_2.canvas["char"]
            for instruction in INSTRUCTIONS:
                container_2.canvas["char"][0, 29:] = container_2.canvas["char"][
                    0, 28:-1
                ]
                container_2.canvas["char"][0, 28] = instruction
                direction = DIRS[instruction]
                warehouse_2.canvas["char"][current_pos] = "."
                new_pos = current_pos + direction
                if wh[new_pos] == ".":
                    current_pos = new_pos
                elif wh[new_pos] == "#":
                    pass
                elif direction.x:  # Horizontal push.
                    look_ahead = new_pos
                    while wh[look_ahead] in "[]":
                        look_ahead += direction
                    if wh[look_ahead] == "#":
                        continue
                    while look_ahead != new_pos:
                        wh[look_ahead] = wh[look_ahead - direction]
                        look_ahead -= direction
                    wh[new_pos] = "."
                    current_pos = new_pos
                elif can_vertical_push(new_pos, direction, wh):
                    do_vertical_push(new_pos, direction, wh)
                    current_pos = new_pos

                recolor_foreground(warehouse_2)
                warehouse_2.canvas["char"][current_pos] = "@"
                warehouse_2.canvas["fg_color"][current_pos] = YELLOW
                await part_2_event.wait()
                await asyncio.sleep(delay)

        part_1_task = asyncio.create_task(do_part_one())
        part_2_task = asyncio.create_task(do_part_two())


WarehouseWoesApp(title="Warehouse Woes", color_theme=AOC_THEME).run()
