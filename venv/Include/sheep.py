import random
import copy as cp
from direction import Direction


class Sheep:
    init_pos_limit = float()
    sheep_move_dist = float()
    alive = True

    def __init__(self, xPos, yPos, logging):
        self.xPos = xPos
        self.yPos = yPos
        self.logging = logging
        pos = "Starting position X: ", self.xPos, "Y: ", self.yPos,
        self.logging.info(pos)
        self.logging.debug(
            "Sheep constructor called with argument(" + self.__str__() + "," + xPos.__str__() + "," + yPos.__str__() + "," + logging.__str__() + ")")

    def move(self):
        self.logging.debug("move called with argument(" + self.__str__() + ")")
        while self.alive:
            direction = random.randrange(0, 4)
            direction = Direction(direction)
            x, y = self.__step(direction)
            if abs(x) <= self.init_pos_limit and abs(y) <= self.init_pos_limit:
                self.xPos = x
                self.yPos = y
                log = (self.__str__(), " position  X :", x, " Y :", y)
                self.logging.debug(log)
                break


    def position(self):
        return [cp.copy(self.xPos), cp.copy(self.yPos)]

    def isAlive(self):
        log = ("isAlive called with argument (" + self.__str__()+  " ) returns ("+ self.alive.__str__() + " )")
        self.logging.debug(log)
        return self.alive

    def kill(self):
        log = ("kill called with argument (" + self.__str__() +")")
        self.logging.debug(log)
        self.yPos = None
        self.xPos = None
        self.alive = False

    def __step(self, direction):
        x, y = self.xPos, self.yPos
        if direction == Direction.LEFT:
            x = self.xPos - self.sheep_move_dist
        elif direction == Direction.RIGHT:
            x = self.xPos + self.sheep_move_dist
        elif direction == Direction.DOWN:
            y = self.yPos - self.sheep_move_dist
        elif direction == Direction.UP:
            y = self.yPos + self.sheep_move_dist
        return x, y
