from aoc_lube.utils import ndigits
from aoc_theme import AOC_THEME, AocText
from batgrl.app import App
from batgrl.gadgets.textbox import Textbox


def blink(stones):
    new_stones = []
    for stone in map(int, stones.strip().split()):
        if stone == 0:
            new_stones.append(1)
            continue

        m, r = divmod(ndigits(stone), 2)
        if r == 0:
            a, b = divmod(stone, 10**m)
            new_stones.append(a)
            new_stones.append(b)
            continue

        new_stones.append(stone * 2024)

    return " ".join(str(i) for i in new_stones)


class OnlyInts(Textbox):
    def on_key(self, key_event):
        if len(key_event.key) == 1 and not (
            key_event.key.isdigit() or key_event.key == " "
        ):
            return

        result = super().on_key(key_event)
        self.do_blinks(self.text)
        return result


class PlutonianPebblesApp(App):
    async def on_start(self):
        blinker = AocText(
            size=(6, 1),
            pos=(1, 0),
            size_hint={"width_hint": 1.0, "height_hint": 1.0, "height_offset": -1},
        )

        def do_blinks(stones):
            blinker.clear()
            if not stones.strip():
                return

            for i in range(blinker.height):
                stones = blink(stones)
                blinker.add_str(stones, pos=(i, 0), truncate_str=True)

        textbox = OnlyInts(size=(1, 1), size_hint={"width_hint": 1.0})
        textbox.do_blinks = do_blinks

        self.add_gadgets(textbox, blinker)


PlutonianPebblesApp(
    title="Plutonian Pebbles", color_theme=AOC_THEME, inline=True, inline_height=15
).run()
