import aoc_lube

DISK = list(map(int, aoc_lube.fetch(year=2024, day=9)))


def get_memory():
    used, free = [], []
    pos = 0
    for i, size in enumerate(DISK):
        (free if i % 2 else used).append([pos, size, i // 2])
        pos += size
    return used, free


def triangular_sum(pos, size):
    return pos * size + (size * (size - 1) // 2)


def checksum(used):
    return sum(file_id * triangular_sum(pos, size) for pos, size, file_id in used)


def move(free_info, file_info):
    file_info[0] = free_info[0]
    free_info[0] += file_info[1]
    free_info[1] -= file_info[1]


def part_one():
    used, free = get_memory()
    files = reversed(used)
    file_info = next(files)
    fragged = []
    for free_info in free:
        if free_info[0] > file_info[0]:
            break
        while free_info[1] >= file_info[1]:
            move(free_info, file_info)
            file_info = next(files)
        if free_info[1] > 0:
            free_info[2] = file_info[2]
            fragged.append(free_info[:])
            file_info[1] -= free_info[1]
            free_info[1] = 0
    return checksum(used) + checksum(fragged)


def part_two():
    used, free = get_memory()
    for file_info in reversed(used):
        for free_info in free:
            if free_info[0] > file_info[0]:
                break
            if free_info[1] >= file_info[1]:
                move(free_info, file_info)
                break
    return checksum(used)


aoc_lube.submit(year=2024, day=9, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=9, part=2, solution=part_two)
