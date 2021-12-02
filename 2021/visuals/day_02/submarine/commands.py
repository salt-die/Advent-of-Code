import json
import re
from pathlib import Path

_THIS_DIR = Path(__file__).parent
_INPUTS = _THIS_DIR.parent.parent.parent / "aoc_helper" / "inputs.json"
_RAW = json.loads(_INPUTS.read_text())["2"]

COMMANDS = re.findall(r"(\w+) (\d+)", _RAW)
