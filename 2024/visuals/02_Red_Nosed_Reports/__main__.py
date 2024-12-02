import asyncio

import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints, sliding_window
from aoc_theme import AOC_THEME, AocText, AocToggle
from batgrl.app import App
from batgrl.colors import WHITE, Color

DATA = [
    list(extract_ints(line)) for line in aoc_lube.fetch(year=2024, day=2).splitlines()
]
GREEN = Color.from_hex("22cc39")
RED = Color.from_hex("dd3330")
DIM = Color.from_hex("444444")


def sign(n):
    return 1 if n > 0 else -1 if n < 0 else 0


def sign_of_seq(report):
    a, b, c, d = report[:4]
    return sign(sign(b - a) + sign(c - b) + sign(d - c))


class RedNosedReportsApp(App):
    async def on_start(self):
        delay = 0.05
        header = AocText()
        header.set_text(
            " sign ┃             Reports            ┃ Part 1 ┃ Part 2 \n"
            "━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━╋━━━━━━━━"
        )
        reports_label = AocText(size=(10, 57))
        reports_label.canvas["char"][:, [6, 39, 48]] = "┃"
        diff_label = AocText(size=(2, 57))
        total_label = AocText()
        total_label.set_text("     ┗━━━━━━━━╋━━━━━━━━\nTOTAL         ┃        ")
        reports_label.top = header.bottom
        diff_label.top = reports_label.bottom
        total_label.bottom = diff_label.bottom
        total_label.right = diff_label.right

        def toggle_delay(state):
            nonlocal delay
            if state == "on":
                delay = 0.01
            else:
                delay = 0.05

        toggle = AocToggle("TURBO", toggle_delay, is_transparent=True)
        toggle.bottom = total_label.bottom
        self.add_gadgets(header, reports_label, diff_label, total_label, toggle)

        def paint(i, color):
            reports_label.canvas[-1, i * 4 + 8 : i * 4 + 10]["fg_color"] = color

        def unhighlight():
            fg = reports_label.canvas["fg_color"]
            fg[np.all(fg == WHITE, axis=-1)] = reports_label.default_fg_color

        def write_dif(i, dif, ok):
            color = GREEN if ok else RED
            diff_label.add_str(
                f"{'+' if dif > 0 else ''}{dif}", pos=(0, i * 4 + 10), fg_color=color
            )

        part_1_safe = 0
        part_2_safe = 0
        result_1_done = False
        result_2_done = False

        def write_result(part, ok):
            nonlocal part_1_safe, part_2_safe, result_1_done, result_2_done
            if ok and part == 1 and not result_1_done:
                part_1_safe += 1
                result_1_done = True
            elif ok and part == 2 and not result_2_done:
                part_2_safe += 1
                result_2_done = True
            total_label.add_str(f"{part_1_safe:3}   ┃  {part_2_safe:3}", pos=(1, 8))

            if ok:
                color = GREEN
                mark = "✓"
            else:
                color = RED
                mark = "✗"

            if part == 1:
                pos = (-1, -14)
            else:
                pos = (-1, -5)
            reports_label.add_str(mark, pos=pos, fg_color=color)

        for report in DATA:
            result_1_done = False
            result_2_done = False
            reports_label.shift(1)
            reports_label.canvas["char"][-1, [6, 39, 48]] = "┃"
            diff_label.clear()
            reports_label.add_str("  ".join(f"{i:2}" for i in report), pos=(-1, 8))

            sgn = sign_of_seq(report)
            reports_label.add_str(
                "+" if sgn == 1 else "-" if sgn == -1 else "0", pos=(-1, 2)
            )
            if sgn == 0:
                write_result(1, False)
                write_result(2, False)
                await asyncio.sleep(delay)
                continue

            mistakes = 0
            skip = False
            for i, (a, b) in enumerate(sliding_window(report, 2)):
                if skip:
                    skip = False
                    continue

                unhighlight()
                paint(i, WHITE)
                paint(i + 1, WHITE)
                dif = b - a
                if sign(dif) == sgn and abs(dif) < 4:
                    write_dif(i, dif, True)
                    await asyncio.sleep(delay)
                    continue

                write_dif(i, dif, False)
                write_result(1, False)

                mistakes += 1
                if mistakes > 1:
                    paint(i + 1, DIM)
                    break

                if a == b:
                    paint(i, DIM)
                elif (
                    i != 0
                    and sign(b - report[i - 1]) == sgn
                    and abs(b - report[i - 1]) < 4
                ):
                    paint(i, DIM)
                    paint(i - 1, WHITE)
                    write_dif(i, b - report[i - 1], True)
                elif (
                    i != len(report) - 2
                    and sign(report[i + 2] - a) == sgn
                    and abs(report[i + 2] - a) < 4
                ):
                    paint(i + 1, DIM)
                    paint(i + 2, WHITE)
                    write_dif(i + 1, report[i + 2] - a, True)
                    await asyncio.sleep(delay)
                    skip = True
                elif i == 0:
                    paint(i, DIM)
                elif i == len(report) - 2:
                    paint(i + 1, DIM)
                else:
                    paint(i, DIM)
                    paint(i + 1, DIM)
                    mistakes += 1
                    break
                await asyncio.sleep(delay)

            write_result(1, mistakes == 0)
            write_result(2, mistakes < 2)
            await asyncio.sleep(delay * 3)


RedNosedReportsApp(
    title="Red Nosed Reports", color_theme=AOC_THEME, inline_height=14, inline=True
).run()
