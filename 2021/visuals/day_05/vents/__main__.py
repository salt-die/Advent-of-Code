from pathlib import Path

import cv2
import numpy as np

from nurses_2.app import App
from nurses_2.colors import AColor
from nurses_2.widgets.graphic_widget import GraphicWidget
from nurses_2.widgets.image import Image

from . import VENTS
from .stable_fluid import StableFluid

WATER_COLOR = AColor.from_hex("0805bf")


class VentFluid(StableFluid):
    def on_size(self):
        super().on_size()

        h, w = self._size

        vent_y = cv2.resize(VENTS[0], (w, 2 * h))
        vent_x = cv2.resize(VENTS[1], (w, 2 * h))
        self._vent_field = np.stack((vent_y, vent_x))

    def on_press(self, key_press_event):
        match key_press_event.key:
            case " ":
                self.parent.children[1].is_visible ^= True
            case "r":
                self.dye[:] = 0

    def render(self, canvas_view, colors_view, source: tuple[slice, slice]):
        self.velocity += self._vent_field
        super().render(canvas_view, colors_view, source)


class VentApp(App):
    async def on_start(self):
        self.add_widgets(
            VentFluid(size_hint=(1.0, 1.0)),
            Image(
                path=Path("vents.png"),
                is_visible=False,
                alpha=.5,
                size_hint=(1.0, 1.0),
            ),
            GraphicWidget(
                default_color=WATER_COLOR,
                alpha=.5,
                size_hint=(1.0, 1.0),
            ),
        )


VentApp().run()
