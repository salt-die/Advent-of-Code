from io import StringIO
from pathlib import Path

import numpy as np
import yaml

_THIS_DIR = Path(__file__).parent
_INPUTS = _THIS_DIR.parent.parent.parent / "aoc_helper" / "inputs.yaml"
_RAW = yaml.full_load(_INPUTS.read_text())["4"]

def parse_raw():
    numbers, cards = _RAW.split("\n\n", 1)

    return (
        tuple(map(int, numbers.split(","))),
        np.loadtxt(StringIO(cards), dtype=int).reshape(-1, 5, 5),
    )

NUMBERS, CARDS = parse_raw()
