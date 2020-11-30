import json
import pathlib
import re
import requests
import time
import webbrowser
import bs4
import rich

YEAR = 2020
THIS_DIR = pathlib.Path(__file__).parent
TOKEN_FILE = ".token"  # Advent of Code session cookie
INPUTS_FILE = "inputs.json"
SUBMISSIONS_FILE = "submissions.json"
URL = f"https://adventofcode.com/{YEAR}/day/{{day}}"

with open(THIS_DIR / TOKEN_FILE) as f:
    token = {"session": f.read().strip()}

def day(d):
    """Return the input for day `d`. All inputs cached in INPUTS_FILE."""
    d = str(d)

    with open(THIS_DIR / INPUTS_FILE) as f:
        inputs = json.load(f)

    if d in inputs:
        return inputs[d]

    response = requests.get(url=URL.format(day=d) + "/input", cookies=token)
    if not response.ok:
        raise ValueError("Bad response")

    # Save input data
    inputs[d] = response.text
    with open(THIS_DIR / INPUTS_FILE, "w") as f:
        json.dump(inputs, f)

    return inputs[d]

def _pretty_print(color, message):
    rich.print(f"[bold {color}]{message}[/bold {color}]")

def submit(day, part, solution):
    """Submit an AoC solution.  Submissions are cached -- Submitting an already submitted solution will return the previous response."""
    day, part, solution = map(str, (day, part, solution))

    with open(THIS_DIR / SUBMISSIONS_FILE) as f:
        submissions = json.load(f)

    if day not in submissions:
        submissions[day] = {"1": {}, "2": {}}

    if solution in submissions[day][part]:
        rich.print(f"Solution {solution} to part {part} has already been submitted, response was:")
        return _pretty_print(*submissions[day][part][solution])

    rich.print(f"Submitting {solution} as solution to part {part}:")
    response = requests.post(url=URL.format(day=day) + "/answer", cookies=token, data={"level": part, "answer": solution})
    if not response.ok:
        raise ValueError("Bad response")

    message = bs4.BeautifulSoup(response.text, "html.parser").article.text
    color = None
    if "That's the right answer" in message:
        color = "green"
        if part.lower() == "a":
            webbrowser.open(response.url)  # View part b in browser
    elif "Did you already complete it" in message:
        color = "yellow"
    elif "That's not the right answer" in message:
        color = "red"
    elif "You gave an answer too recently" in message:
        wait_re = r"You have (?:(\d+)m )?(\d+)s left to wait"
        try:
            [(minutes, seconds)] = re.findall(wait_re, message)
        except ValueError as e:
            raise ValueError("Regex failed on message") from e
        else:
            pause = 60 * int(minutes or 0) + int(seconds)
            rich.print(f"Answer submitted recently, waiting {pause} seconds to retry...")
            time.sleep(pause)
            return submit(day, part, solution)

    submissions[day][part][solution] = color, message
    with open(THIS_DIR / SUBMISSIONS_FILE, "w") as f:
        json.dump(submissions, f)

    _pretty_print(color, message)
