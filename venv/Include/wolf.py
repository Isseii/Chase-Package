import math
from direction import Direction


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def length(x,y):
    return math.sqrt(x * x  + y * y)

class Wolf:
    init_pos_limit = float()
    wolf_move_dist = float()
    alive_sheeps = 0
    killed_sheep = -1


    def __init__(self):
        self.xPos = 0.0
        self.yPos = 0.0

    def move(self, sheep: list):
        self.alive_sheeps = len(sheep)
        if self.__get_closest_sheep_xy(sheep) == -1:
            return
        closestSheep, closest_distance = self.__get_closest_sheep_xy(sheep)
        index = sheep.index(closestSheep)
        self.xPos, self.yPos, wolf_distance = self.__go_towards( closestSheep, index)


    def __go_towards(self, sheep, index):
        csx = sheep.xPos
        csy = sheep.yPos
        dist = distance(self.xPos, self.yPos, csx, csy)
        x = float()
        y = float()
        if dist <= self.wolf_move_dist:
            x, y = csx, csy
            self.alive_sheeps -= 1
            self.killed_sheep = index
            sheep.kill()
        else:
            directX = csx - self.xPos
            directY = csy - self.yPos
            directX, directY = directX/dist, directY/dist
            x = self.xPos + directX
            y = self.yPos + directY
        dist = distance(x, y, csx, csy)
        return x, y, dist

    def __get_closest_sheep_xy(self, sheeps: list):
        index = -1
        self.alive_sheeps = 0
        self.killed_sheep = -1
        for s in sheeps:
            if s.isAlive():
                self.alive_sheeps += 1
                index = sheeps.index(s)
        if self.alive_sheeps == 0:
            return -1
        closest = sheeps[index]
        closest_distance = 0


        for s in sheeps:
            if s.isAlive():
                closest_distance = distance(self.xPos, self.yPos, closest.xPos, closest.yPos)
                sheep_distance = distance(self.xPos, self.yPos, s.xPos, s.yPos)
                if closest_distance > sheep_distance:
                    closest = s
                    closest_distance = sheep_distance
        return closest, closest_distance
