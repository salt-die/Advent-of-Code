from nurses_2.app import App
from nurses_2.widgets.graphic_widget import Interpolation

from . import (
    INSTRUCTIONS,
    NAVY_BLUE,
    YELLOW_ON_BLUE,
)
from .folding_widget import FoldingWidget


class Folding(App):
    async def on_start(self):
        paper = FoldingWidget(
            default_color=NAVY_BLUE,
            interpolation=Interpolation.NEAREST,
            size_hint=(1.0, 1.0),
        )

        self.add_widget(paper)

        for axis in INSTRUCTIONS:
            await paper.fold(axis)


Folding(default_color_pair=YELLOW_ON_BLUE).run()
