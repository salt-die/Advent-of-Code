import numpy as np

from nurses_2.colors import Color, color_pair, WHITE
from nurses_2.widgets.widget import Widget

MARKED = -1
DEFAULT_COLOR_PAIR = color_pair(WHITE, Color.from_hex("#340744"))
SCORE_COLOR = Color.from_hex("#debad6")
ROW_COLOR = Color.from_hex("#e2d114")

ORDINAL_SUFFIX = {
    1: "st",
    2: "nd",
    3: "rd",
}

def ordinal(value: int) -> str:
    """
    Return natural language ordinal of value.
    """
    if value % 100 in (11, 12, 13):
        return f"{value}th"
    return f"{value}{ORDINAL_SUFFIX.get(value % 10, 'th')}"


class BingoCard(Widget):
    def __init__(self, index, card, **kwargs):
        self.card = card

        self._grid_pos = y, x = divmod(index, 10)

        super().__init__(
            size=(5, 14),
            pos=(y * 6 + 1, x * 15 + 1),
            default_color_pair=DEFAULT_COLOR_PAIR,
            **kwargs,
        )

        self._is_won = False

        for y, row in enumerate(card):
            for x, k in enumerate(row):
                self.add_text(f"{k:>2}", y, 3 * x)

    def draw(self, n):
        if self._is_won:
            return

        card = self.card
        marked = card == n

        if not marked.any():
            return

        card[marked] = MARKED

        y, x = np.argwhere(marked).squeeze()

        self.add_text(" ✗", y, 3 * x)

        if (card[y] == MARKED).all():
            self._is_won = True
            self.colors[y, :, :3] = ROW_COLOR

        if (card[:, x] == MARKED).all():
            self._is_won = True
            self.colors[:, 3 * x + 1, :3] = ROW_COLOR

        if self._is_won:
            card[card == MARKED] = 0

            parent = self.parent

            parent.FINISHED += 1

            if parent.FINISHED in (1, 100):
                # Creating visual markers on ScrollView's scrollbars
                # These will be in an incorrect position if the window is re-sized.
                # To do this correctly, subclass ScrollView's scrollbars and
                # implement a `resize` method that moves these markers.
                y, x = self._grid_pos
                vbar, hbar = parent.parent.children

                vbar.colors[int((vbar.height - 2) * y / 9), :, 3:] = ROW_COLOR
                h_index = int((hbar.width - 4) * x / 9)
                hbar.colors[:, h_index: h_index + 2, 3:] = ROW_COLOR

                self.colors[1:4, :, :3] = ROW_COLOR
            else:
                self.colors[1:4, :, :3] = SCORE_COLOR

            self.add_text(f"{f'FINISHED {ordinal(parent.FINISHED)}':^14}", row=1)
            self.add_text(f"{'SCORE:':^14}", row=2)
            self.add_text(f"{card.sum() * n:^14}", row=3)


class BingoFolder(Widget):
    FINISHED = 0

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
            card.draw(n)
