import asyncio
from random import choice

import cv2
from aoc_theme import AOC_THEME, AocButton, AocText
from batgrl.app import App
from batgrl.colors import BLACK, WHITE, Color, lerp_colors
from batgrl.gadgets.behaviors.button_behavior import ButtonBehavior
from batgrl.gadgets.behaviors.movable import Movable
from batgrl.gadgets.behaviors.themable import Themable
from batgrl.gadgets.grid_layout import GridLayout
from batgrl.gadgets.text import Text

W = Color.from_hex("dee3e8")
U = Color.from_hex("2f87e0")
B = Color.from_hex("3a3939")
R = Color.from_hex("e22424")
G = Color.from_hex("2ccc2f")
COLORS = {"w": W, "u": U, "b": B, "r": R, "g": G}


class ColorButton(ButtonBehavior, Themable, Text):
    def __init__(self, name, color, callback, **kwargs):
        super().__init__(**kwargs)
        self.default_fg_color = color
        self.clear()
        self.set_text(f" {name} ")
        self.callback = callback

    def update_theme(self):
        self.default_bg_color = self.get_color("primary_bg")
        self.canvas["bg_color"] = self.get_color("primary_bg")

    def update_normal(self):
        self.canvas["bg_color"] = self.default_bg_color

    def update_hover(self):
        self.canvas["bg_color"] = lerp_colors(self.default_bg_color, WHITE, 0.33)

    def on_release(self):
        self.callback()


class TowelButton(ButtonBehavior, Themable, Text):
    def __init__(self, destroy_callback, design_label, **kwargs):
        super().__init__(**kwargs)
        self.destroy_callback = destroy_callback
        self.design_label = design_label

    def update_theme(self):
        self.default_bg_color = self.get_color("primary_bg")
        self.canvas["bg_color"] = self.get_color("primary_bg")

    def update_normal(self):
        self.canvas["bg_color"] = self.default_bg_color

    def update_hover(self):
        self.canvas["bg_color"] = lerp_colors(self.default_bg_color, WHITE, 0.33)

    def on_mouse(self, mouse_event):
        if (
            self.collides_point(mouse_event.pos)
            and mouse_event.event_type == "mouse_down"
        ):
            if mouse_event.button == "right":
                self.destroy()
                self.destroy_callback()
            elif mouse_event.button == "left" and not self.app.all_matched.is_set():
                towel = Towel(
                    self,
                    self.design_label,
                    size=self.size,
                    pos=mouse_event.pos - self.root.pos,
                )
                towel.canvas[:] = self.canvas
                towel.canvas["bg_color"] = self.default_bg_color
                self.root.add_gadget(towel)
                towel.grab(mouse_event)
        return super().on_mouse(mouse_event)


class Towel(Movable, Text):
    def __init__(self, creator, design_label, **kwargs):
        super().__init__(**kwargs)
        self.creator = creator
        self.design_label = design_label
        self.initial_pos = self.pos
        self.matched = False

    def check_win(self):
        all_xs = set(range(self.design_label.left + 3, self.design_label.right))
        for gadget in self.root.walk():
            if isinstance(gadget, Towel):
                for i in range(gadget.left, gadget.right):
                    if i in all_xs:
                        all_xs.remove(i)
                    else:
                        return
        if not all_xs:
            self.app.all_matched.set()

    def intersects(self):
        seen = set()
        for gadget in self.root.walk():
            if isinstance(gadget, Towel):
                for i in range(gadget.left, gadget.right):
                    if i in seen:
                        return True
                    seen.add(i)
        return False

    def ungrab(self, mouse_event):
        self.creator.on_mouse(mouse_event)
        if self.matched:
            self.y = 3
            self.check_win()
        else:
            coro = self.tween(
                pos=self.initial_pos,
                duration=0.5,
                easing="out_bounce",
                on_complete=self.destroy,
            )
            asyncio.create_task(coro)
        return super().ungrab(mouse_event)

    def grab_update(self, mouse_event):
        super().grab_update(mouse_event)
        y, x = self.pos
        x -= 12
        if x < 0:
            self.matched = False
        else:
            sub_design = self.design_label.canvas["ord"][:, x : x + self.width]

            self.matched = (
                abs(y - 3) < 2
                and not self.intersects()
                and sub_design.shape == self.size
                and (sub_design == self.canvas["ord"]).all()
            )
        if self.matched:
            self.canvas["bg_color"] = lerp_colors(self.creator.default_bg_color, G, 0.3)
        else:
            self.canvas["bg_color"] = self.creator.default_bg_color


