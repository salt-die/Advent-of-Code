import asyncio

import aoc_lube
from aoc_lube.utils import chunk, extract_ints, sliding_window
from aoc_theme import AOC_THEME, AocText
from batgrl.app import App
from batgrl.colors import Color, lerp_colors
from batgrl.gadgets.scroll_view import ScrollView

RULES_IN, PAGES_IN = aoc_lube.fetch(year=2024, day=5).split("\n\n")
RULES = list(chunk(extract_ints(RULES_IN), 2))
PAGES = [list(extract_ints(line)) for line in PAGES_IN.splitlines()]
GREEN = Color.from_hex("1be214")
RED = Color.from_hex("dd3330")
HIGHLIGHT_BG = Color.from_hex("1a2a4f")
YELLOW = Color.from_hex("eff263")
HEIGHT = 7
SUM_WIDTH = 9
PAGE_WIDTH = 70
RULE_WIDTH = 7


class PrintQueueApp(App):
    async def on_start(self):
        delay = 0.05
        total = 0

        tweened = AocText(size=(1, 2), is_enabled=False)
        sum_text = AocText(size=(HEIGHT - 2, SUM_WIDTH))
        sum_text.canvas["char"][:, -2] = "┃"
        total_text = AocText(size=(2, SUM_WIDTH))
        total_text.add_str(" ━━━━━━┫")
        total_text.add_str("     0 ┃", pos=(1, 0))

        header = AocText(size=(1, SUM_WIDTH + PAGE_WIDTH + RULE_WIDTH))
        header.add_str("__**Total**__", pos=(0, 1), markdown=True)
        header.add_str("__**Pages**__", pos=(0, SUM_WIDTH), markdown=True)
        header.add_str("__**Rules**__", pos=(0, -RULE_WIDTH), markdown=True)

        rules_text = AocText()
        rules_text.set_text(RULES_IN)

        rules_sv = ScrollView(size=(HEIGHT, RULE_WIDTH), dynamic_bars=True)
        rules_sv.view = rules_text

        page_text = AocText(size=(HEIGHT, PAGE_WIDTH))

        sum_text.top = header.bottom
        total_text.top = sum_text.bottom
        page_text.top = header.bottom
        page_text.left = sum_text.right
        rules_sv.top = header.bottom
        rules_sv.left = page_text.right

        self.add_gadgets(header, sum_text, total_text, rules_sv, page_text, tweened)

        async def highlight_page(i):
            if i == 0:
                k = i * 3
                page_text.canvas["fg_color"][-1, k : k + 5] = RED
                page_text.canvas["bg_color"][-1, k : k + 5] = HIGHLIGHT_BG
            else:
                k = (i - 1) * 3
                for j in range(3):
                    page_text.canvas["bg_color"][-1, k + j] = page_text.default_bg_color
                    page_text.canvas["bg_color"][-1, k + 5 + j] = HIGHLIGHT_BG
                    await asyncio.sleep(delay)
                page_text.canvas["fg_color"][-1, k + j + 1 : k + j + 3] = RED
                page_text.canvas["fg_color"][-1, k + j + 4 : k + j + 6] = RED

        async def search_rule(a, b):
            for i, (c, d) in enumerate(RULES):
                if i > 0:
                    rules_text.canvas["fg_color"][i - 1] = rules_text.default_fg_color
                    rules_text.canvas["bg_color"][i - 1] = rules_text.default_bg_color
                else:
                    rules_text.canvas["fg_color"] = rules_text.default_fg_color
                    rules_text.canvas["bg_color"] = rules_text.default_bg_color
                rules_text.canvas["fg_color"][i] = RED
                rules_text.canvas["bg_color"][i] = HIGHLIGHT_BG
                rules_sv.scroll_to_rect((i, 0))

                if a == c and b == d:
                    rules_text.canvas["fg_color"][i] = GREEN
                    await asyncio.sleep(delay * 3)
                    return True
                await asyncio.sleep(delay / 10)

            return False

        async def add_total(page):
            nonlocal total
            i = len(page) // 2
            total += page[i]

            page_text.canvas["fg_color"][-1, i * 3 : i * 3 + 2] = YELLOW

            sum_text.shift(1)
            sum_text.canvas["char"][-1, 7] = "┃"

            tweened.add_str(str(page[i]), fg_color=YELLOW)
            tweened.pos = HEIGHT, i * 3 + SUM_WIDTH
            tweened.is_enabled = True

            def on_progress(p):
                tweened.canvas["fg_color"] = lerp_colors(
                    YELLOW, sum_text.default_fg_color, p
                )

            await tweened.tween(
                duration=0.5,
                easing="out_bounce",
                pos=(HEIGHT - 2, 4),
                on_progress=on_progress,
            )

            sum_text.add_str(f"{page[i]}", pos=(-1, 4))
            total_text.add_str(f"{total:4}", pos=(-1, 2))

            tweened.is_enabled = False

        for page in PAGES:
            page_text.shift(1)
            page_text.add_str(
                " ".join(str(i) for i in page), truncate_str=True, pos=(-1, 0)
            )
            for i, (a, b) in enumerate(sliding_window(page)):
                await highlight_page(i)
                k = i * 3
                if await search_rule(a, b):
                    page_text.canvas["fg_color"][-1, k : k + 5] = GREEN
                    page_text.canvas["char"][-1, k + 2] = "<"
                    page_text.canvas["fg_color"][-1, k + 3] = GREEN
                else:
                    page_text.canvas["fg_color"][-1] = RED
                    page_text.canvas["char"][-1, k + 2] = ">"
                    break
            else:
                page_text.canvas["fg_color"][-1] = GREEN
                await add_total(page)

            page_text.canvas["bg_color"][-1] = page_text.default_bg_color
            await asyncio.sleep(delay * 3)


PrintQueueApp(
    title="Print Queue", color_theme=AOC_THEME, inline_height=HEIGHT + 1, inline=True
).run()
