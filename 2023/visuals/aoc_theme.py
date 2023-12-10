from batgrl.colors import WHITE, AColor, Color, ColorPair, ColorTheme
from batgrl.gadgets.behaviors.button_behavior import ButtonBehavior
from batgrl.gadgets.behaviors.toggle_button_behavior import ToggleButtonBehavior
from batgrl.gadgets.text import Text

AOC_BLUE = Color.from_hex("0f0f23")
AOC_BRIGHT_GREEN = Color.from_hex("99ff99")
AOC_GREEN = Color.from_hex("009900")
AOC_GREY = Color.from_hex("cccccc")
AOC_YELLOW = Color.from_hex("eff263")
AOC_CODE_GRAY = Color.from_hex("10101A")
AOC_PRIMARY = ColorPair.from_colors(AOC_GREY, AOC_BLUE)
AOC_SECONDARY = ColorPair.from_colors(WHITE, AOC_BLUE)
AOC_GREEN_ON_BLUE = ColorPair.from_colors(AOC_GREEN, AOC_BLUE)
AOC_BRIGHT_GREEN_ON_BLUE = ColorPair.from_colors(AOC_BRIGHT_GREEN, AOC_BLUE)
AOC_CODE_BLOCK = ColorPair.from_colors(AOC_GREY, AOC_CODE_GRAY)
AOC_THEME = ColorTheme(
    primary=AOC_PRIMARY,
    text_pad_line_highlight=ColorPair.from_colors(AOC_GREY, Color.from_hex("161633")),
    text_pad_selection_highlight=ColorPair.from_hex("eff8fe0078d7"),
    textbox_primary=ColorPair.from_hex("9d9da010101a"),
    textbox_selection_highlight=ColorPair.from_hex("eff8fe0078d7"),
    textbox_placeholder=ColorPair.from_hex("3b3b3b10101a"),
    button_normal=AOC_GREEN_ON_BLUE,
    button_hover=AOC_BRIGHT_GREEN_ON_BLUE,
    button_press=AOC_BRIGHT_GREEN_ON_BLUE,
    scroll_view_scrollbar=Color.from_hex("111121"),
    scroll_view_indicator_normal=Color.from_hex("6f6f78"),
    scroll_view_indicator_hover=Color.from_hex("5c5c65"),
    scroll_view_indicator_press=Color.from_hex("3a3a44"),
    markdown_block_code_background=AOC_CODE_GRAY,
    # Will be added as needed...
    menu_item_hover=AOC_PRIMARY,
    menu_item_selected=AOC_PRIMARY,
    menu_item_disabled=AOC_PRIMARY,
    titlebar_normal=AOC_PRIMARY,
    titlebar_inactive=AOC_PRIMARY,
    window_border_normal=AColor.from_hex("cccccc"),
    window_border_inactive=AColor.from_hex("cccccc"),
    data_table_sort_indicator=AOC_PRIMARY,
    data_table_hover=AOC_PRIMARY,
    data_table_stripe=AOC_PRIMARY,
    data_table_stripe_hover=AOC_PRIMARY,
    data_table_selected=AOC_PRIMARY,
    data_table_selected_hover=AOC_PRIMARY,
    progress_bar=AOC_PRIMARY,
    markdown_link=AOC_PRIMARY,
    markdown_link_hover=AOC_PRIMARY,
    markdown_inline_code=AOC_PRIMARY,
    markdown_quote=AOC_PRIMARY,
    markdown_title=AOC_PRIMARY,
    markdown_image=AOC_PRIMARY,
    markdown_quote_block_code_background=AOC_GREY,
    markdown_header_background=AOC_GREY,
)


class AocButton(ButtonBehavior, Text):
    def __init__(self, label: str, callback, **kwargs):
        super().__init__(default_color_pair=AOC_THEME.button_normal, **kwargs)
        self.set_text(f"[{label}]")
        self.callback = callback

    def update_normal(self):
        self.colors[:] = AOC_THEME.button_normal

    def update_hover(self):
        self.colors[:] = AOC_THEME.button_hover

    def update_down(self):
        self.colors[:] = AOC_THEME.button_press

    def on_release(self):
        self.callback()


class AocToggle(ToggleButtonBehavior, Text):
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
        self.colors[:] = AOC_BRIGHT_GREEN_ON_BLUE

    def update_normal(self):
        self.colors[:] = AOC_GREEN_ON_BLUE

    def update_on(self):
        self.canvas[0, 1]["char"] = "x"

    def update_off(self):
        self.canvas[0, 1]["char"] = " "

    def on_release(self):
        self.callback(self.toggle_state)
