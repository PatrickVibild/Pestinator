import time

import pygame

from fieldgenerator import FieldGenerator
from event import Event
import threading
from observer import Observer
import math

pest_threshold = 0.2


class Drone(Observer):
    def __init__(self, world: FieldGenerator, type, speed=2):
        self.area_x = world.i
        self.area_y = world.j
        self.speed = speed  # TODO to be used somewhere?
        self.position_x = 0
        self.position_y = 0
        self.field = world
        self.type = type
        self.base_coordinates = [0, 0]
        self.battery = 1000
        if type == 'spray':
            Observer.__init__(self)
            self.observe('sick_plant',
                         self.add_sick_plant)  # Listening to events 'spray' and calling method cure if trigger
            self.sick_plants = [[0 for c in range(world.i)] for r in range(world.j)]
            self.sick_coordinate_list = []

    def fly_direction(self):
        if self.position_y % 2 == 0:
            self.position_x += 1
        if self.position_y % 2 == 1:
            self.position_x -= 1
        if self.position_x < 0:
            self.position_x = 0
            self.position_y += 1
        # if self.position_y < 0:
        #    self.position_y = 0
        if self.position_x > self.area_x:
            self.position_x = self.area_x
            self.position_y += 1
        if self.position_y > self.area_y:
            self.position_y = self.area_y

    def scan_and_spray(self):
        infection = self.field.obtain_crop_value(self.position_x, self.position_y)
        # print('Scanning field - ' + str(infection))
        if infection > 0.20:
            Event('spray', [self.position_x, self.position_y])

    def scan(self):
        while True:
            self.fly_direction()
            if self.field.obtain_crop_value(self.position_x, self.position_y) > pest_threshold:
                Event('sick_plant', [self.position_x, self.position_y])
            time.sleep(0.2)

    def spraying_routine(self):
        print(len(self.sick_plants))
        print(len(self.sick_plants[0]))
        Event('create_sick_plant', [10, 0])
        Event('create_sick_plant', [20, 0])
        Event('create_sick_plant', [75, 100])
        Event('create_sick_plant', [100, 100])
        Event('create_sick_plant', [140, 100])
        print(self.sick_coordinate_list)
        while True:
            if len(self.sick_coordinate_list) > 2:
                self.go_and_spray()
            time.sleep(0.2)

    def go_and_spray(self):
        print("Enough plants - let's spray!")
        while len(self.sick_coordinate_list) > 0 and self.enough_charge():
            self.goto_point(self.sick_coordinate_list.pop(0))
        self.return_charger()

    def return_charger(self):
        i, j = self.base_coordinates
        while ((self.position_x != i) or (self.position_y != j)):
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
            time.sleep(0.2)

    def goto_point(self, coordinates):
        # Go to
        print("Going to point: ")
        print(coordinates)

        i, j = coordinates
        while ((self.position_x != i) or (self.position_y != j)) and self.enough_charge():
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
            time.sleep(0.2)
        if [self.position_x, self.position_y] == coordinates:
            print("Position reached!")
            print("Spraying...")
            Event('spray', [self.position_x, self.position_y])
        elif self.enough_charge() == False:
            print("Not enough charge - returning to base")

    def enough_charge(self):
        # print("Battery status: ")
        # print(self.battery)
        if (self.battery > self.distance_to_base() + 5):
            return True
        else:
            return False

    def distance_to_base(self):
        dronePos = [self.position_x, self.position_y]
        distance = math.dist(dronePos, self.base_coordinates)
        # print("Distance to base: ")
        # print (distance)
        return distance

    def add_sick_plant(self, coordinates):
        i, j = coordinates
        print('Sick crop received: {0}, {1}'.format(str(i), str(j)))
        self.sick_plants[i][j] = 1
        self.sick_coordinate_list.append(coordinates)

    def render(self, display, camera_pos):
        x, y = camera_pos
        if self.type == 'scan':
            pygame.draw.circle(display, (0, 0, 255), (self.position_x * 6 + x, self.position_y * 6 + y), 8)
        if self.type == 'spray':
            pygame.draw.circle(display, (255, 0, 255), (self.position_x * 6 + x, self.position_y * 6 + y), 8)

    def run(self):
        if self.type == 'scan':
            t1 = threading.Thread(target=self.scan)
            t1.start()
        if self.type == 'spray':
            t2 = threading.Thread(target=self.spraying_routine)
            t2.start()
