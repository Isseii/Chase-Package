import random
from sheep import Sheep


Sheep.init_pos_limit = 10.0
Sheep.sheep_move_dist = 0.5
sheeps_number = 15
rounds = 50
sheep_arr = []



for i in range(0,sheeps_number):
    posx = (random.randrange(-(2*Sheep.init_pos_limit), (2*Sheep.init_pos_limit)+1, 1))/2
    posy = (random.randrange(-(2*Sheep.init_pos_limit), (2*Sheep.init_pos_limit)+1, 1))/2
    sheep_arr.append(Sheep(posx,posy))

for i in range(rounds):
    for x in range(len(sheep_arr)):
        print(i, x , sheep_arr[x].position())
        sheep_arr[x].move()

