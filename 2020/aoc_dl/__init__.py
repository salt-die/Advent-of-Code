import json
import pathlib
import requests

__all__ = "day"

THIS_DIR = pathlib.Path(__file__).parent
TOKEN_FILE = ".token"  # Advent of Code session id
INPUTS_FILE = "inputs.json"
URL = "https://adventofcode.com/2020/day/{day}/input"  # Reminder to future self:  Change the year!
USER_AGENT = {"User-Agent": "aoc-dl"}

with open(THIS_DIR / TOKEN_FILE) as f:
    token = {"session": f.read().strip()}

def day(d):
    """Return the input for day `d`. All inputs cached in INPUTS_FILE."""
    d = str(d)

    with open(THIS_DIR / INPUTS_FILE) as f:
        inputs = json.load(f)

    if d in inputs:
        return inputs[d]

    response = requests.get(url=URL.format(day=d), cookies=token, headers=USER_AGENT)
    if not response.ok:
        raise ValueError("Bad response")

    # Save input data
    inputs[d] = response.text
    with open(THIS_DIR / INPUTS_FILE, "w") as f:
        json.dump(inputs, f)

    return inputs[d]
