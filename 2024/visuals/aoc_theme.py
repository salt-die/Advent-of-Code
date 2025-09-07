from batgrl.gadgets.behaviors.button_behavior import ButtonBehavior
from batgrl.gadgets.behaviors.themable import Themable
from batgrl.gadgets.behaviors.toggle_button_behavior import ToggleButtonBehavior
from batgrl.gadgets.text import Text
from batgrl.text_tools import Style

AOC_THEME = {
    "primary_fg": "cccccc",
    "primary_bg": "0f0f23",
    "text_pad_line_highlight_fg": "cccccc",
    "text_pad_line_highlight_bg": "161633",
    "text_pad_selection_highlight_fg": "eff8fe",
    "text_pad_selection_highlight_bg": "0078d7",
    "textbox_primary_fg": "9d9da0",
    "textbox_primary_bg": "10101a",
    "textbox_selection_highlight_fg": "eff8fe",
    "textbox_selection_highlight_bg": "0078d7",
    "textbox_placeholder_fg": "3b3b3b",
    "textbox_placeholder_bg": "10101a",
    "button_normal_fg": "009900",
    "button_normal_bg": "0f0f23",
    "button_hover_fg": "99ff99",
    "button_hover_bg": "0f0f23",
    "button_press_fg": "99ff99",
    "button_press_bg": "0f0f23",
    "progress_bar_fg": "cccccc",
    "progress_bar_bg": "0f0f23",
    "scroll_view_scrollbar": "111121",
    "scroll_view_indicator_normal": "6f6f78",
    "scroll_view_indicator_hover": "5c5c65",
    "scroll_view_indicator_press": "3a3a44",
    "markdown_block_code_background": "10101a",
    "titlebar_normal_fg": "99ff99",
    "titlebar_normal_bg": "0f0f23",
    "titlebar_inactive_fg": "009900",
    "titlebar_inactive_bg": "0f0f23",
}


class AocButton(Themable, ButtonBehavior, Text):
    def __init__(self, label: str, callback, **kwargs):
        super().__init__(**kwargs)
        self.default_fg_color = self.get_color("primary_fg")
        self.default_bg_color = self.get_color("primary_bg")
        self.set_text(f"[{label}]")
        self.callback = callback

    def update_theme(self):
        if self.button_state == "normal":
            self.update_normal()
        elif self.button_state == "hover":
            self.update_hover()
        else:
            self.update_down()

    def update_normal(self):
        self.canvas["fg_color"] = self.get_color("button_normal_fg")
        self.canvas["bg_color"] = self.get_color("button_normal_bg")
        self.canvas["style"] = Style.NO_STYLE

    def update_hover(self):
        self.canvas["fg_color"] = self.get_color("button_hover_fg")
        self.canvas["bg_color"] = self.get_color("button_hover_bg")
        self.canvas["style"] = Style.BOLD

    def on_release(self):
        self.callback()


class AocToggle(Themable, ToggleButtonBehavior, Text):
    def __init__(self, label, callback, **kwargs):
        super().__init__(**kwargs)
        self.default_fg_color = self.get_color("primary_fg")
        self.default_bg_color = self.get_color("primary_bg")
        self.set_text(f"[ ] {label}")
        self.callback = callback

    def update_theme(self):
        if self.button_state == "normal":
            self.update_normal()
        elif self.button_state == "hover":
            self.update_hover()
        else:
            self.update_down()

        if self.toggle_state == "on":
            self.update_on()
        else:
            self.update_off()

    def update_normal(self):
        self.canvas["fg_color"] = self.get_color("button_normal_fg")
        self.canvas["bg_color"] = self.get_color("button_normal_bg")
        self.canvas["style"] = Style.NO_STYLE

    def update_hover(self):
        self.canvas["fg_color"] = self.get_color("button_hover_fg")
        self.canvas["bg_color"] = self.get_color("button_hover_bg")
        self.canvas["style"] |= Style.BOLD

    def update_on(self):
        self.canvas[0, 1]["ord"] = ord("x")

    def update_off(self):
        self.canvas[0, 1]["ord"] = ord(" ")

    def on_release(self):
        super().on_release()
        self.callback(self.toggle_state)


class AocText(Themable, Text):
    def update_theme(self):
        self.default_fg_color = self.get_color("primary_fg")
        self.default_bg_color = self.get_color("primary_bg")
        self.canvas["fg_color"] = self.get_color("primary_fg")
        self.canvas["bg_color"] = self.get_color("primary_bg")


if __name__ == "__main__":
    import asyncio
    from colorsys import hsv_to_rgb
    from pathlib import Path
    from random import choice, random
    from typing import Literal

    import numpy as np
    from batgrl.app import App
    from batgrl.colors import Color, gradient

    GREEN = Color.from_hex("009900")
    TRUNK = Color.from_hex("cccccc")
    OFF = Color.from_hex("333333")
    TREE = (Path(__file__).parent / "assets" / "tree.txt").read_text()

    def random_color():
        r, g, b = hsv_to_rgb(random() * np.pi * 2, 1.0, 1.0)
        return Color(int(r * 255), int(g * 255), int(b * 255))

    async def light_effect(
        ornament: Literal["*", "@", "O", "o"],
        kind: Literal["blink", "gradient"],
        delay: float,
        start_color: Color,
        end_color: Color,
        canvas,
    ):
        chars = canvas["char"]
        colors = canvas["fg_color"]

        if kind == "blink":
            while True:
                colors[chars == ornament] = start_color
                await asyncio.sleep(delay * 20)
                colors[chars == ornament] = end_color
                await asyncio.sleep(delay * 20)
        else:
            grad = gradient(start_color, end_color, n=10)
            grad += gradient(end_color, start_color, n=10)
            i = 0
            while True:
                colors[chars == ornament] = grad[i]
                i += 1
                i %= len(grad)
                await asyncio.sleep(delay)

    class ButtonTestApp(App):
        async def on_start(self):
            tree = Text(is_transparent=True)
            tree.set_text(TREE)
            chars = tree.canvas["char"]
            colors = tree.canvas["fg_color"]
            bolds = tree.canvas["bold"]
            colors[np.isin(chars, (">", "<"))] = GREEN
            colors[np.isin(chars, ("|", "_"))] = TRUNK
            bolds[np.isin(chars, ("*", "@", "O", "o", "_", "|"))] = True
            colors[np.isin(chars, ("*", "@", "O", "o"))] = OFF

            tasks = []

            def light_tree(state):
                if state == "on":
                    for ornament in "*@Oo":
                        coro = light_effect(
                            ornament,
                            choice(["blink", "gradient"]),
                            random() / 10,
                            random_color(),
                            random_color(),
                            tree.canvas,
                        )
                        tasks.append(asyncio.create_task(coro))
                else:
                    for task in tasks:
                        task.cancel()
                    tasks.clear()
                    colors[np.isin(chars, ("*", "@", "O", "o"))] = OFF

            light_button = AocToggle("Lights!", light_tree)

            def shuffle():
                if light_button.toggle_state == "off":
                    return
                light_tree("off")
                light_tree("on")

            shuffle_button = AocButton("Shuffle", shuffle)
            light_button.center = tree.center
            shuffle_button.center = tree.center
            light_button.top = tree.bottom
            shuffle_button.top = light_button.bottom
            self.add_gadgets(tree, light_button, shuffle_button)

    ButtonTestApp(color_theme=AOC_THEME, title="Advent of Code 2024").run()
