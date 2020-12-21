import random
import copy as cp
from direction import Direction


class Sheep:
    init_pos_limit = float()
    sheep_move_dist = float()
    alive = True

    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    def move(self):
        while self.alive:
            direction = random.randrange(0, 4)
            direction = Direction(direction)

            x, y = self.__step(direction)
            if abs(x) <= self.init_pos_limit and abs(y) <= self.init_pos_limit:
                self.xPos = x
                self.yPos = y
                break

    def position(self):
        return [cp.copy(self.xPos), cp.copy(self.yPos)]

    def isAlive(self):
        return self.alive

    def kill(self):
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
