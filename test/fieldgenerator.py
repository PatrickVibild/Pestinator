import time

import fastrand
import numpy
import threading
from observer import Observer


def crop_color(infection: float):
    if infection < 0.2:
        return (0, 255, 0)
    if infection < 0.6:
        return (255, 165, 0)
    if infection < 0.95:
        return (255, 0, 0)
    return (255, 255, 255)


class FieldGenerator(Observer):
    def __init__(self, i, j, initial_infection=0.01):
        Observer.__init__(self)
        self.observe('spray', self.cure) # Listening to events 'spray' and calling method cure if trigger
        self.i = i
        self.j = j
        self.field = [[(fastrand.pcg32bounded(10000) / 10000) for x in range(i)] for y in range(j)]
        self.image = numpy.zeros((self.i * 6, self.j * 6, 3))
        for y in range(self.j):
            for x in range(self.i):
                cell_color = crop_color(self.field[x][y])
                for n in range(6):
                    for m in range(6):
                        self.image[(x * 6) + n][(y * 6) + m] = cell_color

    def change_crop_value(self, i, j, value):
        self.field[i][j] = value
        cell_color = crop_color(value)
        for n in range(6):
            for m in range(6):
                self.image[(i * 6) + n][(j * 6) + m] = cell_color

    def infest(self):
        while True:
            time.sleep(5)
            # TODO implement the pest spread

    def run(self):
        t1 = threading.Thread(target=self.infest)
        t1.start()

    def cure(self, coordinates):
        i, j = coordinates
        print('Cleaning crop{0}, {1}'.format(str(i), str(j)))
        self.change_crop_value(i, j, 0.0)
