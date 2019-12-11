from robot import Robot

with open('input11', 'r') as data:
    data = list(map(int, data.read().split(',')))

bad_robot = Robot(data=data)
bad_robot.start()
print(len(bad_robot.painted_locations)) # Part 1

good_robot = Robot(data=data, animate=False)
good_robot.colors[tuple(good_robot.location)] = 1
good_robot.start()

import matplotlib.pyplot as plt
import numpy as np
# Construct picture from dictionary
height = max(good_robot.colors)[0] + 1
width = max(good_robot.colors, key=lambda tup:tup[1])[1] + 1

registration_identifier = np.zeros([height, width])
for location, color in good_robot.colors.items():
    registration_identifier[location] = color

plt.imshow(registration_identifier) # Part 2

#If animating:
#import imageio
#import os
#frames = [imageio.imread(os.path.join('frames/', file))
#          for file in sorted(os.listdir('frames/'))]
#frames[-1:] += frames[-1:] * 40 # Show last frame for longer duration
#imageio.mimsave('frames/langtons_robot.gif', frames, duration=.05)