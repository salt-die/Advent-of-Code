import asyncio

import aoc_lube
from aoc_lube.utils import extract_ints
from aoc_theme import AOC_THEME, AocText
from batgrl.app import App
from batgrl.colors import Color
from batgrl.gadgets._cursor import Cursor

YELLOW = Color.from_hex("e5da0d")
GREEN = Color.from_hex("22cc39")
RED = Color.from_hex("dd3330")
A, _, _, *CODE = extract_ints(aoc_lube.fetch(year=2024, day=17))

OPNAMES = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
DELAY = 0.005


async def run_program(a, display, instruction):
    display.clear()
    display.add_str(f"{CODE} -> []")
    display.add_str(
        "    INSTRUCTION    ┃         A         ┃         B         ┃         C         ",
        pos=(2, 0),
    )
    display.add_str(
        "━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━",
        pos=(3, 0),
    )
    display.canvas["char"][4:, [19, 39, 59]] = "┃"

    instruction.pos = (0, 1)

    A, B, C = a, 0, 0

    def combo(operand):
        return (
            operand if operand <= 3 else A if operand == 4 else B if operand == 5 else C
        )

    pointer = 0
    out = []
    while pointer < len(CODE):
        if pointer < len(CODE):
            await instruction.tween(
                x=3 * pointer + 1, duration=DELAY * 5, easing="out_quint"
            )

        opcode, operand = CODE[pointer : pointer + 2]
        match opcode:
            case 0:  # adv
                A = A >> combo(operand)
            case 1:  # bxl
                B ^= operand
            case 2:  # bst
                B = combo(operand) % 8
            case 3:  # jnz
                if A:
                    pointer = operand - 2
            case 4:  # bxc
                B ^= C
            case 5:  # out
                out.append(combo(operand) % 8)
            case 6:  # bdv
                B = A >> combo(operand)
            case 7:  # cdv
                C = A >> combo(operand)

        pointer += 2
        if opcode == 5:
            display.add_str(f"{CODE} -> {out}")
        display.canvas["char"][5:] = display.canvas["char"][4:-1]
        display.canvas["char"][4] = " "
        display.canvas["char"][4, [19, 39, 59]] = "┃"
        display.add_str(
            (
                f"{f'{OPNAMES[opcode]}({operand})':^19}┃{oct(A):^19}┃{oct(B):^19}┃{oct(C):^19}"
            ),
            pos=(4, 0),
        )
        await asyncio.sleep(DELAY)
    return out


async def solve(solver, display, instruction):
    global DELAY
    DELAY = 0.05
    cursor = solver.children[0]
    cursor.x = 10
    possible = [0]
    for i in range(len(CODE)):
        solver.clear()
        solver.add_str(
            f"Possible: {', '.join(oct(n) for n in possible)}", truncate_str=True
        )
        solver.add_str("Match:".ljust(100), pos=(2, 0))

        new_possible = []
        cursor.width = len(oct(possible[0]))

        for j, n in enumerate(possible):
            await cursor.tween(
                x=j * (cursor.width + 2) + 10, duration=DELAY * 5, easing="out_quint"
            )

            for a in range(8):
                solver.add_str(f"Testing: {oct(n * 8)} + {a}", pos=(1, 0))
                if CODE[-i - 1 :] == await run_program(n * 8 + a, display, instruction):
                    new_possible.append(n * 8 + a)
                    solver.add_str(
                        f"Match: {', '.join(oct(n) for n in new_possible)}",
                        pos=(2, 0),
                        truncate_str=True,
                    )
        possible = new_possible
        DELAY *= 0.5
    return possible[0]


class ChronospatialComputerApp(App):
    async def on_start(self):
        cursor = Cursor(fg_color=RED)
        cursor.size = (1, 4)
        cursor.is_enabled = True

        instruction = AocText(is_transparent=True, alpha=0)
        instruction.set_text("\n▔  ▔")
        instruction.bind("pos", lambda: setattr(cursor, "x", instruction.x))

        display = AocText(size=(9, 100))
        display.add_gadgets(cursor, instruction)

        cursor_2 = Cursor(fg_color=GREEN)
        cursor_2.is_enabled = True
        solver = AocText(size=(3, 100), pos=(9, 0))
        solver.add_gadget(cursor_2)

        self.add_gadgets(display, solver)
        cursor.bg_color = display.default_bg_color
        cursor_2.bg_color = solver.default_bg_color

        await solve(solver, display, instruction)


ChronospatialComputerApp(
    title="Chronospatial Computer",
    color_theme=AOC_THEME,
    inline=True,
    inline_height=12,
).run()
