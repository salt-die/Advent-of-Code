from batgrl.colors import ColorTheme
from batgrl.gadgets.behaviors.button_behavior import ButtonBehavior
from batgrl.gadgets.behaviors.themable import Themable
from batgrl.gadgets.behaviors.toggle_button_behavior import ToggleButtonBehavior
from batgrl.gadgets.text import Text
from batgrl.text_tools import Style

AOC_THEME: ColorTheme = {
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
    "button_disallowed_fg": "222222",
    "button_disallowed_bg": "0f0f23",
    "progress_bar_fg": "cccccc",
    "progress_bar_bg": "0f0f23",
    "scroll_view_scrollbar": "111121",
    "scroll_view_indicator_normal": "6f6f78",
    "scroll_view_indicator_hover": "5c5c65",
    "scroll_view_indicator_press": "3a3a44",
    "markdown_block_code_bg": "10101a",
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
        elif self.button_state == "disallowed":
            self.update_disallowed()
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

    def update_disallowed(self):
        self.canvas["fg_color"] = self.get_color("button_disallowed_fg")
        self.canvas["bg_color"] = self.get_color("button_disallowed_bg")
        self.canvas["style"] = Style.NO_STYLE

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
