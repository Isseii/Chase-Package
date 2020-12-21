import random
import json
import csv
from sheep import Sheep
from wolf import Wolf

Sheep.init_pos_limit = 10.0
Sheep.sheep_move_dist = 0.5
Wolf.wolf_move_dist = 1.0
sheep_number = 15
rounds = 50

def __toJson(sheep_arr,wolf,data,i):
    sheeps_holder = []
    for j in range(len(sheep_arr)):
        pos = str(sheep_arr[j].xPos) + " " + str(sheep_arr[j].yPos)
        sheeps_holder.append(pos)
    pos = str(round(wolf.xPos, 3)) + " " + str(round(wolf.yPos, 3))
    data['lea'].append({'round_no': i,
                        'wolf_pos' : pos,
                        'sheep_pos' : sheeps_holder})
    return data

def __toCsv(sheeps):
    with open('alive.csv.', 'w' , newline='') as  csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, )
        writer.writerow(['Round','Alive_Sheeps'])
        round = 0
        for s in sheeps:
            writer.writerow([round , s])
            round += 1




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
    data = {}
    sheeps_alive = []
    data['lea'] = []
    __toJson(sheep_arr, wolf, data, 0)
    sheeps_alive.append(sheep_number)
    for i in range(rounds):
        print("Round : ", i)
        for j in range(len(sheep_arr)):
            sheep_arr[j].move()
            pos = str(sheep_arr[j].xPos) + " " + str(sheep_arr[j].yPos)
        wolf.move(sheep_arr)
        pos = str(wolf.xPos) + " " + str(wolf.yPos)
        print("Wolf Position  X : ", round(wolf.xPos, 3), ", Y :", round(wolf.yPos, 3))
        if wolf.killed_sheep != -1:
            print("Wolf killed sheep number ", wolf.killed_sheep)
        print("Number of alive sheeps ", wolf.alive_sheeps)
        __toJson(sheep_arr,wolf,data,i+1)
        sheeps_alive.append(wolf.alive_sheeps)

    __toCsv(sheeps_alive)
    with open('pos.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)



