import random
import copy


class Sheep:
    init_pos_limit = float()
    sheep_move_dist = float()

    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    def step(self, direction):
        holder = float()
        if direction == 0:
            holder = self.xPos - self.sheep_move_dist
        elif direction == 1:
            holder = self.xPos + self.sheep_move_dist
        elif direction == 2:
            holder = self.yPos - self.sheep_move_dist
        elif direction == 3:
            holder = self.yPos + self.sheep_move_dist
        return holder

    def move(self):
        direction = random.randrange(0, 4)
        self.step(direction)
        loop = True
        while loop:
            if abs(self.step(direction)) <= 10.0:
                loop = False
            else:
                direction = random.randrange(0, 4)

        if direction == 0:
            self.xPos -= self.sheep_move_dist
        elif direction == 1:
            self.xPos += self.sheep_move_dist
        elif direction == 2:
            self.yPos -= self.sheep_move_dist
        elif direction == 3:
            self.yPos += self.sheep_move_dist

        return True

    def position(self):
        return [copy.copy(self.xPos), copy.copy(self.yPos)]
