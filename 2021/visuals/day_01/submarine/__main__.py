import asyncio
from pathlib import Path

import numpy as np

from nurses_2.app import App
from nurses_2.colors import AColor
from nurses_2.widgets.graphic_widget import GraphicWidget, Anchor
from nurses_2.widgets.image import Image
from nurses_2.widgets.parallax import Parallax

from .ocean_floor import SCALE, create_floor_texture

ASSETS = Path("assets")
PARALLAX_IMAGES = ASSETS / "parallax_frames"

WATER_COLOR = AColor.from_hex("0805bf")

SCROLL_FPS = .05


class OceanFloor(GraphicWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        asyncio.create_task(self.travel())

    async def travel(self):
        entire_ocean_floor = create_floor_texture()
        entire_ocean_floor_width = entire_ocean_floor.shape[1]

        x = 20 * SCALE

        h, w = self.size
        current_depth = np.argwhere(np.any(entire_ocean_floor[:, x + w // 2], axis=-1)).min() - int(1.5 * h)

        while x + self.width < entire_ocean_floor_width:
            h, w = self.size
            depth = np.argwhere(np.any(entire_ocean_floor[:, x + w // 2], axis=-1)).min() - int(1.5 * h)

            for y in np.linspace(current_depth, depth, SCALE).astype(int):
                x += 1
                self.root.children[0].horizontal_offset += 1
                h, w = self.size
                self.texture[:] = entire_ocean_floor[y: y + 2 * h, x: x + w]

                try:
                    await asyncio.sleep(SCROLL_FPS)
                except asyncio.CancelledError:
                    return

            current_depth = depth


class SubmarineApp(App):
    async def on_start(self):
        background = Parallax(
            path=PARALLAX_IMAGES,
            size_hint=(1.0, 1.0),
        )

        submarine = Image(
            path=ASSETS / "submarine.png",
            pos_hint=(.2, .4),
            anchor=Anchor.CENTER,
            size_hint=(.25, .24),
        )

        water_mask = GraphicWidget(
            default_color=WATER_COLOR,
            alpha=.5,
            size_hint=(1.0, 1.0),
        )

        self.add_widgets(
            background,
            submarine,
            OceanFloor(size_hint=(1.0, 1.0)),
            water_mask,
        )


SubmarineApp().run()
