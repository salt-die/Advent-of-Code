import bs4
import json
import re
import requests
import time
import webbrowser
from typing import Callable

from .constants import *

__all__ = (
    "day",
    "submit",
    "extract_ints",
    "extract_maze",
    "matching",
)

TOKEN = {"session": TOKEN_FILE.read_text().strip()}

def day(d):
    """
    Return the input for day `d`. Inputs are cached.
    """
    d = str(d)

    inputs = json.loads(INPUTS_FILE.read_text())

    if d in inputs:
        return inputs[d]

    response = requests.get(url=URL.format(day=d) + "/input", cookies=TOKEN)
    if not response.ok:
        raise ValueError("Bad response")

    # Save input data
    inputs[d] = response.text.strip()
    INPUTS_FILE.write_text(json.dumps(inputs, indent=2))
    return inputs[d]

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
            ValueError("Unexpected Response.")
    print(
        "\x1b[1m",  # Bold
        COLOR,
        message,
        "\x1b[0m",  # Reset
        sep="",
    )

def submit(day, solution: Callable):
    """
    Submit an AoC solution.

    Submissions are cached -- Submitting an already submitted solution will return the previous response.
    """
    day = str(day)

    match solution.__name__:
        case "part_one":
            part = "1"
        case "part_two":
            part = "2"
        case _:
            raise ValueError(f"solution callable has bad name, {solution.__name__}")

    submissions = json.loads(SUBMISSIONS_FILE.read_text())

    current = submissions.setdefault(day, {"1": {}, "2": {}})[part]

    if "solution" in current:
        print(
            f"Day {day} part {part} has already been solved."
            f"  The solution was: {current['solution']}."
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
            raise ValueError("Bad response")

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
    SUBMISSIONS_FILE.write_text(json.dumps(submissions, indent=2))

# Utilities
############

def extract_ints(raw):
    """
    Extract integers from a string.
    """
    return map(int, re.findall(r'(\d+)', raw))

def extract_maze(raw, empty_cell=".", largest_component=False):
    """
    Parse an ascii maze into a networkx graph.
    """
    maze = np.array(list(map(list, raw.splitlines())))

    import networkx as nx

    G = nx.grid_graph(maze.shape[::-1])

    walls = np.stack(np.where(maze != empty_cell)).T
    G.remove_nodes_from(map(tuple, walls))

    if largest_component:
        G.remove_nodes_from(G.nodes - max(nx.connected_components(G), key=lambda g: len(g)))

    return maze, G

def matching(items):
    """
    Return a maximum matching from a dict of lists.
    """
    import networkx as nx

    G = nx.from_dict_of_lists(items)

    return tuple(
        (k, v)
        for k, v in nx.bipartite.maximum_matching(G, top_nodes=items).items()
        if k in items
    )
