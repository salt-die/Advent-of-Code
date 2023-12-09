import asyncio

import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints
from aoc_theme import AOC_CODE_BLOCK, AOC_PRIMARY, AOC_THEME, WHITE
from batgrl.app import App
from batgrl.gadgets.gadget_base import GadgetBase
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.text import Text

DATA = [
    np.fromiter(extract_ints(line), int)
    for line in aoc_lube.fetch(year=2023, day=9).splitlines()
]
INT_LEN = len(str(max(datum.max() for datum in DATA)))
INT_LEN += INT_LEN % 2 == 0
HLEN = INT_LEN // 2 + 1


def predict(data):
    return sum(np.diff(data, n=i)[-1] for i in range(len(data)))


class MirageApp(App):
    async def on_start(self):
        total_label = Text(size=(21, 25), default_color_pair=AOC_PRIMARY)
        total_label.canvas[:, 12]["char"] = "┃"
        total_label.add_str("━━━━━━━━━━━━╋━━━━━━━━━━━━", pos=(-2, 0))
        total_label.add_str("0", pos=(-1, 10))
        total_label.add_str("0", pos=(-1, -2))
        extrap_label = Text(default_color_pair=AOC_PRIMARY, is_enabled=False)
        extrap_backwards_label = Text(default_color_pair=AOC_PRIMARY, is_enabled=False)

        diff_label = Text(
            size=(20, (INT_LEN + 1) * 23), default_color_pair=AOC_CODE_BLOCK
        )
        for i in range(20):
            diff_label.colors[i, : i * HLEN + INT_LEN, :3] = WHITE
            diff_label.colors[i, -i * HLEN - 1 - INT_LEN :, :3] = WHITE

        sv = ScrollView(
            pos=(0, 26), size=(21, 100), show_vertical_bar=False, disable_ptf=True
        )
        sv.view = diff_label

        container = GadgetBase(size=(21, 126), pos_hint={"y_hint": 0.5, "x_hint": 0.5})
        container.add_gadgets(total_label, sv)

        self.add_gadgets(container, extrap_label, extrap_backwards_label)

        extrap_total = 0
        extrap_backwards_total = 0
        for datum in DATA:
            diffs = [datum]
            while diffs[-1].any():
                diffs.append(np.diff(diffs[-1]))

            diff_label.canvas["char"] = " "
            for i, diff in enumerate(diffs):
                row = " ".join(f"{n:>{INT_LEN}}" for n in diff)
                diff_label.add_str(row, (i, i * HLEN + INT_LEN + 1))
                await asyncio.sleep(0.1)

            extrap = 0
            extrap_backwards = 0
            bottom = len(diffs)
            x1 = (22 - bottom) * (INT_LEN + 1) + bottom * HLEN
            x2 = bottom * HLEN
            for i, diff in enumerate(reversed(diffs)):
                extrap += diff[-1]
                x1 += HLEN
                diff_label.add_str(f"{extrap:>{INT_LEN}}", (bottom - i - 1, x1))

                extrap_backwards = diff[0] - extrap_backwards
                x2 -= HLEN
                diff_label.add_str(
                    f"{extrap_backwards:>{INT_LEN}}", (bottom - i - 1, x2)
                )
                await asyncio.sleep(0.1)

            extrap_total += extrap
            extrap_backwards_total += extrap_backwards

            total_label.canvas[:-3] = total_label.canvas[1:-2]
            total_label.add_str("            ┃            ", (-3, 0))

            y, x = diff_label.absolute_pos
            extrap_label.set_text(f"{extrap:>{INT_LEN}}")
            extrap_label.pos = y, x + x1
            extrap_label.is_enabled = True

            extrap_backwards_label.set_text(f"{extrap_backwards:>{INT_LEN}}")
            extrap_backwards_label.pos = y, x + x2
            extrap_backwards_label.is_enabled = True

            y, x = total_label.absolute_pos
            await asyncio.gather(
                extrap_label.tween(
                    duration=0.5,
                    easing="out_quint",
                    pos=(y + 18, 12 - INT_LEN - 1 + x),
                ),
                extrap_backwards_label.tween(
                    duration=0.5,
                    easing="out_quint",
                    pos=(y + 18, 25 - INT_LEN - 1 + x),
                ),
            )
            total_label.add_str(f" {extrap:>10} ┃ {extrap_backwards:>10}", (-3, 0))
            total_label.add_str(
                f" {extrap_total:>10} ┃ {extrap_backwards_total:>10}", (-1, 0)
            )


if __name__ == "__main__":
    MirageApp(
        title="Mirage Maintenance",
        background_color_pair=AOC_PRIMARY,
        color_theme=AOC_THEME,
    ).run()
