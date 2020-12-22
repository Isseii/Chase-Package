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
        log = (self.__str__(), " starting position  X :", self.xPos, " Y :", self.yPos)
        self.logging.debug(log)

    def move(self):
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
        log = (self.__str__(), " living  : ", self.alive)
        self.logging.debug(log)
        return self.alive

    def kill(self,str):
        log = (str, " killed ",self.__str__())
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
