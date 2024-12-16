from heapq import heappop, heappush

import aoc_lube
from aoc_lube.utils import extract_maze

MAZE = extract_maze(aoc_lube.fetch(year=2024, day=16))[1]
START, END = (139, 1), (1, 139)


def find_min_path():
    min_scores = {}
    best_seats = set()
    best_score = -1
    heap = [(0, START, (0, 1), [])]
    while heap:
        score, pos, dir, seats = heappop(heap)
        if pos == END:
            best_score = score
            best_seats.update(seats)
            continue

        for neighbor in MAZE[pos]:
            new_dir = (neighbor[0] - pos[0], neighbor[1] - pos[1])
            new_score = score + 1001 ** (new_dir != dir)
            if min_scores.setdefault((neighbor, new_dir), new_score) >= new_score:
                min_scores[neighbor, new_dir] = new_score
                heappush(heap, (new_score, neighbor, new_dir, seats + [pos]))

    return best_score, len(best_seats) + 1


def part_one():
    return find_min_path()[0]


def part_two():
    return find_min_path()[1]


aoc_lube.submit(year=2024, day=16, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=16, part=2, solution=part_two)
