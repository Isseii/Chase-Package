import random
from sheep import Sheep

Sheep.init_pos_limit = 10.0
Sheep.sheep_move_dist = 0.5
sheeps_number = 15
rounds = 50


def __generate_sheeps(no):
    for i in range(0, no):
        posx = (random.randrange(-(2 * Sheep.init_pos_limit), (2 * Sheep.init_pos_limit) + 1, 1)) / 2
        posy = (random.randrange(-(2 * Sheep.init_pos_limit), (2 * Sheep.init_pos_limit) + 1, 1)) / 2
        sheep_arr.append(Sheep(posx, posy))


if __name__ == "__main__":
    __generate_sheeps(sheeps_number)

    sheep_arr = []
    for i in range(rounds):
        for j in range(len(sheep_arr)):
            print(i, j, sheep_arr[j].position())
            sheep_arr[j].move()
