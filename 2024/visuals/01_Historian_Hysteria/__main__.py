from collections import Counter

import aoc_lube
from aoc_lube.utils import distribute, extract_ints
from aoc_theme import AOC_THEME, AocText, AocToggle
from batgrl.app import App
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.tabs import Tabs

L, R = distribute(extract_ints(aoc_lube.fetch(year=2024, day=1)), 2)
L = list(L)
R = list(R)

LABELS = """\
 Left  ┃ Right ┃ Similarity 
━━━━━━━╋━━━━━━━╋━━━━━━━━━━━━"""
FOOTER = """\
               ╋━━━━━━━━━━━━
         TOTAL ┃            """


class HistorianApp(App):
    async def on_start(self):
        part_1 = Gadget(size=(20, 28))

        labels_1 = AocText()
        labels_1.set_text(LABELS)
        footer_1 = AocText()
        footer_1.set_text(FOOTER)

        data_1 = AocText(size=(1000, 26))
        data_1.canvas["char"][:, [7, 15]] = "┃"

        sv_1 = ScrollView(size=(15, 28), dynamic_bars=True)
        sv_1.view = data_1

        def on_toggle_1(state):
            if state == "off":
                a = L
                b = R
            else:
                a = sorted(L)
                b = sorted(R)

            total = 0

            for i, (j, k) in enumerate(zip(a, b)):
                data_1.add_str(str(j), pos=(i, 1))
                data_1.add_str(str(k), pos=(i, 9))
                similarity = abs(j - k)
                total += similarity
                data_1.add_str(str(similarity).ljust(8), pos=(i, 17))

            footer_1.add_str(str(total).ljust(10), pos=(1, 17))

        on_toggle_1("off")

        toggle_1 = AocToggle(label="Sorted", callback=on_toggle_1)

        sv_1.top = labels_1.bottom
        footer_1.top = sv_1.bottom
        toggle_1.center = sv_1.center
        toggle_1.top = footer_1.bottom
        part_1.add_gadgets(labels_1, sv_1, footer_1, toggle_1)

        part_2 = Gadget(size=(20, 28))

        labels_2 = AocText()
        labels_2.set_text(LABELS)
        footer_2 = AocText()
        footer_2.set_text(FOOTER)

        data_2 = AocText(size=(1000, 26))
        data_2.canvas["char"][:, [7, 15]] = "┃"

        def on_toggle_2(state):
            if state == "off":
                a = L
                b = R
            else:
                a = sorted(L)
                b = sorted(R)

            counts = Counter(R)
            total = 0

            for i, (j, k) in enumerate(zip(a, b)):
                data_2.add_str(str(j), pos=(i, 1))
                data_2.add_str(str(k), pos=(i, 9))
                similarity = j * counts[j]
                total += similarity
                data_2.add_str(str(similarity).ljust(8), pos=(i, 17))

            footer_2.add_str(str(total).ljust(10), pos=(1, 17))

        on_toggle_2("off")

        toggle_2 = AocToggle(label="Sorted", callback=on_toggle_2)

        sv_2 = ScrollView(size=(15, 28), dynamic_bars=True)
        sv_2.view = data_2

        sv_2.top = labels_2.bottom
        footer_2.top = sv_2.bottom
        toggle_2.center = sv_2.center
        toggle_2.top = footer_2.bottom

        part_2.add_gadgets(labels_2, sv_2, footer_2, toggle_2)

        tabs = Tabs(size=(22, 28))
        tabs.add_tab("Part 1", part_1)
        tabs.add_tab("Part 2", part_2)
        tabs.tabs["Part 1"].toggle_state = "on"

        self.add_gadget(tabs)


HistorianApp(
    title="Historian Hysteria", color_theme=AOC_THEME, inline=True, inline_height=22
).run()
