from arcade import Arcade

with open('input13', 'r') as data:
    data = list(map(int, data.read().split(',')))

arcade = Arcade()
arcade << data
arcade.start()

print(sum(value == 2 for value in arcade.pixels.values()))

arcade.start(quarters=2)
print(arcade.score)
