from aoc_lube.utils import extract_ints
import numpy as np

from nurses_2.app import App
from nurses_2.colors import Color, ColorPair, WHITE, lerp_colors
from nurses_2.io import MouseEventType
from nurses_2.widgets.button import Button
from nurses_2.widgets.text_pad import TextPad
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.split_layout import VSplitLayout

from .cube import Cube
from .drop_renderer import DropRenderer

AOC_BRIGHT_GREEN = Color.from_hex("99ff99")
AOC_BLUE = Color.from_hex("0f0f23")
AOC_CODE_BLUE = Color.from_hex("10101a")
AOC_GREEN = Color.from_hex("009900")
AOC_GREY = Color.from_hex("cccccc")
BLUE_ON_BLUE = ColorPair.from_colors(AOC_BLUE, AOC_BLUE)
CODE_BLUE_ON_BLUE = ColorPair.from_colors(AOC_CODE_BLUE, AOC_CODE_BLUE)
GREY_ON_BLUE = ColorPair.from_colors(AOC_GREY, AOC_CODE_BLUE)
GREEN_ON_BLUE = ColorPair.from_colors(AOC_GREEN, AOC_CODE_BLUE)
BRIGHT_GREEN_ON_BLUE = ColorPair.from_colors(AOC_BRIGHT_GREEN, AOC_CODE_BLUE)

EXAMPLE_INPUT = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

def generate_drop_positions(text):
    data = np.fromiter(extract_ints(text), int).reshape(-1, 3)
    data -= data.min(axis=0)
    data -= data.max() // 2
    for pos in data:
        yield Cube(pos)


class ModalTextWidget(TextWidget):
    def on_mouse(self, mouse_event):
        if mouse_event.event_type is not MouseEventType.MOUSE_MOVE:
            self.is_enabled = False


class LavaApp(App):
    async def on_start(self):
        split_layout = VSplitLayout(size_hint=(1.0, 1.0))

        renderer = DropRenderer(size_hint=(1.0, 1.0))

        error_message = ModalTextWidget(
            size=(3, 21),
            pos_hint=(.5, .5),
            anchor="center",
            is_enabled=False,
            default_color_pair=GREY_ON_BLUE,
        )
        error_message.add_border()
        error_message.add_text("Error parsing data.", row=1, column=1)

        data_input = TextPad(
            size_hint=(1.0, 1.0),
            ptf_on_focus=False,
            disable_ptf=True,
            show_horizontal_bar=False,
            show_vertical_bar=False,
        )
        # Colors usually set by theme we are manually changing. (We want two themes!)
        data_input._pad.colors[:] = GREY_ON_BLUE
        data_input._pad.default_color_pair = GREY_ON_BLUE
        data_input.background_color_pair = CODE_BLUE_ON_BLUE
        data_input.selection_hightlight = lerp_colors(AOC_CODE_BLUE, WHITE, 1/10)
        data_input.line_highlight = lerp_colors(AOC_CODE_BLUE, WHITE, 1/40)
        data_input.text = EXAMPLE_INPUT

        def button_callback():
            try:
                drops = list(generate_drop_positions(data_input.text))
            except:
                error_message.is_enabled = True
            else:
                renderer.drops = drops
                renderer._render_drops()

        enter_input = Button(
            size=(1, 14),
            label="[ Enter Data ]",
            pos_hint=(None, .5),
            anchor="bottom_center",
            callback=button_callback,
        )
        enter_input.subscribe(
            split_layout.left_pane,
            "size",
            lambda: setattr(enter_input, "y", split_layout.left_pane.bottom - 2),
        )
        # Colors usually set by theme we are manually changing. (We want two themes!)
        enter_input.normal_color_pair = GREEN_ON_BLUE
        enter_input.hover_color_pair = BRIGHT_GREEN_ON_BLUE
        enter_input.down_color_pair = BRIGHT_GREEN_ON_BLUE
        enter_input.update_normal()

        split_layout.left_pane.add_widgets(data_input, enter_input)
        split_layout.right_pane.add_widget(renderer)
        self.add_widgets(split_layout, error_message)
        split_layout.split_col = 20


LavaApp(title="Lava Renderer", background_color_pair=BLUE_ON_BLUE).run()
