import time

import pygame

from fieldgenerator import FieldGenerator
from event import Event
import threading
from observer import Observer
import numpy as np


class Drone(Observer):
    def __init__(self, world: FieldGenerator, type, speed=2):
        self.area_x = world.i
        self.area_y = world.j
        self.speed = speed  # TODO to be used somewhere?
        self.position_x = 0
        self.position_y = 0
        self.field = world.field
        self.type = type
        self.base_coordinates = [0,0]
        self.battery = 100
        if type == 'spray':
            Observer.__init__(self)
            self.observe('sick_plant', self.add_sick_plant) # Listening to events 'spray' and calling method cure if trigger
            self.sick_plants = [[0 for c in range(world.i)] for r in range(world.j)]
            self.sick_coordinate_list = []
        
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
        #print('Drone at {0}, {1}'.format(str(self.position_x), str(self.position_y)))

    def scan_and_spray(self):
        infection = self.field[self.position_x][self.position_y]
        #print('Scanning field - ' + str(infection))
        if infection > 0.20:
            Event('spray', [self.position_x, self.position_y])

    def random_fly(self):
        while True:
            self.fly_direction(1, 0)
            self.scan_and_spray()
            time.sleep(0.2)

    def scan(self):
        while True:
            self.fly_direction(1, 0)
            self.scan_and_spray()
            time.sleep(0.2)

    def spraying_routine(self):
        print(len(self.sick_plants))
        print(len(self.sick_plants[0]))
        Event('sick_plant', [10, 10])
        Event('sick_plant', [50, 50])
        Event('sick_plant', [100, 100])
        print(self.sick_coordinate_list)
        while True:
            if len(self.sick_coordinate_list) > 2:
                self.go_and_spray()
            time.sleep(0.2)
    
    def go_and_spray(self):
        print ("Let's spray!")
        while len(self.sick_coordinate_list) > 0:
            self.goto_point(self.sick_coordinate_list.pop(0))
            
    def return_charger(self):
        self.goto_point([0,0])
        
    def goto_point(self,coordinates):
        #Go to 
        print("Going to point: ")
        print(coordinates)
        
        i,j = coordinates
        while (self.position_x != i) or (self.position_y != j):
            if self.position_x < i:
                self.position_x += 1
            elif self.position_x > i:
                self.position_x -= 1
                
            if self.position_y < i:
                self.position_y += 1
            elif self.position_y > i:
                self.position_y -= 1
            time.sleep(0.2)
        print("Position reached!")
        
    def enough_charge(self):
        if (self.battery < self.distance_to_base):
            return True
        else: 
            return False
        
    def distance_to_base(self):
        dronePos = [self.position_x,self.position_y]
        return np.linalg.norm(dronePos - self.base_coordinates)
    
    def add_sick_plant(self,coordinates):
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

