import random
from sheep import Sheep
from wolf import Wolf

Sheep.init_pos_limit = 10.0
Sheep.sheep_move_dist = 0.5
sheep_number = 15
rounds = 50


def __generate_sheeps(no):
    sheep_arr = []
    for i in range(0, no):
        posx = (random.randrange(-(2 * Sheep.init_pos_limit), (2 * Sheep.init_pos_limit) + 1, 1)) / 2
        posy = (random.randrange(-(2 * Sheep.init_pos_limit), (2 * Sheep.init_pos_limit) + 1, 1)) / 2
        sheep_arr.append(Sheep(posx, posy))
    return sheep_arr


if __name__ == "__main__":
    sheep_arr = __generate_sheeps(sheep_number)
    wolf = Wolf()

    for i in range(rounds):
        for j in range(len(sheep_arr)):
            print(i, j, sheep_arr[j].position())
            sheep_arr[j].move()
            wolf.move(sheep_arr)
