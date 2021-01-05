import math
from chase.direction import Direction


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def length(x, y):
    return math.sqrt(x * x + y * y)


class Wolf:
    init_pos_limit = float()
    wolf_move_dist = float()
    alive_sheeps = 0
    killed_sheep = -1

    def __init__(self, logging):
        self.xPos = 0.0
        self.yPos = 0.0
        self.logging = logging

        self.logging.debug(
            "Wolf constructor called with argument(" + self.__str__() + "," +  logging.__str__() + ")")

    def move(self, sheep: list):
        self.alive_sheeps = len(sheep)
        closestSheep, closest_distance = self.__get_closest_sheep_xy(sheep)
        if closest_distance == -1:
            return
        index = sheep.index(closestSheep)
        self.xPos, self.yPos, wolf_distance = self.__go_towards( closestSheep, index)
        self.logging.debug("move called with argument("+ self.__str__() +"," + sheep.__str__() +")")



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
        self.logging.debug(
            "__go_towards called with argument(" + self.__str__() +"," + sheep.__str__() + "," + index.__str__() +
            "), returned (" + x.__str__() + "," + y.__str__() + "," + dist.__str__() )
        return x, y, dist

    def __get_closest_sheep_xy(self, sheeps: list):
        index = -1
        self.alive_sheeps = 0
        self.killed_sheep = -1
        alive_sheeps = []
        for s in sheeps:
            if s.isAlive():
                self.alive_sheeps += 1
                index = sheeps.index(s)
                alive_sheeps.append(s)
        if self.alive_sheeps == 0:
            return -1, -1
        closest = sheeps[index]
        closest_distance = 0
        for s in alive_sheeps:
            closest_distance = distance(self.xPos, self.yPos, closest.xPos, closest.yPos)
            sheep_distance = distance(self.xPos, self.yPos, s.xPos, s.yPos)
            if closest_distance > sheep_distance:
                closest = s
                closest_distance = sheep_distance

        self.logging.debug(
            "__get_closest_sheep_xy called with argument(" + self.__str__() + "," + sheeps.__str__() +
            "), returned (" +  closest.__str__() + "," + closest_distance.__str__() )

        return closest, closest_distance
