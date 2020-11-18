import math
from direction import Direction


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Wolf:
    init_pos_limit = float()
    wolf_move_dist = float()

    def __init__(self):
        self.xPos = 0.0
        self.yPos = 0.0

    def move(self, sheep: list):
        csx, csy = self.__get_closest_sheep_xy(sheep)
        # print("closest_sheep=[" + str(csx) + "," + str(csy) + "]") # DEBUG

        # TODO: __check_for_prey and handle if there is any sheep to go bye bye :*

        direction = self.__go_towards(csx, csy)
        x, y = self.__step(direction)
        self.xPos = x
        self.yPos = y

    def __check_for_prey(self, csx, csy):
        if distance(self.xPos, self.yPos, csx, csy) < self.wolf_move_dist:
            return True
        return False

    def __step(self, direction):
        x, y = self.xPos, self.yPos
        if direction == Direction.LEFT:
            x = self.xPos - self.wolf_move_dist
        elif direction == Direction.RIGHT:
            x = self.xPos + self.wolf_move_dist
        elif direction == Direction.DOWN:
            y = self.yPos - self.wolf_move_dist
        elif direction == Direction.UP:
            y = self.yPos + self.wolf_move_dist
        return x, y

    def __go_towards(self, csx, csy):
        dist = distance(self.xPos, self.yPos, csx, csy)
        x, y = self.xPos - csx, self.yPos - csy
        x, y = x/dist, y/dist
        # print(str(x) + ", " + str(y)) # DEBUG
        if abs(x) > abs(y):
            if x > 0:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        else:
            if y > 0:
                return Direction.UP
            else:
                return Direction.DOWN

    def __get_closest_sheep_xy(self, sheep: list):
        closest = sheep[0]

        for s in sheep:
            closest_distance = distance(self.xPos, self.yPos, closest.xPos, closest.yPos)
            sheep_distance = distance(self.xPos, self.yPos, s.xPos, s.yPos)
            if closest_distance > sheep_distance:
                closest = s

        return closest.xPos, closest.yPos
