import asyncio
import re
from bisect import bisect

import aoc_lube
from aoc_theme import AOC_THEME, AocText, AocToggle
from batgrl.app import App
from batgrl.colors import WHITE, Color, lerp_colors
from batgrl.gadgets.scroll_view import ScrollView

RAW = aoc_lube.fetch(year=2024, day=3)
NEWLINES = [-1, *(i for i, char in enumerate(RAW) if char == "\n")]
COMMAND_RE = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")
GREEN = Color.from_hex("22cc39")
RED = Color.from_hex("dd3330")
BRIGHT_GREEN = lerp_colors(GREEN, WHITE, 0.5)
BRIGHT_RED = lerp_colors(RED, WHITE, 0.5)
DIM = Color.from_hex("444444")


class MullItOverApp(App):
    async def on_start(self):
        enabled = True
        delay = 0.05
        i = 0
        part_1 = 0
        part_2 = 0

        def toggle_turbo(state):
            nonlocal delay
            if state == "on":
                delay = 0.01
            else:
                delay = 0.07

        enabled_label = AocText(size=(1, 49))
        turbo_button = AocToggle("TURBO", toggle_turbo)
        header_label = AocText(size=(2, 49))
        header_label.add_str("         Part 1         ┃         Part 2         ")
        header_label.add_str(
            "━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━", pos=(1, 0)
        )
        results_1_label = AocText(size=(8, 24))
        results_2_label = AocText(size=(8, 25))
        results_2_label.canvas["char"][:, 0] = "┃"
        total_label = AocText(size=(2, 49))
        total_label.set_text(
            "━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "                        ┃                        "
        )
        data_label = AocText()
        data_label.set_text(RAW)
        sv = ScrollView(size=(7, 49), dynamic_bars=True)
        sv.view = data_label

        turbo_button.right = sv.right
        sv.top = enabled_label.bottom
        header_label.top = sv.bottom
        results_1_label.top = header_label.bottom
        results_2_label.top = header_label.bottom
        results_2_label.left = results_1_label.right
        total_label.top = results_1_label.bottom

        self.add_gadgets(
            enabled_label,
            turbo_button,
            sv,
            header_label,
            results_1_label,
            results_2_label,
            total_label,
        )

        def enable():
            nonlocal enabled
            enabled = True
            enabled_label.add_str("   Enabled ")
            enabled_label.canvas["bg_color"][0, :2] = GREEN

        def disable():
            nonlocal enabled
            enabled = False
            enabled_label.add_str("   Disabled")
            enabled_label.canvas["bg_color"][0, :2] = RED

        def add_part_1(a, b):
            nonlocal part_1
            result = a * b
            part_1 += result
            results_1_label.shift(1)
            mul = f" mul({a},{b})".ljust(13)
            results_1_label.add_str(f"{mul} == {result:6}", pos=(-1, 0))
            total_label.add_str(f"{part_1}".rjust(23), pos=(1, 0))

        def add_part_2(a, b):
            nonlocal part_2
            result = a * b
            part_2 += result
            results_2_label.shift(1)
            mul = f"┃ mul({a},{b})".ljust(14)
            results_2_label.add_str(f"{mul} == {result:6}", pos=(-1, 0))
            total_label.add_str(f"{part_2}".rjust(23), pos=(1, 25))

        async def paint_char(i, is_match):
            if i >= len(RAW) or RAW[i] == "\n":
                return

            if is_match:
                color = BRIGHT_GREEN if enabled else BRIGHT_RED
            else:
                color = DIM

            row = bisect(NEWLINES, i) - 1
            column = i - NEWLINES[row] - 1
            data_label.canvas["fg_color"][row, column] = color
            if not sv.is_grabbed and not sv._horizontal_bar.is_grabbed:
                sv.scroll_to_rect((row, column), (1, 23))

            await asyncio.sleep(delay)

        enable()

        for match in COMMAND_RE.finditer(RAW):
            for i in range(i, match.start()):
                await paint_char(i, is_match=False)

            if match[0] == "don't()":
                disable()
            elif match[0] == "do()":
                enable()
            else:
                a, b = map(int, match.groups())
                add_part_1(a, b)
                if enabled:
                    add_part_2(a, b)

            for i in range(match.start(), match.end() + 1):
                await paint_char(i, is_match=True)


MullItOverApp(
    title="Mull It Over", color_theme=AOC_THEME, inline_height=20, inline=True
).run()
