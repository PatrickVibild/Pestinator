import random
import threading
import time

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
        self.chance_crop = False
        self.visibility_thresh = 50

    def weather_update(self, wind_data: Forecast):
        print('Field updated the weather')
        self.weather = wind_data

    def run(self):
        t1 = threading.Thread(target=self.fast_brute_force_routine)
        t1.start()

    def move_right(self, i):
        return self.position_x + i, self.position_y

    def move_left(self, i):
        return self.position_x - i, self.position_y

    def move_up(self, i):
        return self.position_x, self.position_y - i

    def move_down(self, i):
        return self.position_x, self.position_y + i

    def drone_routine(self):
        while True:
            self.flight_route()

            if self.field.is_crop_infected(self.position_x, self.position_y):
                Event('sick_plant', [self.position_x, self.position_y])
            time.sleep(0.001)

    def scan_area(self):
        self.spiral_count = 1
        self.direction_count = 0
        while self.field.is_crop_infected(self.position_x, self.position_y):
            Event('sick_plant', [self.position_x, self.position_y])
            print(self.move_right(self.spiral_count)[0])
            if self.spiral_count % 2 == 1:
                if self.direction_count == 0:
                    self.fly_to(self.move_right(self.spiral_count)[0], self.move_right(self.spiral_count)[1])
                    self.direction_count += 1
                else:
                    self.fly_to(self.move_down(self.spiral_count)[0], self.move_down(self.spiral_count)[1])
                    self.spiral_count += 1
                    self.direction_count += 1
            else:
                if self.direction_count == 0:
                    self.fly_to(self.move_left(self.spiral_count)[0], self.move_left(self.spiral_count)[1])
                    self.direction_count += 1
                else:
                    self.fly_to(self.move_up(self.spiral_count)[0], self.move_up(self.spiral_count)[1])
                    self.spiral_count += 1
                    self.direction_count += 1

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
            if self.weather.wind_speed <= self.wind_thresh:
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
                print("The wind speed is too high, so drones are not able to fly")

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
        if self.chance_of_seeing_crop():
            # Each time we detect a infected crop we scan the area
            self.scan_area()
            # Event('sick_plant', [self.position_x, self.position_y])

    def chance_of_seeing_crop(self):
        # print("visibility Drone: " + str(self.weather.visibility))
        if self.weather.visibility >= self.visibility_thresh:
            self.chance_crop = self.field.is_crop_infected(self.position_x, self.position_y)
        else:
            self.chance_crop = self.probability(self.weather.visibility)
        return self.chance_crop

    def probability(self, chance):
        return random.randint(0, 100) < chance
