import re
from itertools import cycle
from pathlib import Path

import numpy as np
import yaml

from nurses_2.colors import AColor, color_pair, gradient, AWHITE

def _parse_raw():
    this_dir = Path(__file__).parent
    inputs = this_dir.parent.parent.parent / "aoc_helper" / "inputs.yaml"
    raw = yaml.full_load(inputs.read_text())["13"]

    points, _instructions = raw.split("\n\n")

    paper = np.zeros((895, 1311), dtype=bool)
    for x, y in re.findall(r"(\d+),(\d+)", points):
        paper[int(y), int(x)] = 1

    instructions = re.findall(r"fold along ([xy])=\d+", _instructions)

    return paper, instructions

PAPER, INSTRUCTIONS = _parse_raw()

NAVY_BLUE = AColor.from_hex("0F0F23")
STAR_YELLOW = AColor.from_hex("F2F762")

YELLOW_ON_BLUE = color_pair(STAR_YELLOW, NAVY_BLUE)
YELLOW_TO_WHITE = cycle(gradient(STAR_YELLOW, AWHITE, 30) + gradient(AWHITE, STAR_YELLOW, 30))
