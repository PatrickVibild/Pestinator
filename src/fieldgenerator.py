import math
import time
from event import Event
import numpy
import threading
from observer import Observer
from chronos import Chronos
from weather_sim import Forecast


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
    weather = None

    def __init__(self, i, j, initial_infection=0.0, detection_threshold=0.2):
        Observer.__init__(self)
        self.observe('spray', self.cure)  # Listening to events 'spray' and calling method cure if trigger
        self.observe('weather', self.weather_update)
        self.detection_threshold = detection_threshold
        self.i = i
        self.j = j
        self.__healthy = 0
        self.__infected = 0
        self.__critical = 0
        self.__dead = 0
        self._field = [[bound(numpy.random.lognormal(0, 1) / 10 + initial_infection) for x in range(i)] for y in
                       range(j)]
        self._image = numpy.zeros((self.i * 6, self.j * 6, 3))
        for y in range(self.j):
            for x in range(self.i):
                cell_color = crop_color(self._field[x][y])
                self.stats(self._field[x][y])
                for n in range(6):
                    for m in range(6):
                        self._image[(x * 6) + n][(y * 6) + m] = cell_color
        side_values = 0.20
        self.kernel = [
            [side_values, side_values, side_values],
            [side_values, 0.7, side_values],
            [side_values, side_values, side_values]
        ]
        self.publish_stats()

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
        # TODO protect the cell once its been clean.
        while True:
            time.sleep(Chronos.field_waiting())
            if self.weather is None:
                continue
            copy_field = self._field
            wind_kernel = self.direction_kernel()
            for x in range(len(copy_field)):
                for y in range(len(copy_field[x])):
                    total = 0
                    for m in range(len(wind_kernel)):
                        if x + m - 1 < 0 or x + m - 1 >= len(copy_field):  # -1 allows us to use only a 3x3 kernel
                            continue
                        for n in range(len(wind_kernel[m])):
                            if y + n - 1 < 0 or y + n - 1 >= len(copy_field[x]):
                                continue
                            total += copy_field[x + m - 1][y + n - 1] * wind_kernel[m][n]
                    self.change_crop_value(x, y, total)
                    self.stats(self._field[x][y])
            self.publish_stats()
    def direction_kernel(self):
        wind_kernel = numpy.zeros((len(self.kernel), len(self.kernel[0])))
        direction = self.weather.wind_direction * math.pi / 180
        wind_kernel[0][0] = max(
            self.kernel[0][0] * math.cos(direction) / 2 + self.kernel[0][0] * (-1) * math.sin(direction) / 2, 0)
        wind_kernel[0][1] = max(self.kernel[0][1] * (-1) * math.sin(direction), 0)
        wind_kernel[0][2] = max(
            self.kernel[0][2] * (-1) * math.cos(direction) / 2 + self.kernel[0][2] * (-1) * math.sin(direction) / 2, 0)
        wind_kernel[1][0] = max(self.kernel[1][0] * math.cos(direction), 0)
        wind_kernel[1][1] = self.kernel[1][1]
        wind_kernel[1][2] = max(self.kernel[1][2] * (-1) * math.cos(direction), 0)
        wind_kernel[2][0] = max(
            self.kernel[2][0] * math.cos(direction) / 2 + self.kernel[2][0] * math.sin(direction) / 2, 0)
        wind_kernel[2][1] = max(self.kernel[2][1] * math.sin(direction), 0)
        wind_kernel[2][2] = max(
            self.kernel[2][2] * (-1) * math.cos(direction) / 2 + self.kernel[2][0] * math.sin(direction) / 2, 0)
        return wind_kernel

    def run(self):
        t1 = threading.Thread(target=self.infest)
        t1.start()

    def cure(self, coordinates):
        i, j = coordinates
        # print('Cleaning crop{0}, {1}'.format(str(i), str(j)))
        self.change_crop_value(i, j, 0.0)

    def weather_update(self, w_data: Forecast):
        # print('Field updated the weather')
        self.weather = w_data

    def stats(self, infection):
        if infection < 0.2:
            self.__healthy += 1
        elif infection < 0.6:
            self.__infected += 1
        elif infection < 0.95:
            self.__critical += 1
        else:
            self.__dead += 1

    def clear_stats(self):
        self.__healthy = 0
        self.__infected = 0
        self.__critical = 0
        self.__dead = 0

    def publish_stats(self):
        Event('field_data', (self.__healthy, self.__infected, self.__critical, self.__dead))
        self.clear_stats()
