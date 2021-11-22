import threading
import time

from test.drone import Drone
from test.event import Event
from test.fieldgenerator import FieldGenerator
from observer import Observer


class SprayingDrone(Observer, Drone):
    sick_coordinate_list = []
    def __init__(self, world: FieldGenerator, speed=2, color=(127, 0, 255)):
        self.sick_coordinate_list = SprayingDrone.sick_coordinate_list
        Observer.__init__(self)
        Drone.__init__(self, world, speed, color)
        self.observe('sick_plant', self.add_sick_plant)
        self.sick_plants = [[0 for c in range(world.i)] for r in range(world.j)]
        self.sick_coordinate_list = []
        self.tank = 200
        self.tank_capacity = 200
        self.is_filling = False

    def run(self):
        t1 = threading.Thread(target=self.drone_routine)
        t1.start()

    def drone_routine(self):
        while True:
            if len(self.sick_coordinate_list) > 1:
                self.go_and_spray()
            time.sleep(0.2)

    def enough_tank(self):
        if self.tank <= 20:
            return False
        return True

    def add_sick_plant(self, coordinates):
        i, j = coordinates
        self.sick_plants[i][j] = 1
        if coordinates not in self.sick_coordinate_list:
            print('Sick crop received: {0}, {1}'.format(str(i), str(j)))
            self.sick_coordinate_list.append(coordinates)

    def charge_fill_drone(self):
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
            time.sleep(0.01)
        Event('charge and fill', self)

    def go_and_spray(self):
        while len(self.sick_coordinate_list) > 0 and self.enough_charge() and self.enough_tank() and not self.is_filling and not self.is_charging:
            self.spray_crop(self.sick_coordinate_list.pop(0))
        if not self.is_charging or not self.is_filling:
            self.charge_fill_drone()

    def spray_crop(self, coordinates):
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
            time.sleep(0.01)
        if [self.position_x, self.position_y] == coordinates:
            Event('spray', [self.position_x, self.position_y])
            self.tank -= 10
        elif not self.enough_charge():
            print("Not enough charge - returning to base")
        elif not self.enough_tank():
            print("Not enough tank - returning to base")
