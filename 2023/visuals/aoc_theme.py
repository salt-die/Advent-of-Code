from batgrl.colors import WHITE, ColorTheme
from batgrl.gadgets.behaviors.button_behavior import ButtonBehavior
from batgrl.gadgets.behaviors.themable import Themable
from batgrl.gadgets.behaviors.toggle_button_behavior import ToggleButtonBehavior
from batgrl.gadgets.text import Text

AOC_BLUE = "0f0f23"
AOC_BRIGHT_GREEN = "99ff99"
AOC_GREEN = "009900"
AOC_GREY = "cccccc"
AOC_YELLOW = "eff263"
AOC_CODE_GRAY = "10101A"
AOC_PRIMARY = {"fg": "cccccc", "bg": "0f0f23"}
AOC_SECONDARY = {"fg": WHITE, "bg": AOC_BLUE}
AOC_GREEN_ON_BLUE = {"fg": AOC_GREEN, "bg": AOC_BLUE}
AOC_BRIGHT_GREEN_ON_BLUE = {"fg": AOC_BRIGHT_GREEN, "bg": AOC_BLUE}
AOC_CODE_BLOCK = {"fg": AOC_GREY, "bg": AOC_CODE_GRAY}
AOC_THEME = ColorTheme(
    primary=AOC_PRIMARY,
    text_pad_line_highlight={"fg": AOC_GREY, "bg": "161633"},
    text_pad_selection_highlight={"fg": "eff8fe", "bg": "0078d7"},
    textbox_primary={"fg": "9d9da0", "bg": "10101a"},
    textbox_selection_highlight={"fg": "eff8fe", "bg": "0078d7"},
    textbox_placeholder={"fg": "3b3b3b", "bg": "10101a"},
    button_normal=AOC_GREEN_ON_BLUE,
    button_hover=AOC_BRIGHT_GREEN_ON_BLUE,
    button_press=AOC_BRIGHT_GREEN_ON_BLUE,
    progress_bar=AOC_PRIMARY,
    scroll_view_scrollbar="111121",
    scroll_view_indicator_normal="6f6f78",
    scroll_view_indicator_hover="5c5c65",
    scroll_view_indicator_press="3a3a44",
    markdown_block_code_background=AOC_CODE_GRAY,
    # Will be added as needed...
    menu_item_hover=AOC_PRIMARY,
    menu_item_selected=AOC_PRIMARY,
    menu_item_disabled=AOC_PRIMARY,
    titlebar_normal=AOC_PRIMARY,
    titlebar_inactive=AOC_PRIMARY,
    window_border_normal="cccccc",
    window_border_inactive="cccccc",
    data_table_sort_indicator=AOC_PRIMARY,
    data_table_hover=AOC_PRIMARY,
    data_table_stripe=AOC_PRIMARY,
    data_table_stripe_hover=AOC_PRIMARY,
    data_table_selected=AOC_PRIMARY,
    data_table_selected_hover=AOC_PRIMARY,
    markdown_link=AOC_PRIMARY,
    markdown_link_hover=AOC_PRIMARY,
    markdown_inline_code=AOC_PRIMARY,
    markdown_quote=AOC_PRIMARY,
    markdown_title=AOC_PRIMARY,
    markdown_image=AOC_PRIMARY,
    markdown_quote_block_code_background=AOC_GREY,
    markdown_header_background=AOC_GREY,
)


class AocButton(Themable, ButtonBehavior, Text):
    def __init__(self, label: str, callback, **kwargs):
        super().__init__(**kwargs)
        self.default_fg_color = self.color_theme.primary.fg
        self.default_bg_color = self.color_theme.primary.bg
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
        self.canvas["fg_color"] = self.color_theme.button_normal.fg
        self.canvas["bg_color"] = self.color_theme.button_normal.bg

    def update_hover(self):
        self.canvas["fg_color"] = self.color_theme.button_hover.fg
        self.canvas["bg_color"] = self.color_theme.button_hover.bg

    def update_down(self):
        self.canvas["fg_color"] = self.color_theme.button_press.fg
        self.canvas["bg_color"] = self.color_theme.button_press.bg

    def on_release(self):
        self.callback()


class AocToggle(Themable, ToggleButtonBehavior, Text):
    def __init__(self, label, callback, **kwargs):
        super().__init__(**kwargs)
        self.set_text(f"[ ] {label}")
        self.update_normal()
        self.callback = callback
        if self.toggle_state == "on":
            self.update_on()
        else:
            self.update_off()

    def update_hover(self):
        self.canvas["fg_color"] = self.color_theme.button_hover.fg
        self.canvas["bg_color"] = self.color_theme.button_hover.bg

    def update_normal(self):
        self.canvas["fg_color"] = self.color_theme.button_normal.fg
        self.canvas["bg_color"] = self.color_theme.button_normal.bg

    def update_on(self):
        self.canvas[0, 1]["char"] = "x"

    def update_off(self):
        self.canvas[0, 1]["char"] = " "

    def on_release(self):
        self.callback(self.toggle_state)
