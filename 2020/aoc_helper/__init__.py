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
    inputs[d] = response.text.strip()
    with open(THIS_DIR / INPUTS_FILE, "w") as f:
        json.dump(inputs, f, indent=2)

    return inputs[d]

def _pretty_print(message):
    # The first place the message differs between right and wrong answers is index 7; we differentiate messages with this index.
    #   "green" indicates a correct answer
    #   "yellow" indicates a submission to an already solved problem
    #   "red" indicates a timeout or wrong answer
    color = {"t": "green", "'": "yellow"}.get(message[7], "red")
    rich.print(f"[bold {color}]{message}[/bold {color}]")

def submit(day, solv_func):
    """Submit an AoC solution.  Submissions are cached -- Submitting an already submitted solution will return the previous response.
       solv_func is expected to be named "part_one" or "part_two"; the function is passed instead of the answer as we only run it in
       cases where we haven't seen a solution yet.  (To save time running slow part_one funcs in cases where we run solution files
       multiple times working on part two.)

       Possible responses to submissions start with:
            "That's the right answer! ..."
            "You don't seem to be solving the right level. ..."
            "That's not the right answer. If you're stuck, ..."
            "You gave an answer too recently; you have to wait ..."
    """
    day = str(day)
    part = "1" if solv_func.__name__ == "part_one" else "2"

    with open(THIS_DIR / SUBMISSIONS_FILE) as f:
        submissions = json.load(f)

    if day not in submissions:
        submissions[day] = {"1": {}, "2": {}}

    # We won't run the function if we already have the solution.
    # If solv_func is slow this can save us time when running solution files multiple times.
    if "solution" in submissions[day][part]:
        return rich.print(f"Day {day} part {part} has already been solved.  The solution was: {submissions[day][part]['solution']}.")

    if (solution :=  solv_func()) is None:  # Our templated code when run will submit empty solutions.  Ignore these.
        return
    solution = str(solution)

    if solution in submissions[day][part]:
        rich.print(f"Solution {solution} to part {part} has already been submitted, response was:")
        return _pretty_print(submissions[day][part][solution])

    while True:
        rich.print(f"Submitting {solution} as solution to part {part}:")
        response = requests.post(url=URL.format(day=day) + "/answer", cookies=token, data={"level": part, "answer": solution})
        if not response.ok:
            raise ValueError("Bad response")

        message = bs4.BeautifulSoup(response.text, "html.parser").article.text

        if message[4] == "g":  # This rather esoteric check is really asking, "Is this the message 'You gave an answer too recently;...'?"
            _pretty_print(message)
            minutes, seconds = re.search(r"(?:(\d+)m )?(\d+)s", message).groups()

            pause = 60 * int(minutes or 0) + int(seconds)
            rich.print(f"Waiting {pause} seconds to retry...")
            time.sleep(pause)
        else:
            break

    if message[7] == "t":  # Correct Solution:  We mark this part as solved by adding key `"solution"`.
        submissions[day][part]["solution"] = solution
        if part == "1": webbrowser.open(response.url)  # View part 2 in browser

    submissions[day][part][solution] = message
    with open(THIS_DIR / SUBMISSIONS_FILE, "w") as f:
        json.dump(submissions, f, indent=2)

    _pretty_print(message)

def extract_ints(raw):
    """Utility function to extract all integers from some string."""
    return map(int, re.findall(r'(\d+)', raw))

def extract_maze(raw, empty_cell=".", largest_component=False):
    """Utility function to parse an ascii maze into a networkx graph."""
    maze = np.array(list(map(list, raw.splitlines())))

    import networkx as nx
    G = nx.grid_graph(maze.shape[::-1])
    walls = np.stack(np.where(maze != empty_cell)).T
    G.remove_nodes_from(map(tuple, walls))
    if largest_component:
        G.remove_nodes_from(G.nodes - max(nx.connected_components(G), key=lambda g: len(g)))
    return maze, G