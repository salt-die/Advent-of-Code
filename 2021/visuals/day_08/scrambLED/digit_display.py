import asyncio
import numpy as np

from nurses_2.colors import Color, ColorPair, BLACK, WHITE, gradient
from nurses_2.widgets import Widget
from nurses_2.widgets.behaviors import AutoPositionBehavior

DIM_GREEN = Color.from_hex("062b0f")
BRIGHT_GREEN = Color.from_hex("33e860")

DIM_GREEN_ON_BLACK = ColorPair.from_colors(DIM_GREEN, BLACK)
BRIGHT_GREEN_ON_BLACK = ColorPair.from_colors(BRIGHT_GREEN, BLACK)

GREEN_TO_WHITE = gradient(BRIGHT_GREEN, WHITE, 40) + gradient(WHITE, BRIGHT_GREEN, 40)

SEGMENT_SLICES = {
 "a": np.s_[ 0, 1: -1, :3],
 "b": np.s_[ 1: 3,  0, :3],
 "c": np.s_[ 1: 3, -1, :3],
 "d": np.s_[ 3, 1: -1, :3],
 "e": np.s_[ 4: 6,  0, :3],
 "f": np.s_[ 4: 6, -1, :3],
 "g": np.s_[-1, 1: -1, :3],
}


class DigitDisplay(Widget):
    def __init__(self, pos=(0, 0), **kwargs):
        super().__init__(
            size=(7, 6),
            pos=pos,
            default_color_pair=DIM_GREEN_ON_BLACK,
            **kwargs,
        )

        self.reset()

        canvas = self.canvas
        canvas[[0, 3, 6], 1: -1] = "━"
        canvas[1: 3,  [0, -1]] = canvas[4: 6, [0, -1]] = "┃"

    def flash(self):
        asyncio.create_task(self._flash())

    async def _flash(self):
        colors = self.colors[..., :3]
        mask = np.all(colors==BRIGHT_GREEN, axis=-1)
        for color in GREEN_TO_WHITE:
            colors[mask] = color
            await asyncio.sleep(.01)

    def reset(self):
        for segment in "abcdefg":
            setattr(self, segment, False)

    def __setattr__(self, attr, value):
        if attr in SEGMENT_SLICES:
            self.colors[SEGMENT_SLICES[attr]] = BRIGHT_GREEN if value else DIM_GREEN
        else:
            return super().__setattr__(attr, value)


class DigitFolder(AutoPositionBehavior, Widget):
    def __init__(self, pos=(0, 0), default_color_pair=BRIGHT_GREEN_ON_BLACK, **kwargs):
        super().__init__(
            size=(9, 14 * 7 + 3),
            pos=pos,
            default_color_pair=default_color_pair,
            **kwargs,
        )

        for i in range(14):
            self.add_widget(DigitDisplay(pos=(1, i * 7 + (1 if i < 10 else 3))))

        self.add_border(*"┏┓┗┛┃━")
        self.canvas[1: -1, 71] = "┃"
        self.canvas[[0, -1], 71] = "┳", "┻"
