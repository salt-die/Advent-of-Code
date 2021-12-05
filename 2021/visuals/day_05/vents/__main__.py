from pathlib import Path

import cv2
import numpy as np

from nurses_2.app import App
from nurses_2.colors import Color, color_pair
from nurses_2.widgets.behaviors import AutoSizeBehavior
from nurses_2.widgets.graphic_widget import GraphicWidget
from nurses_2.widgets.image import Image

from . import VENTS
from .stable_fluid import StableFluid

WATER_COLOR = Color.from_hex("0805bf")


class AutoSizeGraphicWidget(AutoSizeBehavior, GraphicWidget):
    ...


class AutoSizeImage(AutoSizeBehavior, Image):
    ...


class VentFluid(StableFluid):
    def resize(self, size):
        super().resize(size)

        h, w = size

        vent_y = cv2.resize(VENTS[0], (w, 2 * h))
        vent_x = cv2.resize(VENTS[1], (w, 2 * h))
        self._vent_field = np.stack((vent_y, vent_x))

    def on_press(self, key_press_event):
        match key_press_event.key:
            case " ":
                self.parent.children[1].is_visible ^= True
            case "r":
                self.dye[:] = 0

    def render(self, canvas_view, colors_view, rect):
        self.velocity += self._vent_field
        super().render(canvas_view, colors_view, rect)


class VentApp(App):
    async def on_start(self):
        self.root.add_widgets(
            VentFluid(),
            AutoSizeImage(
                path=Path("vents.png"),
                is_visible=False,
                alpha=.5,
            ),
            AutoSizeGraphicWidget(
                default_color_pair=color_pair(WATER_COLOR, WATER_COLOR),
                alpha=.5,
            ),
        )


VentApp().run()
