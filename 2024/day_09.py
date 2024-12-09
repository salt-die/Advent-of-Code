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


def part_one():
    used, free = get_memory()
    fragged = []
    for free_info in free:
        file_info = used[-1]
        if free_info[0] > file_info[0]:
            break
        while free_info[1] >= file_info[1]:
            file_info[0] = free_info[0]
            free_info[0] += file_info[1]
            free_info[1] -= file_info[1]
            fragged.append(used.pop())
            file_info = used[-1]

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
                file_info[0] = free_info[0]
                free_info[0] += file_info[1]
                free_info[1] -= file_info[1]
                break

    return checksum(used)


print(part_one(), part_two())
aoc_lube.submit(year=2024, day=9, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=9, part=2, solution=part_two)
