import asyncio

from aoc_theme import AOC_PRIMARY, AocButton
from batgrl.app import App
from batgrl.colors import Color, ColorPair
from batgrl.gadgets.behaviors.button_behavior import ButtonBehavior
from batgrl.gadgets.text import Text

BROWN = Color.from_hex("2d1503")
YELLOW = Color.from_hex("eac36e")
GREEN = Color.from_hex("25aa37")
BRIGHT_GREEN = Color.from_hex("51ed25")
BLUE = Color.from_hex("1b89c4")
PURPLE = Color.from_hex("8a2ed1")
BROWN_ON_YELLOW = ColorPair.from_colors(BROWN, YELLOW)

CARD_TEMPLATE = (
    "                \n"
    " {rank}              \n"
    "                 \n"
    "                 \n"
    "  a'!   _,,_     \n"
    "    \\\\_/    \\    \n"
    "     \\, /-( /'-, \n"
    "     //\\\\ //\\\\   \n"
    "                 \n"
    "                 \n"
    "               {rank} \n"
)


def score_hand(hand, J="J"):
    return sum(
        sum(
            other.rank in {"J", J} and card.rank in {"J", J} or other.rank == card.rank
            for other in hand
        )
        for card in hand
    )


def score_wild(hand):
    return max((score_hand(hand, rank), rank) for rank in "23456789TQKA")


class Card(ButtonBehavior, Text):
    def __init__(self, rank):
        super().__init__(default_color_pair=BROWN_ON_YELLOW)
        self.rank = rank
        self.set_text(CARD_TEMPLATE.format(rank=rank))
        self.add_border("double")
        self.hover_border = Text(size=self.size, is_transparent=True, is_enabled=False)
        self.hover_border.add_border("thick")
        self.hover_border.colors[..., :3] = GREEN
        self.add_gadget(self.hover_border)

    def update_normal(self):
        self.hover_border.is_enabled = False

    def update_hover(self):
        self.hover_border.is_enabled = True

    def on_release(self):
        ncards = len(self.app.selected_cards)
        if ncards == 10:
            return

        card = Text(pos=self.pos, size=self.size, default_color_pair=BROWN_ON_YELLOW)
        card.rank = self.rank
        card.canvas[:] = self.canvas
        self.app.selected_cards.append(card)
        self.root.add_gadget(card)

        kwargs = {"easing": "out_elastic"}
        if ncards < 5:
            kwargs["pos"] = (18, ncards * 10 + 5)
        else:
            kwargs["pos"] = (18, ncards * 10 + 25)

        if ncards == 9:
            kwargs["on_complete"] = self.app.all_selected.set

        asyncio.create_task(card.tween(**kwargs))


class CardApp(App):
    async def on_start(self):
        for i, rank in enumerate("J23456789TQKA"):
            self.add_gadget(Card(rank))
            self.children[-1].x = 10 * i

        self.selected_cards = []
        self.all_selected = asyncio.Event()

        wins_label = Text(pos=(22, 63), default_color_pair=AOC_PRIMARY)
        ok_event = asyncio.Event()
        ok_button = AocButton("AGAIN", ok_event.set, pos=(25, 65), is_enabled=False)
        self.add_gadgets(wins_label, ok_button)

        while True:
            await self.all_selected.wait()
            a = self.selected_cards[:5]
            b = self.selected_cards[5:]
            a_score, a_jack = score_wild(a)
            b_score, b_jack = score_wild(b)

            tweens = []
            for hand, jack in zip((a, b), (a_jack, b_jack)):
                groups = {}
                for card in hand:
                    if card.rank == "J":
                        card.add_str(f"({jack})", (1, 2))
                        card.add_str(f"({jack})", (-2, -5))
                        groups.setdefault(jack, []).append(card)
                    else:
                        groups.setdefault(card.rank, []).append(card)

                i = 0
                for cards in groups.values():
                    if len(cards) == 1:
                        continue

                    for card in cards:
                        card.add_border(
                            "thick", color_pair=(BLUE if i == 0 else PURPLE) * 2
                        )
                        tweens.append(
                            card.tween(duration=0.5, y=card.y - 3, easing="out_elastic")
                        )
                    i += 1

            await asyncio.gather(*tweens)

            if a_score == b_score:
                for a_card, b_card in zip(a, b):
                    a_value = "J23456789TQKA".index(a_card.rank)
                    b_value = "J23456789TQKA".index(b_card.rank)
                    if a_value > b_value:
                        tie_breaker = a_card
                        winner = 0
                        break

                    if b_value > a_value:
                        tie_breaker = b_card
                        winner = 1
                        break
                else:
                    winner = 2
                    tie_breaker = None

                if tie_breaker is not None:
                    tie_breaker.add_border("thick", color_pair=BRIGHT_GREEN * 2)
                    tie_breaker.add_str("Tie-breaker", pos=(1, 3))
                    await tie_breaker.tween(
                        duration=0.5, y=card.y - 2, easing="out_elastic"
                    )
            else:
                winner = b_score > a_score

            wins_label.is_enabled = True
            wins_label.set_text(
                "\n <- WINNER \n"
                if winner == 0
                else "\n WINNER -> \n"
                if winner == 1
                else "\n <- TIE -> \n"
            )
            wins_label.add_border("mcgugan_wide")

            ok_button.is_enabled = True
            ok_event.clear()
            await ok_event.wait()

            wins_label.is_enabled = False
            ok_button.is_enabled = False
            ok_button.update_normal()

            for card in self.selected_cards:
                card.destroy()
            self.selected_cards.clear()
            self.all_selected.clear()


if __name__ == "__main__":
    CardApp(title="Camel Cards", background_color_pair=AOC_PRIMARY).run()
