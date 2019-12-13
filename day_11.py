from robot import Robot

with open('input11', 'r') as data:
    data = list(map(int, data.read().split(',')))

bad_robot = Robot(data=data, animate=True)
bad_robot.start()
print(len(bad_robot.painted_locations)) # Part 1

good_robot = Robot(data=data, animate=True)
good_robot.colors[tuple(good_robot.location)] = 1
good_robot.start() # Part 2
