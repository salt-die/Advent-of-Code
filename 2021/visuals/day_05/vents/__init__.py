import re
from math import copysign
from pathlib import Path

import cv2
import numpy as np
import yaml

_THIS_DIR = Path(__file__).parent
_INPUTS = _THIS_DIR.parent.parent.parent / "aoc_helper" / "inputs.yaml"
_RAW = yaml.full_load(_INPUTS.read_text())["5"]

VENTS = np.zeros((2, 1000, 1000), dtype=float)
VENT_SCALE = .2

for match in re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", _RAW):
    a, b, c ,d = map(int, match)

    if a != c:
        VENTS[1] += cv2.line(
            np.zeros_like(VENTS[0]),
            (a, b),
            (c, d),
            copysign(1, c - a),
            thickness=2,
        )

    if b != d:
        VENTS[0] += cv2.line(
            np.zeros_like(VENTS[0]),
            (a, b),
            (c, d),
            copysign(1, d - b),
            thickness=2,
        )

if not Path("vents.png").exists():
    mask = VENTS < 0
    VENTS[mask] *= -1
    cv2.imwrite(
        "vents.png",
        np.dstack((VENTS.sum(0).astype(int) * 50,) * 3),
    )
    VENTS[mask] *= -1

VENTS *= VENT_SCALE
