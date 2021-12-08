import re
from pathlib import Path

import yaml

_THIS_DIR = Path(__file__).parent
_ASSETS = _THIS_DIR.parent / "assets"
_INPUTS = _THIS_DIR.parent.parent.parent / "aoc_helper" / "inputs.yaml"
_RAW = yaml.full_load(_INPUTS.read_text())["8"]
_DIGIT_RE = re.compile(r"[a-g]+")

DATA = [_DIGIT_RE.findall(line) for line in _RAW.splitlines()]
COMPUTER_FRAMES = _ASSETS / "computer"
SONAR_FRAMES = _ASSETS / "sonar"
