from typing import Literal

from aoc_theme import AOC_THEME, AocButton, AocText
from batgrl.app import App
from batgrl.colors import WHITE, Color, lerp_colors
from batgrl.gadgets.behaviors.grabbable import Grabbable
from batgrl.gadgets.behaviors.movable import Movable
from batgrl.gadgets.behaviors.toggle_button_behavior import ToggleButtonBehavior
from batgrl.gadgets.grid_layout import GridLayout

GREEN = Color.from_hex("22cc39")
RED = Color.from_hex("dd3330")


def line_char(dy, dx, turn):
    if dy == 0:
        return "─"
    if dx == 0:
        return "│"
    if dx > 0:
        if dy > 0:
            return "╰╮"[turn]
        return "╭╯"[turn]
    if dy > 0:
        return "╯╭"[turn]
    return "╮╰"[turn]


def draw_path(start, end, color, cells):
    h, w = cells.shape
    cy, cx = start
    ey, ex = end
    dy = (ey > cy) - (cy > ey)
    dx = (ex > cx) - (cx > ex)
    ty = cy + (ey - cy) // 2
    while cy != ty:
        cy += dy
        if 0 <= cy < h and 0 <= cx < w:
            cells[cy, cx]["char"] = "│"
            cells[cy, cx]["fg_color"] = color
    if 0 <= cy < h and 0 <= cx < w:
        cells[cy, cx]["char"] = line_char(dy, dx, 0)
    while cx != ex:
        cx += dx
        if 0 <= cy < h and 0 <= cx < w:
            cells[cy, cx]["char"] = "─"
            cells[cy, cx]["fg_color"] = color
    if 0 <= cy < h and 0 <= cx < w:
        cells[cy, cx]["char"] = line_char(dy, dx, 1)
    while cy != ey:
        cy += dy
        if 0 <= cy < h and 0 <= cx < w:
            cells[cy, cx]["char"] = "│"
            cells[cy, cx]["fg_color"] = color


class Connector(Grabbable, AocText):
    ins = []
    outs = []

    def __init__(self, kind: Literal["in", "out"] = "out", **kwargs):
        super().__init__(**kwargs)
        self.circuit_board = None
        self.in_ = None
        self.out = None
        self.kind = kind
        self.set_text("┴" if kind == "in" else "┬")

    def on_add(self):
        super().on_add()
        self.circuit_board: CircuitBoard = self.parent.parent
        if self.kind == "in":
            self.ins.append(self)
        else:
            self.outs.append(self)

    def on_remove(self):
        super().on_remove()
        self.disconnect()
        if self.kind == "in":
            self.ins.remove(self)
        else:
            self.outs.remove(self)
        self.circuit_board.update_connections()

    def grab(self, mouse_event):
        self.disconnect()
        super().grab(mouse_event)

    def grab_update(self, mouse_event):
        self.circuit_board.clear()
        draw_path(
            self.absolute_pos,
            mouse_event.pos,
            self.default_fg_color,
            self.circuit_board.canvas,
        )

    def ungrab(self, mouse_event):
        self.circuit_board.clear()
        if self.kind == "in":
            others = self.outs
        else:
            others = self.ins
        if others:

            def manhattan_distance(a):
                y, x = mouse_event.pos - a.absolute_pos
                return abs(y) + abs(x)

            closest = min(others, key=manhattan_distance)
            if manhattan_distance(closest) < 3:
                self.connect(closest)
        return super().ungrab(mouse_event)

    def connect(self, other):
        if self.kind == "in":
            other.out = self
            self.in_ = other
        else:
            other.in_ = self
            self.out = other
        self.circuit_board.update_connections()

    def disconnect(self):
        if self.in_ is None and self.out is None:
            return

        if self.kind == "in":
            self.in_.out = None
            self.in_ = None
        else:
            self.out.in_ = None
            self.out = None
        self.circuit_board.update_connections()


