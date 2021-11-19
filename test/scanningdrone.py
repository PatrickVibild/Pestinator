import random
import threading
import time

from test.drone import Drone
from test.event import Event
from test.fieldgenerator import FieldGenerator
from observer import Observer


def swap(x, y):
    tmp = x
    x = y
    y = tmp
    return x, y


def bound(value, upper, lower):
    return min(upper, max(value, lower))


class ScanningDrone(Drone, Observer):
    def __init__(self, world: FieldGenerator, speed=2, color=(0, 0, 255)):
        Observer.__init__(self)
        # TODO implement observers
        Drone.__init__(self, world, speed, color)
        self.exploring = True

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
        x, y = (0, random.randint(5, 20))
        while True:
            self.fly_to(x, y)
            x, y = swap(x, y)
            self.fly_to(x, y)
            x, y = self.shift_position(x, y)
            self.fly_to(x, y)
            x, y = swap(x, y)
            self.fly_to(x, y)
            x, y = self.shift_position(x, y)

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
            self.scan_and_report()
            time.sleep(0.01)

    def scan_and_report(self):
        if self.field.is_crop_infected(self.position_x, self.position_y):
            Event('sick_plant', [self.position_x, self.position_y])
