import asyncio
from pathlib import Path

from nurses_2.app import App
from nurses_2.colors import Color, color_pair, WHITE
from nurses_2.widgets import Widget
from nurses_2.widgets.behaviors import (
    AutoSizeBehavior,
    AutoPositionBehavior,
    Anchor,
)
from nurses_2.widgets.graphic_widget import GraphicWidget
from nurses_2.widgets.image import Image
from nurses_2.widgets.parallax import Parallax

from .commands import COMMANDS
from .stable_fluid import StableFluid

ASSETS = Path("assets")
PARALLAX_IMAGES = sorted((ASSETS / "parallax_frames").iterdir())
VELOCITY_SCALE = .035
WATER_COLOR = Color.from_hex("0805bf")
LABEL_COLOR = tuple(i//2 for i in WATER_COLOR)


class AutoGeometryImage(AutoSizeBehavior, AutoPositionBehavior, Image):
    ...


class AutoSizeGraphicWidget(AutoSizeBehavior, GraphicWidget):
    ...


class AutoPositionWidget(AutoPositionBehavior, Widget):
    ...


class AutoSizeParallax(AutoSizeBehavior, Parallax):
    ...


class SubmarineApp(App):
    async def on_start(self):
        background = AutoSizeParallax(
            layers=[AutoGeometryImage(path=path) for path in PARALLAX_IMAGES],
        )

        fluid = StableFluid(alpha=.5)

        submarine = AutoGeometryImage(
            path=ASSETS / "submarine.png",
            size_hint=(.2, .2),
            pos_hint=(.5, .5),
            anchor=Anchor.TOP_CENTER,
        )

        water_mask = AutoSizeGraphicWidget(
            default_color_pair=color_pair(WATER_COLOR, WATER_COLOR),
            alpha=.5,
        )

        label = AutoPositionWidget(
            size=(1, 18),
            default_color_pair=color_pair(WHITE, LABEL_COLOR),
            pos_hint=(None, .5),
            anchor=Anchor.TOP_CENTER,
        )
        label.add_text("Command:")

        self.root.add_widgets(background, fluid, submarine, water_mask, label)

        async def background_update():
            while True:
                fluid.poke()

                match command:
                    case "forward":
                        fluid.velocity[1] -= amount * VELOCITY_SCALE
                        background.horizontal_offset += amount
                    case "up":
                        fluid.velocity[0] += amount * VELOCITY_SCALE
                        background.vertical_offset -= amount
                    case "down":
                        fluid.velocity[0] -= amount * VELOCITY_SCALE
                        background.vertical_offset += amount

                try:
                    await asyncio.sleep(0)
                except asyncio.CancelledError:
                    return

        background_task = asyncio.create_task(background_update())

        for command, amount in COMMANDS:
            label.add_text(f'{f"{command} {amount}":<10}', column=9)
            await asyncio.sleep(1)

        background_task.cancel()


SubmarineApp().run()
