import asyncio

from nurses_2.app import App
from nurses_2.colors import Color, color_pair, WHITE
from nurses_2.widgets import Widget
from nurses_2.widgets.behaviors import AutoSizeBehavior
from nurses_2.widgets.scroll_view import ScrollView

from . import NUMBERS, CARDS
from .bingo_widgets import BingoCard, BingoFolder

DEFAULT_COLOR_PAIR = color_pair(Color.from_hex("#741aac"), Color.from_hex("#340744"))
LABEL_DEFAULT_COLOR_PAIR = color_pair(WHITE, Color.from_hex("#340744"))


class AutoSizeScrollView(AutoSizeBehavior, ScrollView):
    def resize(self, size):
        h, w = size
        super().resize((h - 1, w))


class AutoSizeWidget(AutoSizeBehavior, Widget):
    ...


class BingoApp(App):
    async def on_start(self):
        folder = BingoFolder(
            cards=[BingoCard(i, card) for i, card in enumerate(CARDS)],
            default_color_pair=DEFAULT_COLOR_PAIR,
        )

        label = AutoSizeWidget(
            size=(1, 10),
            size_hint=(None, 1),
            default_color_pair=LABEL_DEFAULT_COLOR_PAIR,
        )

        scroll_view = AutoSizeScrollView(pos=(1, 0))
        scroll_view.add_widget(folder)

        self.root.add_widgets(label, scroll_view)

        for number in NUMBERS:
            folder.draw(number)
            label.add_text(f"{f'Draw: {number}':^{label.width}}")
            await asyncio.sleep(.5)


BingoApp().run()
