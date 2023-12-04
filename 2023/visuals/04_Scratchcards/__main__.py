import asyncio
import re

import aoc_lube
from aoc_theme import AOC_BLUE, AOC_PRIMARY, AocButton
from batgrl.app import App
from batgrl.colors import Color, ColorPair, lerp_colors, rainbow_gradient
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.text import Text, add_text
from batgrl.io import MouseEvent

BROWN = Color.from_hex("2d1503")
YELLOW = Color.from_hex("eac36e")
SILVER = Color.from_hex("827f7f")
BROWN_ON_YELLOW = ColorPair.from_colors(BROWN, YELLOW)
CARD_BORDER = ColorPair.from_colors(BROWN, AOC_BLUE)
RAINBOW = rainbow_gradient(10)


class Scratcher(Text):
    all_scratched_event = asyncio.Event()
    auto_scratch = False

    def on_mouse(self, mouse_event: MouseEvent) -> bool | None:
        if mouse_event.button != "no_button" and self.collides_point(
            mouse_event.position
        ):
            y, x = self.to_local(mouse_event.position)
            self.canvas[y, x]["char"] = " "
            if (self.canvas[:2]["char"] == " ").all() and (
                self.canvas[3:]["char"] == " "
            ).all():
                self.all_scratched_event.set()
            return True

    async def wait_until_scratched(self):
        self.canvas["char"] = "█"

        if not self.auto_scratch:
            self.all_scratched_event.clear()
            await self.all_scratched_event.wait()

        if self.auto_scratch:
            for y in range(self.height):
                for x in range(self.width):
                    self.canvas[y, x]["char"] = " "
                    await asyncio.sleep(0.03)

    def toggle_auto(self):
        self.auto_scratch = not self.auto_scratch
        self.all_scratched_event.set()


class ScratchcardApp(App):
    async def on_start(self):
        card = Text(size=(14, 33), default_color_pair=BROWN_ON_YELLOW)

        table = Text(size=(14, 33), default_color_pair=AOC_PRIMARY)
        table.left = card.right
        table.canvas[:, 19]["char"] = "┃"
        table.add_str("Score:", pos=(-3, 1))
        add_text(table.canvas[-2:, 12:], "━━━━━━━╋━━━━━━━━━━\n TOTAL ┃     0")

        score = Text(default_color_pair=AOC_PRIMARY, is_enabled=False)

        scratcher = Scratcher(
            size=(8, 14),
            pos=(4, 18),
            is_transparent=True,
            default_color_pair=SILVER * 2,
        )

        ok_event = asyncio.Event()
        ok = AocButton(
            label="OK", pos=(12, 40), callback=ok_event.set, is_enabled=False
        )

        def auto_callback():
            scratcher.toggle_auto()
            ok_event.set()

        auto = AocButton(label="AUTO", pos=(12, 34), callback=auto_callback)

        container = Gadget(size=(14, 66), pos_hint={"y_hint": 0.5, "x_hint": 0.5})
        container.add_gadgets(card, scratcher, table, score, ok, auto)
        self.add_gadgets(container)

        score_total = 0
        for line in aoc_lube.fetch(2023, 4).splitlines():
            name, _, rest = line.partition(": ")
            wins, _, draws = rest.partition(" | ")
            lines = [
                wins[:14],
                wins[15:],
                draws[:14],
                draws[15:29],
                draws[30:44],
                draws[45:59],
                draws[60:],
            ]
            card.colors[:] = BROWN_ON_YELLOW
            add_text(
                card.canvas,
                "\n\n"
                f" Powerstar{name.removeprefix("Card")}     December 2023\n"
                " ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f" Winning numbers: {lines[0]} \n"
                f"                  {lines[1]} \n\n"
                f"    Your numbers: {lines[2]} \n"
                f"                  {lines[3]} \n"
                f"                  {lines[4]} \n"
                f"                  {lines[5]} \n"
                f"                  {lines[6]} \n\n",
            )
            card.add_border("mcgugan_wide", color_pair=CARD_BORDER)

            await scratcher.wait_until_scratched()

            wins_numbers = set(wins.split())
            draws_numbers = set(draws.split())
            matches = wins_numbers & draws_numbers
            n_matches = len(matches)
            current_score = 0 if n_matches == 0 else 2 ** (n_matches - 1)

            table.add_str(f"{n_matches} matches!".ljust(12), pos=(-4, 1))

            score_total += current_score
            score.pos = 11, 41
            score.set_text(str(current_score).rjust(3))
            score.is_enabled = True

            match_coords = []
            for match in matches:
                for y, line in enumerate(lines, start=4):
                    if y > 5:
                        y += 1
                    if m := re.search(rf"\b{match}\b", line):
                        x1, x2 = m.span()
                        match_coords.append((y, x1 + 18, x2 + 18))

            for i in range(11):
                for j, (y, x1, x2) in enumerate(match_coords):
                    card.colors[y, x1:x2, :3] = lerp_colors(
                        BROWN, RAINBOW[j // 2], i / 20
                    )

                await asyncio.sleep(0.03)

            table.canvas[0:-3, 23:] = table.canvas[1:-2, 23:]
            table.canvas[-3, 23:]["char"] = " "

            await score.tween(duration=0.5, easing="out_bounce", pos=(11, 56))
            table.add_str(str(current_score).rjust(3), (11, 23))
            table.add_str(str(score_total).rjust(5), (13, 21))
            score.is_enabled = False

            if not scratcher.auto_scratch:
                ok.is_enabled = True
                ok_event.clear()
                await ok_event.wait()
                ok.is_enabled = False
                ok.update_normal()


if __name__ == "__main__":
    ScratchcardApp(title="Scratchcards", background_color_pair=AOC_PRIMARY).run()
