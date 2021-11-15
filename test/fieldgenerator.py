import time

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


def bound(value):
    return max(min(value, 0.9), 0)


class FieldGenerator(Observer):
    def __init__(self, i, j, initial_infection=0.0, detection_threshold=0.2):
        Observer.__init__(self)
        self.observe('spray', self.cure) # Listening to events 'spray' and calling method cure if trigger
        self.detection_threshold = detection_threshold
        self.i = i
        self.j = j
        self._field = [[bound(numpy.random.lognormal(0, 1) / 10 + initial_infection) for x in range(i)] for y in range(j)]
        self._image = numpy.zeros((self.i * 6, self.j * 6, 3))
        for y in range(self.j):
            for x in range(self.i):
                cell_color = crop_color(self._field[x][y])
                for n in range(6):
                    for m in range(6):
                        self._image[(x * 6) + n][(y * 6) + m] = cell_color
        side_values = 0.06
        self.kernel = [
            [side_values, side_values   , side_values],
            [side_values, 0.7          , side_values],
            [side_values, side_values   , side_values]
        ]
    def obtain_render_image(self):
        return self._image

    def obtain_crop_value(self, i, j):
        return self._field[i][j]

    def is_crop_infected(self, i, j):
        return self._field[i][j] > self.detection_threshold

    def change_crop_value(self, i, j, value):
        self._field[i][j] = value
        cell_color = crop_color(value)
        for n in range(6):
            for m in range(6):
                self._image[(i * 6) + n][(j * 6) + m] = cell_color

    def infest(self):
        while True:
            time.sleep(30)
            copy_field = self._field
            for x in range(len(copy_field)):
                for y in range(len(copy_field[x])):
                    total = 0
                    for m in range(len(self.kernel)):
                        if x+m-1 < 0 or x+m-1 >= len(copy_field):
                            continue
                        for n in range(len(self.kernel[m])):
                            if y+n-1 < 0 or y+n-1 >= len(copy_field[x]):
                                continue
                            total += copy_field[x+m-1][y+n-1] * self.kernel[m][n]
                    self.change_crop_value(x, y, total)

    def run(self):
        t1 = threading.Thread(target=self.infest)
        t1.start()

    def cure(self, coordinates):
        i, j = coordinates
        print('Cleaning crop{0}, {1}'.format(str(i), str(j)))
        self.change_crop_value(i, j, 0.0)

