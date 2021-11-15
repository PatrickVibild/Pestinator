import threading
import time

from test.drone import Drone
from test.event import Event
from test.fieldgenerator import FieldGenerator
from observer import Observer


class SprayingDrone(Observer, Drone):
    def __init__(self, world: FieldGenerator, speed=2, color=(127, 0, 255)):
        Observer.__init__(self)
        Drone.__init__(self, world, speed, color)
        self.observe('sick_plant', self.add_sick_plant)
        self.sick_plants = [[0 for c in range(world.i)] for r in range(world.j)]
        self.sick_coordinate_list = []

    def run(self):
        t1 = threading.Thread(target=self.drone_routine)
        t1.start()

    def drone_routine(self):
        while True:
            if len(self.sick_coordinate_list) > 1:
                self.go_and_spray()
            time.sleep(0.2)

    def add_sick_plant(self, coordinates):
        i, j = coordinates
        print('Sick crop received: {0}, {1}'.format(str(i), str(j)))
        self.sick_plants[i][j] = 1
        self.sick_coordinate_list.append(coordinates)

    def go_and_spray(self):
        while len(self.sick_coordinate_list) > 0 and self.enough_charge() and not self.is_charging:
            self.spray_crop(self.sick_coordinate_list.pop(0))
        if not self.is_charging:
            self.charge_drone()

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
            time.sleep(0.2)
        if [self.position_x, self.position_y] == coordinates:
            Event('spray', [self.position_x, self.position_y])
        elif not self.enough_charge():
            print("Not enough charge - returning to base")
