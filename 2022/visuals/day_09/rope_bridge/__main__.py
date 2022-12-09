import numpy as np

from nurses_2.app import App
from nurses_2.colors import AColor, Color, ColorPair, ColorTheme
from nurses_2.io import MouseEventType
from nurses_2.widgets.button import Button
from nurses_2.widgets.slider import Slider
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.graphic_widget import GraphicWidget

AOC_GREEN = Color.from_hex("009900")
AOC_AGREEN = AColor.from_hex("009900")
AOC_BRIGHT_GREEN = Color.from_hex("99ff99")
AOC_BLUE = Color.from_hex("0f0f23")
AOC_ABLUE = AColor.from_hex("0f0f23")
AOC_AGREY = AColor.from_hex("cccccc")
ROPE_ACOLOR = AColor.from_hex("514008")
GREEN_ON_BLUE = ColorPair.from_colors(AOC_AGREEN, AOC_ABLUE)
AOC_THEME = ColorTheme(
    primary_fg=AOC_GREEN,
    primary_bg=AOC_BLUE,
    primary_fg_light=AOC_BRIGHT_GREEN,
    primary_bg_light=AOC_BLUE,
    primary_fg_dark=AOC_GREEN,
    primary_bg_dark=AOC_BLUE,
    secondary_fg=AOC_BRIGHT_GREEN,
    secondary_bg=AOC_BLUE,
)


class RopeWidget(GraphicWidget):
    def __init__(self, rope, rope_color, tail_tracker, tail_color, **kwargs):
        super().__init__(**kwargs)
        self.rope = rope
        self.rope_color = rope_color
        self.tail_tracker = tail_tracker
        self.tail_color = tail_color

    def on_mouse(self, mouse_event):
        if (
            mouse_event.event_type is MouseEventType.MOUSE_MOVE and
            self.collides_point(mouse_event.position)
        ):
            y, x = self.to_local(mouse_event.position)
            y *= 2

            rope = self.rope
            rope[0] = np.array([y, x])
            for i in range(len(rope) - 1):
                delta = rope[i] - rope[i + 1]
                rope[i + 1] += np.clip(delta, -1, 1) * (abs(delta).max() > 1)

            self.texture[:] = self.default_color
            for y, x in rope:
                self.texture[y, x] = self.rope_color
            self.tail_tracker.texture[y, x] = self.tail_color


class RopeBridgeApp(App):
    async def on_start(self):
        rope = [np.zeros(2, int), np.zeros(2, int)]

        tail_tracker = GraphicWidget(size_hint=(1.0, 1.0), default_color=AOC_ABLUE)

        rope_widget = RopeWidget(
            rope=rope,
            rope_color=ROPE_ACOLOR,
            tail_tracker=tail_tracker,
            tail_color=AOC_AGREY,
            size_hint=(1.0, 1.0),
        )

        slider_label = TextWidget(
            pos_hint=(None, .5),
            anchor="top_center",
            size=(1, 19),
            default_color_pair=GREEN_ON_BLUE
        )

        def slider_update(n):
            n = int(n)
            l = len(rope)
            if n > l:
                rope.extend(rope[-1].copy() for _ in range(n - l))
            elif n < l:
                del rope[n:]

            slider_label.add_text(f"Number of knots: {n:<2}")

        slider = Slider(
            pos=(1, 1),
            pos_hint=(None, .5),
            anchor="top_center",
            size=(1, 48),
            min=2,
            max=50,
            start_value=2,
            fill_color=AOC_BRIGHT_GREEN,
            callback=slider_update,
            default_color_pair=GREEN_ON_BLUE,
        )

        def reset_tail():
            tail_tracker.texture[:] = tail_tracker.default_color
        tail_tracker.subscribe(tail_tracker, "size", reset_tail)

        reset_button = Button(
            label="[Reset]",
            callback=reset_tail,
            size=(1, 9),
            pos_hint=(None, .5),
            pos=(2, 1),
            anchor="top_center",
        )

        self.add_widgets(tail_tracker, rope_widget, slider, slider_label, reset_button)


RopeBridgeApp(title="--- Day 9: Rope Bridge ---", color_theme=AOC_THEME).run()
