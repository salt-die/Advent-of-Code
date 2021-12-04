from numpy import spacing
from nurses_2.colors import Color, color_pair, WHITE
from nurses_2.widgets.widget import Widget

MARKED = -1
DEFAULT_COLOR_PAIR = color_pair(WHITE, Color.from_hex("#340744"))
SCORE_COLOR = Color.from_hex("#debad6")
ROW_COLOR = Color.from_hex("#e2d114")


class BingoCard(Widget):
    def __init__(self, index, card, **kwargs):
        self.card = card

        y, x = divmod(index, 10)

        super().__init__(
            size=(5, 14),
            pos=(y * 6 + 1, x * 15 + 1),
            default_color_pair=DEFAULT_COLOR_PAIR,
            **kwargs,
        )

        self._is_won = False
        self.card_to_canvas(-1)

    def card_to_canvas(self, n):
        if self._is_won:
            return

        card = self.card
        canvas = self.canvas

        card[card == n] = MARKED

        for i, row in enumerate(card):
            for j, k in enumerate(row):
                column = 3 * j
                if k == MARKED:
                    canvas[i, column: column + 2] = " ", "✗"

                    # Temporary bright full columns or rows.
                    if (card[i] == MARKED).all() or (card[:, j] == MARKED).all():
                        self._is_won = True
                        self.colors[i, column + 1, :3] = ROW_COLOR

                elif not self._is_won:
                    canvas[i, column: column + 2] = tuple(f"{k:>2}")

        if self._is_won:
            self.add_text(f"{'SCORE:':^14}", row=1)
            self.add_text(f"{(card * ~(card == MARKED)).sum() * n:^14}", row=2)

            self.colors[[1, 2], :, :3] = SCORE_COLOR


class BingoFolder(Widget):
    def __init__(self, cards, **kwargs):
        super().__init__(
            size=(61, 151),
            **kwargs,
        )
        canvas = self.canvas

        # Create grid with box characters.
        vs, hs = 6, 15  # vertical spacing, horizontal spacing
        h, v, tl, tm, tr, bl, bm, br, ml, mm, mr = "━┃┏┳┓┗┻┛┣╋┫"

        canvas[::vs] = h
        canvas[:, ::hs] = v
        canvas[vs: -vs: vs, hs: -hs: hs] = mm

        # Top
        canvas[0, hs: -hs: hs] = tm
        # Bottom
        canvas[-1, hs: -hs: hs] = bm
        # Left
        canvas[vs: -vs: vs, 0] = ml
        # Right
        canvas[vs: -vs: vs, -1] = mr

        # Corners
        canvas[0, 0] = tl
        canvas[0, -1] = tr
        canvas[-1, 0] = bl
        canvas[-1, -1] = br

        self.cards = cards
        self.add_widgets(cards)

    def draw(self, n):
        """
        Mark the number n for each bingo card.
        """
        for card in self.cards:
            card.card_to_canvas(n)
