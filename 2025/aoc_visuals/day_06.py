import asyncio
import time

import aoc_lube
from batgrl.app import App
from batgrl.colors import GREEN, lerp_colors

from .aoc_theme import AocText

RAW = aoc_lube.fetch(year=2025, day=6)
MAX_WIDTH = 25


async def flash_ops(sum_text, where_ops, text, x):
    T = 0.5
    default_fg = text.default_fg_color
    default_bg = text.default_bg_color
    sum_text.canvas["fg_color"][3][where_ops] = default_bg
    start = time.perf_counter()
    while True:
        elapsed = time.perf_counter() - start
        if elapsed < T / 2:
            sum_text.canvas["fg_color"][3][where_ops] = lerp_colors(
                default_bg, GREEN, 2 * elapsed
            )
            text.canvas["fg_color"][4, x] = lerp_colors(default_fg, GREEN, 2 * elapsed)
        elif elapsed < T:
            sum_text.canvas["fg_color"][3][where_ops] = lerp_colors(
                GREEN, default_fg, 2 * (elapsed - T / 2)
            )
            text.canvas["fg_color"][4, x] = lerp_colors(
                GREEN, default_bg, 2 * (elapsed - T / 2)
            )
        else:
            sum_text.canvas["fg_color"][3][where_ops] = default_fg
            text.canvas["fg_color"][4, x] = default_bg
            break

        await asyncio.sleep(0)


class Visual(App):
    async def on_start(self):
        assert self.root  # For type-checker

        text = AocText(pos=(0, MAX_WIDTH + 4))
        lines = RAW.splitlines()
        text.width = max(len(line) for line in lines)
        for i, line in enumerate(lines):
            text.add_str(line, pos=(i, 0))
        self.add_gadget(text)

        sum_text = AocText(size=(4, MAX_WIDTH + 2))
        sum_text.chars[:, -1] = "┃"
        total_text = AocText(size=(2, MAX_WIDTH + 2))
        total_text.top = sum_text.bottom
        total_text.add_str("━" * MAX_WIDTH + "━┫")
        total_text.add_str(f"TOTAL: {"0":>{MAX_WIDTH-7}} ┃", pos=(1, 0))

        self.add_gadgets(sum_text, total_text)

        total = 0
        op = "+"
        unused_symbols = []
        current_number: list[AocText] = []
        numbers: list[list[AocText]] = []

        chars = text.chars
        for x in range(text.width):
            if current_number:
                numbers.append(current_number)
                current_number = []

            for y in range(5):
                char = chars[y, x]
                if char in " ":
                    continue
                if char in "*+":
                    op = char
                    continue

                if unused_symbols:
                    symbol = unused_symbols.pop()
                else:
                    symbol = AocText()

                symbol.set_text(char)
                symbol.pos = y, x + text.x
                current_number.append(symbol)

            if (chars[:, x] == " ").all():
                sum_text.shift()
                sum_text.chars[-1, -1] = "┃"

                chars[:4, :x] = " "
                w = (
                    MAX_WIDTH
                    - 3 * (len(numbers) - 1)
                    - sum(len(number) for number in numbers)
                )
                i = 0
                tweens = []
                where_ops = []
                s = ""
                for number in numbers:
                    n = []
                    for digit in number:
                        s += digit.chars[0, 0]
                        self.add_gadget(digit)
                        n.append(
                            digit.tween(
                                pos=(3, i + w), easing="out_cubic", duration=0.3
                            )
                        )
                        i += 1
                    tweens.append(n)
                    where_ops.append(w + i + 1)
                    s += f" {op} "
                    i += 3
                where_ops.pop()
                s = s[:-3]

                for tween in tweens:
                    await asyncio.gather(*tween)

                for number in numbers:
                    for digit in number:
                        self.root.remove_gadget(digit)
                        unused_symbols.append(digit)

                sum_text.add_str(s, pos=(3, w))
                await flash_ops(sum_text, where_ops, text, x - len(numbers))

                numbers.clear()
                total += eval(s)
                total_text.add_str(f"TOTAL: {total:>{MAX_WIDTH-7}}", pos=(1, 0))

                await text.tween(easing="out_bounce", duration=0.5, x=MAX_WIDTH + 2 - x)
