from maze_solver import Robot

with open('input15', 'r') as data:
    data = list(map(int, data.read().split(',')))

Robot(data=data).start()