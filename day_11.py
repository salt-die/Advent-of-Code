from robot import Robot
from display import array_from_dict
import matplotlib.pyplot as plt

with open('input11', 'r') as data:
    data = list(map(int, data.read().split(',')))

bad_robot = Robot(data=data)
bad_robot.start()
plt.imshow(array_from_dict(bad_robot.colors))
plt.show()
print(len(bad_robot.painted_locations)) # Part 1

good_robot = Robot(data=data, animate=True)
good_robot.colors[tuple(good_robot.location)] = 1
good_robot.start() # Part 2
