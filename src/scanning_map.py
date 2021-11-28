import random

import numpy


class ScanningMap:
    def __init__(self, area_x, area_y):
        self.area_x = area_x - 1
        self.area_y = area_y - 1
        self.heat_map = numpy.zeros((area_x, area_y))

    def obtain_new_direction(self, drone_x, drone_y):
        x = random.randint(0, self.area_x)
        y = random.randint(0, self.area_y)
        while self.heat_map[x][y] > 50:
            x = random.randint(0, self.area_x)
            y = random.randint(0, self.area_y)

        self.heat_map[x][y] = 100
        self.__reduce_values()
        self.__increase_values(x, y, drone_x, drone_y)
        return x, y

    def __reduce_values(self):
        for x in range(self.area_x):
            for y in range(self.area_y):
                self.heat_map[x][y] = max(self.heat_map[x][y] - 1, 0)

    def __increase_values(self, x, y, position_x, position_y):
        while position_x != x and position_y != y:
            if position_x < x:
                position_x += 1
            elif position_x > x:
                position_x -= 1
            if position_y < y:
                position_y += 1
            elif position_y > y:
                position_y -= 1
            self.__heat(position_x, position_y)

    def __heat(self, x, y):
        for i in range(5):
            for j in range(5):
                try:
                    self.heat_map[x + i - 2][y + j - 2] = 400
                except:
                    pass

