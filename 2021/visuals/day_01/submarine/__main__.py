import asyncio
from pathlib import Path

import numpy as np

from nurses_2.app import App
from nurses_2.colors import Color, color_pair
from nurses_2.widgets.behaviors import AutoSizeBehavior, AutoPositionBehavior, Anchor
from nurses_2.widgets.graphic_widget import GraphicWidget
from nurses_2.widgets.image import Image
from nurses_2.widgets.parallax import Parallax

from .ocean_floor import SCALE, create_floor_texture

PARALLAX_IMAGES = sorted(Path("parallax_frames").iterdir())
NIMAGES = len(PARALLAX_IMAGES)

WATER_COLOR = Color.from_hex("0805bf")

SCROLL_FPS = .05


class AutoGeometryImage(AutoSizeBehavior, AutoPositionBehavior, Image):
    ...


class AutoSizeGraphicWidget(AutoSizeBehavior, GraphicWidget):
    ...


class AutoSizeParallax(AutoSizeBehavior, Parallax):
    ...


class OceanFloor(AutoSizeBehavior, GraphicWidget):
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
        background = AutoSizeParallax(
            layers=[AutoGeometryImage(path=path) for path in PARALLAX_IMAGES],
        )

        submarine = AutoGeometryImage(
            path=Path("submarine.png"),
            pos_hint=(.2, .4),
            anchor=Anchor.CENTER,
            size_hint=(.2, .2),
        )

        water_mask = AutoSizeGraphicWidget(
            default_color_pair=color_pair(WATER_COLOR, WATER_COLOR),
            alpha=.5,
        )

        self.root.add_widgets(
            background,
            submarine,
            OceanFloor(),
            water_mask,
        )


SubmarineApp().run()
