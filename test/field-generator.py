import random

import numpy


class FieldGenerator:
    def __init__(self, x, y, initial_infection=0.01):
        self.field = numpy.zeros((x, y))
        for x in range(0, x):
            for y in range(0, y):
                # TODO - maybe use a log-normal distribution? average on low values, but with chance of long tails.
                self.field[x][y] = CropCell(random.uniform((0, initial_infection)))


class CropCell:
    def __init__(self, infection):
        assert infection <= 1
        assert infection >= 0
        self.infection = infection
        self.alive = True

    def is_sick(self):
        if not self.alive or self.infection <= 0.2:
            return False
        return True

    # TODO - implement cell update from its neightbours.
    def update(self):
        self.alive = False if self.infection > 0.95 else True
