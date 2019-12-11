from numpy import arctan2, pi, array
from numpy.linalg import norm

with open('input10', 'r') as data:
    asteroids = [(x, y) for y, line in enumerate(data.readlines())
                        for x, character in enumerate(line) if character == '#']

def angle(u, v):
    (x1, y1), (x2, y2) = u, v
    # Note y's are inverted; angles changed from (-pi, pi) to (0, 2 * pi)
    return arctan2(x2 - x1, y1 - y2) % (2 * pi)

def unique_lines(asteroid):
    return len(set(angle(asteroid, other) for other in asteroids))

number_visible, laser_base = max((unique_lines(asteroid), asteroid) for asteroid in asteroids)
print(number_visible) # Part 1

asteroids.remove(laser_base)
asteroids.sort(key=lambda asteroid: norm(array(asteroid) - laser_base))
rank = {asteroid : sum(angle(laser_base, asteroid) == angle(laser_base, other)
                       for other in asteroids[:i])
        for i, asteroid in enumerate(asteroids)}
x, y = sorted(asteroids, key=lambda asteroid: (rank[asteroid], angle(laser_base, asteroid)))[199]
print(x * 100 + y) # Part 2