class LinenLayoutApp(App):
    async def on_start(self):
        self.towel_buttons: dict[str, TowelButton] = {}
        self.current_towel = ""
        self.current_design = ""
        self.all_matched = asyncio.Event()
        self.level = 1

        design_label = AocText(pos=(3, 12))
        design_label.set_text(" : ")

        def create_new_design():
            self.all_matched.clear()
            for gadget in self.root.children.copy():
                if isinstance(gadget, Towel):
                    gadget.destroy()

            if not self.towel_buttons:
                self.current_design = ""
                design_label.set_text(" : ")
                return

            seq = list(self.towel_buttons)
            self.current_design = ""
            while len(self.current_design) < 8 * self.level:
                self.current_design += choice(seq)
            design_label.set_text(f" : {self.current_design}")
            for i, char in enumerate(self.current_design, start=3):
                design_label.canvas["fg_color"][0, i] = lerp_colors(
                    COLORS[char], BLACK, 0.33
                )

        new_design_button = AocButton("New Design", create_new_design, pos=(3, 0))

        towel_grid = GridLayout(pos=(2, 0), horizontal_spacing=2, is_transparent=True)
        towel_maker = AocText(size=(1, 12))

        def add_color_callback(name):
            def add_color():
                if len(self.current_towel) == 8:
                    return
                i = len(self.current_towel) + 3
                towel_maker.canvas["ord"][0, i] = ord(name)
                towel_maker.canvas["fg_color"][0, i] = COLORS[name]
                self.current_towel += name

            return add_color

        def reset_towel():
            self.current_towel = ""
            towel_maker.add_str(" : ........ ")
            towel_maker.canvas["fg_color"] = towel_maker.default_fg_color

        reset_towel()

        def create_towel_button_destroy_callback(towel):
            def destroy_callback():
                del self.towel_buttons[towel]
                towel_grid.grid_columns -= 1
                towel_grid.size = towel_grid.min_grid_size
                create_new_design()

            return destroy_callback

        def create_towel():
            if not self.current_towel or self.current_towel in self.towel_buttons:
                return

            towel_button = TowelButton(
                create_towel_button_destroy_callback(self.current_towel),
                design_label,
                size=(1, len(self.current_towel)),
            )
            for i, char in enumerate(self.current_towel):
                towel_button.canvas["ord"][0, i] = ord(char)
                towel_button.canvas["fg_color"][0, i] = COLORS[char]

            self.towel_buttons[self.current_towel] = towel_button

            towel_grid.add_gadget(towel_button)
            towel_grid.grid_columns += 1
            towel_grid.size = towel_grid.min_grid_size

            reset_towel()
            create_new_design()

        buttons = [
            ColorButton(name, color, add_color_callback(name))
            for name, color in COLORS.items()
        ]
        reset_towel_button = AocButton("Reset", reset_towel)
        create_towel_button = AocButton("Create", create_towel)

        level_label = AocText(size=(5, 10), size_hint={"width_hint": 1.0})

        color_grid = GridLayout(grid_columns=8, pos=(1, 0))
        color_grid.add_gadgets(
            *buttons, towel_maker, reset_towel_button, create_towel_button
        )
        color_grid.size = color_grid.min_grid_size

        self.add_gadgets(
            level_label, color_grid, towel_grid, new_design_button, design_label
        )

        while True:
            level_label.add_str(f"Level: {self.level}")
            await self.all_matched.wait()
            self.level += 1

            for gadget in self.root.children.copy():
                if isinstance(gadget, Towel):
                    gadget.destroy()

            while self.all_matched.is_set():
                hsv = cv2.cvtColor(design_label.canvas["fg_color"], cv2.COLOR_RGB2HSV)
                hsv[..., 0] += 5
                design_label.canvas["fg_color"] = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
                await asyncio.sleep(0.05)


LinenLayoutApp(
    title="Linen Layout", color_theme=AOC_THEME, inline=True, inline_height=5
).run()
