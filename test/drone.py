import time

import pygame

from fieldgenerator import FieldGenerator
from event import Event
import threading


class Drone:
    def __init__(self, world: FieldGenerator, speed=2):
        self.area_x = world.i
        self.area_y = world.j
        self.speed = speed  # TODO to be used somewhere?
        self.position_x = 0  # TODO change this, for testing starting in the mid of the field
        self.position_y = 0
        self.field = world.field

    def fly_direction(self, x, y):
        self.position_x += x
        self.position_y += y
        if self.position_x < 0:
            self.position_x = 0
        if self.position_y < 0:
            self.position_y = 0
        if self.position_x > self.area_x:
            self.position_x = self.area_x
        if self.position_y > self.area_y:
            self.position_y = self.area_y
        print('Drone at {0}, {1}'.format(str(self.position_x), str(self.position_y)))

    def scan_and_spray(self):
        infection = self.field[self.position_x][self.position_y].infection
        print('Scanning field - ' + str(infection))
        if infection > 0.20:
            Event('spray', [self.position_x, self.position_y])

    def random_fly(self):
        while True:
            self.fly_direction(1, 0)
            self.scan_and_spray()
            time.sleep(0.2)

    def render(self, display, camera_pos):
        x, y = camera_pos
        pygame.draw.circle(display, (0, 0, 255), (self.position_x * 6 + x, self.position_y * 6 + y), 8)

    def run(self):
        t1 = threading.Thread(target=self.random_fly)
        t1.start()
