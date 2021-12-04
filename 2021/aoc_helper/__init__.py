import bs4
import re
import requests
import time
import webbrowser
import yaml
from typing import Callable

from .constants import *
from . import utils

__all__ = (
    "day",
    "submit",
    "utils",
)

TOKEN = {"session": TOKEN_FILE.read_text().strip()}

def day(d):
    """
    Return the input for day `d`. Inputs are cached.
    """
    d = str(d)

    inputs = yaml.full_load(INPUTS_FILE.read_text())

    if d in inputs:
        return inputs[d]

    response = requests.get(url=URL.format(day=d) + "/input", cookies=TOKEN)
    if not response.ok:
        raise ValueError("Request failed.")

    # Save input data
    inputs[d] = response.text.strip()
    INPUTS_FILE.write_text(yaml.dump(inputs, default_style="|"))
    return inputs[d]

def submit(day, solution: Callable):
    """
    Submit an AoC solution. Submissions are cached.
    """
    day = str(day)

    match solution.__name__:
        case "part_one":
            part = "1"
        case "part_two":
            part = "2"
        case _:
            raise ValueError(f"solution callable has bad name, {solution.__name__}")

    submissions = yaml.full_load(SUBMISSIONS_FILE.read_text())

    current = submissions.setdefault(day, {"1": {}, "2": {}})[part]

    if "solution" in current:
        print(
            f"Day {day} part {part} has already been solved. "
            f"The solution was:\n{current['solution']}"
        )
        return

    solution = solution()
    if solution is None:
        return

    solution = str(solution)

    if solution in current:
        print(f"Solution {solution} to part {part} has already been submitted, response was:")
        _pretty_print(current[solution])
        return

    while True:
        print(f"Submitting {solution} as solution to part {part}:")
        response = requests.post(
            url=URL.format(day=day) + "/answer",
            cookies=TOKEN,
            data={"level": part, "answer": solution}
        )

        if not response.ok:
            raise ValueError("Request failed.")

        message = bs4.BeautifulSoup(response.text, "html.parser").article.text
        _pretty_print(message)

        if message[4] == "g":  # "You gave an answer too recently"
            minutes, seconds = re.search(r"(?:(\d+)m )?(\d+)s", message).groups()

            timeout = 60 * int(minutes or 0) + int(seconds)
            print(f"Waiting {timeout} seconds to retry...")
            time.sleep(timeout)
        else:
            break

    if message[7] == "t":  # "That's the right answer! ..."
        current["solution"] = solution

        if part == "1":
            webbrowser.open(response.url)  # View part 2 in browser

    current[solution] = message
    SUBMISSIONS_FILE.write_text(yaml.dump(submissions))

def _pretty_print(message):
    match message[7]:
        case "t":
            # "That's the right answer! ..."
            COLOR = "\x1b[32m"  # Green
        case "'" | "e":
            # "You don't seem to be solving the right level. ..."
            # "You gave an answer too recently; you have to wait ..."
            COLOR = "\x1b[33m"  # Yellow
        case "n":
            # "That's not the right answer. If you're stuck, ..."
            COLOR = "\x1b[31m"  # Red
        case _:
            raise ValueError("Unexpected message.", message)
    print(
        "\x1b[1m",  # Bold
        COLOR,
        message,
        "\x1b[0m",  # Reset
        sep="",
    )
