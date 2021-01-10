import random
import copy as cp
from chase.direction import Direction


class Sheep:
    init_pos_limit = 10.0
    sheep_move_dist = 0.5
    alive = True

    def __init__(self, xPos, yPos, logging):
        self.xPos = xPos
        self.yPos = yPos
        self.logging = logging
        pos = "Starting position X: ", self.xPos, "Y: ", self.yPos,
        self.logging.info(pos)
        self.logging.debug(
            "Sheep constructor called with argument(" + str(self) + "," + str(xPos) + "," + str(yPos) + "," + str(logging) + ")")

    def move(self):
        self.logging.debug("move called with argument(" + str(self) + ")")
        while self.alive:
            direction = random.randrange(0, 4)
            direction = Direction(direction)
            x, y = self.__step(direction)
            if abs(x) <= self.init_pos_limit and abs(y) <= self.init_pos_limit:
                self.xPos = x
                self.yPos = y
                log = (str(self), " position  X :", x, " Y :", y)
                self.logging.debug(log)
                break


    def position(self):
        return [cp.copy(self.xPos), cp.copy(self.yPos)]

    def is_alive(self):
        log = ("isAlive called with argument (" + str(self)+  " ) returns ("+ str(self.alive) + " )")
        self.logging.debug(log)
        return self.alive

    def kill(self):
        log = ("kill called with argument (" + str(self) +")")
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
