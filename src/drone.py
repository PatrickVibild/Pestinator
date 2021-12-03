import math
import time

import pygame
from fieldgenerator import FieldGenerator
from chronos import Chronos
from weather_sim import Forecast
from abc import ABC, abstractmethod

from event import Event


class Drone(ABC):
    def __init__(self, world: FieldGenerator, weather: Forecast, speed=2, color=(0, 0, 0)):
        self.area_x = world.i - 1
        self.area_y = world.j - 1
        self.speed = speed  # TODO to be used somewhere?
        self.position_x = 0
        self.position_y = 0
        self.field = world
        self.base_coordinates = [0, 0]
        self.battery = 2000
        self.battery_capacity = 2000
        self.is_charging = False
        self.color = color
        self.weather = weather
        self.wind_thresh = 8

    def distance_to_base(self):
        dronePos = [self.position_x, self.position_y]
        distance = math.dist(dronePos, self.base_coordinates)
        return distance

    def enough_charge(self):
        if self.battery <= self.distance_to_base() + 5:
      #      print("Not enough battery - returning to base")
            return False
        return True

    def charge_drone(self):
        i, j = self.base_coordinates
        while (self.position_x != i) or (self.position_y != j):
            if self.position_x < i:
                self.position_x += 1
                self.battery -= 1
            elif self.position_x > i:
                self.position_x -= 1
                self.battery -= 1

            if self.position_y < j:
                self.position_y += 1
                self.battery -= 1
            elif self.position_y > j:
                self.position_y -= 1
                self.battery -= 1
            time.sleep(Chronos.drone_waiting())
        Event('charge', self)

    def render(self, display, camera_pos):
        x, y = camera_pos
        pygame.draw.circle(display, self.color, (self.position_x * 6 + x, self.position_y * 6 + y), 8)

    @abstractmethod
    def drone_routine(self):
        pass

    @abstractmethod
    def run(self):
        pass
