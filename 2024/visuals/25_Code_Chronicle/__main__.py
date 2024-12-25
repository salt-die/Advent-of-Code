import asyncio

import aoc_lube
from aoc_theme import AOC_THEME, AocText
from batgrl.app import App
from batgrl.colors import Color
from batgrl.geometry.easings import out_quad
from batgrl.text_tools import add_text, new_cell

RAW = aoc_lube.fetch(year=2024, day=25).split("\n\n")
LOCKS = [lock for lock in RAW if lock.startswith("#####")]
KEYS = [key for key in RAW if key.startswith(".....")]

GREEN = Color.from_hex("22cc39")
RED = Color.from_hex("dd3330")
CELL = new_cell(char=".")


class CodeChronicleApp(App):
    async def on_start(self):
        delay = 0.05

        locks = AocText(size=(7, len(LOCKS) * 7 - 2), default_cell=CELL)
        for i, lock in enumerate(LOCKS):
            add_text(locks.canvas[:, 7 * i : 7 * i + 7], lock)

        keys = AocText(size=(7, len(KEYS) * 7 - 2), default_cell=CELL)
        for i, key in enumerate(KEYS):
            add_text(keys.canvas[:, 7 * i : 7 * i + 7], key)

        keys.top = locks.bottom + 1

        lock = 0
        key = 0

        def reposition_lock_key():
            locks.x = fitting.x - lock * 7
            keys.x = fitting.x - key * 7

        fitting = AocText(size=(15, 5), pos_hint={"x_hint": 0.5})
        fitting.bind("pos", reposition_lock_key)
        background = AocText(
            size_hint={"height_hint": 1.0, "width_hint": 1.0}, default_cell=CELL
        )
        self.add_gadgets(background, locks, keys, fitting)

        chars = fitting.canvas["char"]
        colors = fitting.canvas["fg_color"]
        while True:
            fitting.is_transparent = False
            lock_c = locks.canvas["char"][:, 7 * lock : 7 * lock + 5]
            keys_c = keys.canvas["char"][:, 7 * key : 7 * key + 5]
            keys_fg = keys.canvas["fg_color"][:, 7 * key : 7 * key + 5]
            keys_fg[keys_c == "#"] = GREEN

            dy = 1
            y = 0
            while dy != -1 or y != -1:
                chars[:] = "."
                colors[:] = fitting.default_fg_color
                chars[:7] = lock_c
                where_key = keys_c == "#"
                chars[8 - y : 8 - y + 7][where_key] = "#"
                colors[8 - y : 8 - y + 7][where_key] = GREEN

                if dy > 0 and y > 1:
                    overlap = (lock_c[-y + 1 :] == keys_c[: y - 1]) & (
                        lock_c[-y + 1 :] == "#"
                    )
                    colors[:7][-y + 1 :][overlap] = RED
                    if overlap.any():
                        dy = -1
                elif dy < 0:
                    colors[8 - y : 8 - y + 7][where_key & (lock_c == "#")] = RED

                if y == 8:
                    dy = -1
                y += dy

                await asyncio.sleep(2 * delay * out_quad(y / 8))

            if key < len(KEYS) - 1:
                key += 1
            elif lock < len(LOCKS) - 1:
                lock += 1
                key = 0
            else:
                break

            keys_fg[:] = colors[8:]
            fitting.clear()
            fitting.is_transparent = True

            key_move = keys.tween(
                x=fitting.x - key * 7, duration=delay * 10, easing="out_back"
            )
            lock_move = locks.tween(
                x=fitting.x - lock * 7, duration=delay * 10, easing="out_back"
            )
            await asyncio.gather(key_move, lock_move)
            delay *= 0.99


CodeChronicleApp(
    title="Code Chronicle", color_theme=AOC_THEME, inline=True, inline_height=15
).run()
