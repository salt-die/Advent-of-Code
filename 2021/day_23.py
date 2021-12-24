from heapq import heappush, heappop
from typing import NamedTuple

import aoc_helper


class State(NamedTuple):
    rooms: tuple[tuple[str]]
    hallway: tuple[None | str]=(None,) * 11
    cost: int=0

    def __lt__(self, other: "State"):
        return self.cost < other.cost

ROOMS = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

COSTS = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

def tuple_replace(tup, index, item=None):
    return tuple(item if i == index else j for i, j in enumerate(tup))

def all_is_none(iterable):
    return all(i is None for i in iterable)

def shortest_path(*rooms):
    depth = len(rooms[0])
    goals = tuple((pod,) * depth for pod in "ABCD")

    STOPS = (0, 1, 3, 5, 7, 9, 10)
    queue = [ State(rooms) ]
    seen = set()

    while queue:
        rooms, hallway, cost = heappop(queue)

        if rooms == goals:
           return cost

        if (rooms, hallway) in seen:
            continue

        seen.add((rooms, hallway))

        # room to hallway
        for i, (room, goal) in enumerate(zip(rooms, goals)):
            if room == goal:
                continue

            for distance_to_hall, pod in enumerate(room):
                if pod:
                    break
            else:
                continue

            for stop in STOPS:
                room_index = 2 * (i + 1)
                start, end = sorted((room_index, stop))

                if all_is_none(hallway[start: end + 1]):
                    new_room = tuple_replace(room, distance_to_hall)
                    new_rooms = tuple_replace(rooms, i, new_room)
                    new_hallway = tuple_replace(hallway, stop, pod)
                    new_cost = cost + COSTS[pod] * (distance_to_hall + end - start + 1)

                    heappush(queue, State(new_rooms, new_hallway, new_cost))

        # hallway to room
        for stop in STOPS:
            if (pod := hallway[stop]) is None:
                continue

            pod_dest = ROOMS[pod]
            room_index = pod_dest // 2 - 1
            room = rooms[room_index]

            path = hallway[pod_dest: stop] if pod_dest < stop else hallway[stop + 1: pod_dest + 1]
            if all_is_none(path) and all(i in (None, pod) for i in room):
                for i, state in enumerate(room):
                    if state is not None:
                        i -= 1
                        break

                assert i != -1, "can't move to destination"

                new_room = tuple_replace(room, i, pod)
                new_rooms = tuple_replace(rooms, room_index, new_room)
                new_hallway = tuple_replace(hallway, stop)
                new_cost = cost + COSTS[pod] * (i + abs(pod_dest - stop) + 1)

                heappush(queue, State(new_rooms, new_hallway, new_cost))

def part_one():
    return shortest_path(
        ("C", "C"),
        ("A", "A"),
        ("B", "D"),
        ("D", "B"),
    )

def part_two():
    return shortest_path(
        ("C", "D", "D", "C"),
        ("A", "C", "B", "A"),
        ("B", "B", "A", "D"),
        ("D", "A", "C", "B"),
    )

aoc_helper.submit(23, part_one)
aoc_helper.submit(23, part_two)
