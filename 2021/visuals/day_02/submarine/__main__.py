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
VELOCITY_SCALE = .1
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
        background.command = "forward"
        background.amount = 0

        fluid = StableFluid(alpha=.5)

        submarine = AutoGeometryImage(
            path=ASSETS / "submarine.png",
            size_hint=(.2, .2),
            pos_hint=(.5, .5),
            anchor=Anchor.CENTER,
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

        async def parallax_move():
            while True:
                match background.command:
                    case "forward":
                        background.horizontal_offset += background.amount
                    case "up":
                        background.vertical_offset -= background.amount
                    case "down":
                        background.vertical_offset += background.amount

                try:
                    await asyncio.sleep(0)
                except asyncio.CancelledError:
                    return

        async def fluid_update():
            while True:
                fluid.poke()

                try:
                    await asyncio.sleep(.1)
                except asyncio.CancelledError:
                    return

        parallax_task = asyncio.create_task(parallax_move())
        fluid_task = asyncio.create_task(fluid_update())

        for command, amount in COMMANDS:
            background.command = command
            background.amount = int(amount)

            match command:
                case "forward":
                    fluid.velocity[1] -= float(amount) * VELOCITY_SCALE
                case "up":
                    fluid.velocity[0] += float(amount) * VELOCITY_SCALE
                case "down":
                    fluid.velocity[0] -= float(amount) * VELOCITY_SCALE

            label.add_text(f'{f"{command} {amount}":<10}', column=9)

            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                return

        parallax_task.cancel()
        fluid_task.cancel()


SubmarineApp().run()
