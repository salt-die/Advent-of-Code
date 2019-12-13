from arcade import Arcade

with open('input13', 'r') as data:
    data = list(map(int, data.read().split(',')))

arcade = Arcade()
arcade << data
arcade()
print((arcade.pixels == 2).sum())

arcade(quarters=2)
print(arcade.score)
