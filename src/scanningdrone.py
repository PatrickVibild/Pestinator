import random
import threading
import time

import numpy

from drone import Drone
from event import Event
from fieldgenerator import FieldGenerator
from weather_sim import Forecast
from observer import Observer


def swap(x, y):
    tmp = x
    x = y
    y = tmp
    return x, y


def bound(value, upper, lower):
    return min(upper, max(value, lower))


class ScanningDrone(Drone, Observer):
    def __init__(self, world: FieldGenerator, weather: Forecast, speed=2, color=(0, 0, 255)):
        Observer.__init__(self)
        # TODO implement observers
        Drone.__init__(self, world, weather, speed, color)
        self.observe('weather', self.weather_update)
        self.exploring = True
        self.spiral_count = 1
        self.direction_count = 0
        self.visibility_thresh = 50

    def weather_update(self, wind_data: Forecast):
        print('Field updated the weather')
        self.weather = wind_data

    def run(self):
        t1 = threading.Thread(target=self.fast_brute_force_routine)
        t1.start()

    def drone_routine(self):
        while True:
            self.flight_route()

            if self.field.is_crop_infected(self.position_x, self.position_y):
                Event('sick_plant', [self.position_x, self.position_y])
            time.sleep(0.001)

    def flight_route(self):
        if self.position_y % 2 == 0:
            self.position_x += 1
            if self.position_x > self.area_x:
                self.position_x = self.area_x
        if self.position_x == self.area_x:
            self.position_y += 1
        if self.position_y % 2 == 1:
            self.position_x -= 1
            if self.position_x < 0:
                self.position_x = 0
        if self.position_x == 0:
            self.position_y += 1
        if self.position_y >= self.area_y:
            self.position_y = self.area_y

    def fast_brute_force_routine(self):
        seed = random.randint(0, self.area_x + self.area_y)
        if seed <= self.area_y:
            x, y = (0, seed)
        else:
            x, y = (seed - self.area_y, 0)
        self.exploring = True if random.randint(0, 1) == 0 else False

        while True:
            if self.weather.wind_speed <= self.wind_thresh and not self.weather.night:
                self.fly_to(x, y)
                x, y = swap(x, y)
                self.fly_to(x, y)
                x, y = self.shift_position(x, y)
                self.fly_to(x, y)
                x, y = swap(x, y)
                self.fly_to(x, y)
                x, y = self.shift_position(x, y)
            else:
                self.charge_drone()

    def shift_position(self, x, y):
        if y == self.area_y and x == self.area_x:
            self.exploring = False
        if y == 0 and x == 0:
            self.exploring = True
        if self.exploring:
            if y == 0 or y == self.area_y:
                return bound(x + random.randint(3, 8), self.area_x, 0), y
            if x == 0 or x == self.area_x:
                return x, bound(y + random.randint(3, 8), self.area_y, 0)
        else:
            if y == 0 or y == self.area_y:
                return bound(x - random.randint(3, 8), self.area_x, 0), y
            if x == 0 or x == self.area_x:
                return x, bound(y - random.randint(3, 8), self.area_y, 0)

    def fly_to(self, x, y):
        while (self.position_x != x) or (self.position_y != y):
            if self.weather.wind_speed >= self.wind_thresh:
                break
            self.forward(x, y)
            self.scan_and_report(x, y)
            time.sleep(0.05)

    def forward(self, x, y):
        if self.position_x < x:
            self.position_x += 1
            self.battery -= 1
        elif self.position_x > x:
            self.position_x -= 1
            self.battery -= 1
        if self.position_y < y:
            self.position_y += 1
            self.battery -= 1
        elif self.position_y > y:
            self.position_y -= 1
            self.battery -= 1
        self.position_x = bound(self.position_x, self.area_x, 0)
        self.position_y = bound(self.position_y, self.area_y, 0)

    def scan_and_report(self, direction_x, direction_y):
        self.scan_area(self.position_x, self.position_y, direction_x, direction_y)

    def scan_area(self, x, y, direction_x, direction_y, radius=0):
        infected = False
        area = []
        if radius > 0:
            area.append({'x': x - radius, 'y': y + radius})
            area.append({'x': x - radius, 'y': y - radius})
            area.append({'x': x + radius, 'y': y - radius})
            area.append({'x': x + radius, 'y': y + radius})
            for a in area:
                if not self.is_coordinate_in_area(a['x'], a['y']):
                    continue

                while self.position_x != a['x'] or self.position_y != a['y']:
                    self.forward(a['x'], a['y'])
                    if self.field.is_crop_infected(self.position_x, self.position_y):
                        infected = True
                        Event('sick_plant', [self.position_x, self.position_y])
                    time.sleep(0.05)

            #if infected:
            if radius < 4 and infected:
                self.scan_area(x, y, direction_x, direction_y, radius + 1)
        else:
            if self.field.is_crop_infected(self.position_x, self.position_y):
                Event('sick_plant', [self.position_x, self.position_y])
                self.scan_area(x, y, direction_x, direction_y, radius + 1)

        times = 0
        while (self.position_x != x or self.position_y != y) and times <= radius:
            self.forward(x, y)
            time.sleep(0.05)
            times += 1

    def is_coordinate_in_area(self, x, y):
        return 0 <= x <= self.area_x and 0 <= y <= self.area_y

    def chance_of_seeing_crop(self):
        if self.weather.visibility >= self.visibility_thresh:
            return self.field.is_crop_infected(self.position_x, self.position_y)
        return False
        # return self.probability(self.weather.visibility)
        # do we need to implement this proability? This should give false positives, not false negatives.

    # def probability(self, chance):
    #    return random.randint(0, 100) < chance