class InputToggle(ToggleButtonBehavior, AocText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = 3, 5
        self.pos = 1, 1

    def update_normal(self):
        if self.toggle_state == "on":
            self.update_on()
        else:
            self.update_off()

    def update_hover(self):
        color = GREEN if self.toggle_state == "on" else RED
        self.canvas["bg_color"] = lerp_colors(color, WHITE, 0.5)

    def update_on(self):
        self.canvas["bg_color"] = GREEN
        self.canvas["char"][1, 2] = "1"

    def update_off(self):
        self.canvas["bg_color"] = RED
        self.canvas["char"][1, 2] = "0"

    def on_toggle(self):
        super().on_toggle()
        self.parent.parent.update_connections()


class Component(Movable, AocText):
    state: Literal["on", "off", "disabled"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_text("┌─────┐\n│     │\n│     │\n│     │\n└─────┘")
        self.ptf_on_grab = True
        self.circuit_board = None

    def on_add(self):
        self.circuit_board = self.parent
        self._bind = self.bind("pos", lambda: self.circuit_board.update_connections())
        super().on_add()

    def on_mouse(self, mouse_event):
        if (
            mouse_event.button == "right"
            and mouse_event.event_type == "mouse_down"
            and self.collides_point(mouse_event.pos)
        ):
            self.destroy()
            return True
        return super().on_mouse(mouse_event)


class Input(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.toggle = InputToggle()
        self.out_a = Connector(pos=(4, 2))
        self.out_b = Connector(pos=(4, 4))
        self.add_gadgets(self.toggle, self.out_a, self.out_b)

        # ToggleButton may go to hover state when moving input because
        # ToggleButton.on_mouse will be called before Input.on_mouse.
        # Reset ToggleButton to normal state on move:
        self.bind("pos", lambda: setattr(self.toggle, "button_state", "normal"))

    @property
    def state(self):
        return self.toggle.toggle_state


class Output(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.in_ = Connector(pos=(0, 3), kind="in")
        self.add_gadgets(self.in_)

    @property
    def state(self):
        if self.in_.in_ is None:
            return "disabled"

        return self.in_.in_.parent.state


class Gate(Component):
    def __init__(self, kind: Literal["XOR", "OR", "AND"], **kwargs):
        super().__init__(**kwargs)
        self.kind = kind
        self.add_str(kind, pos=(2, 2))
        self.in_a = Connector(pos=(0, 2), kind="in")
        self.in_b = Connector(pos=(0, 4), kind="in")
        self.out_a = Connector(pos=(4, 2))
        self.out_b = Connector(pos=(4, 4))
        self.add_gadgets(self.in_a, self.in_b, self.out_a, self.out_b)

    @property
    def state(self):
        if self.in_a.in_ is None or self.in_b.in_ is None:
            return "disabled"
        if self.in_a.in_.parent.state == "disabled":
            return "disabled"
        if self.in_b.in_.parent.state == "disabled":
            return "disabled"
        a = self.in_a.in_.parent.state == "on"
        b = self.in_b.in_.parent.state == "on"
        if self.kind == "XOR":
            result = a ^ b
        elif self.kind == "OR":
            result = a or b
        else:
            result = a and b
        return "on" if result else "off"


class CircuitBoard(AocText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._connections = AocText(
            size_hint={"height_hint": 1.0, "width_hint": 1.0}, is_transparent=True
        )
        self.add_gadget(self._connections)

    def update_connections(self):
        self._connections.clear()
        for descendent in self.walk():
            if (
                isinstance(descendent, Connector)
                and descendent.kind == "out"
                and descendent.out is not None
            ):
                color = (
                    GREEN
                    if descendent.parent.state == "on"
                    else RED
                    if descendent.parent.state == "off"
                    else descendent.default_fg_color
                )
                draw_path(
                    descendent.absolute_pos,
                    descendent.out.absolute_pos,
                    color,
                    self._connections.canvas,
                )
            elif isinstance(descendent, (Gate, Output)):
                descendent.canvas["bg_color"][1:-1, 1:-1] = (
                    descendent.default_bg_color
                    if descendent.state == "disabled"
                    else RED
                    if descendent.state == "off"
                    else GREEN
                )
                if isinstance(descendent, Output):
                    descendent.canvas["char"][2, 3] = (
                        "0"
                        if descendent.state == "off"
                        else "1"
                        if descendent.state == "on"
                        else " "
                    )


class CrossedWiresApp(App):
    async def on_start(self):
        circuit_board = CircuitBoard(size_hint={"height_hint": 1.0, "width_hint": 1.0})

        def create_callback(gadget_type):
            def callback():
                circuit_board.add_gadget(gadget_type())

            return callback

        add_input = AocButton("IN", create_callback(Input))
        add_output = AocButton("OUT", create_callback(Output))
        add_xor = AocButton("XOR", create_callback(lambda: Gate("XOR")))
        add_and = AocButton("AND", create_callback(lambda: Gate("AND")))
        add_or = AocButton("OR", create_callback(lambda: Gate("OR")))
        grid_layout = GridLayout(grid_columns=5)
        grid_layout.add_gadgets(add_input, add_output, add_xor, add_and, add_or)
        grid_layout.size = grid_layout.min_grid_size
        circuit_board.add_gadget(grid_layout)
        self.add_gadget(circuit_board)


CrossedWiresApp(title="Crossed Wires", color_theme=AOC_THEME).run()
