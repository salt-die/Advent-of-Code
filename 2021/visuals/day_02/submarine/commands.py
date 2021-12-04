import yaml
import re
from pathlib import Path

_THIS_DIR = Path(__file__).parent
_INPUTS = _THIS_DIR.parent.parent.parent / "aoc_helper" / "inputs.yaml"
_RAW = yaml.full_load(_INPUTS.read_text())["2"]

COMMANDS = [
    (command, int(amount))
    for command, amount in re.findall(r"(\w+) (\d+)", _RAW)
]
