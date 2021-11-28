import threading
import time

from chronos import Chronos
from drone import Drone
from event import Event
from fieldgenerator import FieldGenerator
from observer import Observer
from spraying_organizer import Spraying_Organizer


class SprayingDrone(Observer, Drone):
    def __init__(self, world: FieldGenerator, organizer: Spraying_Organizer, drone_number, grid=False, speed=2, color=(127, 0, 255)):
        self.sick_coordinate_list = organizer.sick_coordinate_list
        Observer.__init__(self)
        Drone.__init__(self, world, speed, color)
    #    self.observe('sick_plant', self.add_sick_plant)
        self.sick_plants = [[0 for c in range(world.i)] for r in range(world.j)]
        self.tank = 2000
        self.tank_capacity = 2000
        self.number = drone_number
        self.grid = grid

    def run(self):
        t1 = threading.Thread(target=self.drone_routine)
        t1.start()

    def drone_routine(self):
        while True:
            if len(self.sick_coordinate_list) > 1:
                self.go_and_spray()
            time.sleep(Chronos.drone_waiting())

    def enough_tank(self):
        if self.tank <= 20:
     #       print("Not enough tank - returning to base")
            return False
        return True

    def add_sick_plant(self, coordinates):
        i, j = coordinates
        self.sick_plants[i][j] = 1
        if coordinates not in self.sick_coordinate_list:
            # print('Sick crop received: {0}, {1}'.format(str(i), str(j)))
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
            time.sleep(Chronos.drone_waiting())
        Event('charge and fill', self)

    def go_and_spray(self):
        while len(self.sick_coordinate_list) > 0 and self.enough_charge() and self.enough_tank() and not self.is_charging:
            self.spray_crop(self.sick_coordinate_list.pop(0))
        if not self.is_charging:
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
            time.sleep(Chronos.drone_waiting())
        if [self.position_x, self.position_y] == coordinates:
            if self.grid:
                # print("Spraying in a grid around {0}".format(coordinates))
                if self.position_x != 0:
                    self.position_x -= 1
                if self.position_y != 0:
                    self.position_y -= 1
                for i in range(3):
                    if self.position_x > self.area_x or self.position_x < 0:
                        self.position_x = self.area_x
                    if self.position_y > self.area_y or self.position_y < 0:
                        self.position_y = self.area_y
                    Event('spray', [self.position_x, self.position_y])
                    self.tank -= 1
                    if [self.position_x, self.position_y] in self.sick_coordinate_list:
                        # print("Removing coordinate from list...")
                        try:
                            self.sick_coordinate_list.remove([self.position_x, self.position_y])
                        except:
                            if [self.position_x, self.position_y] in self.sick_coordinate_list:
                                self.sick_coordinate_list.remove([self.position_x, self.position_y])
                    self.position_x += 1
                self.position_y += 1
                self.position_x -= 1
                for i in range(3):
                    if self.position_x > self.area_x or self.position_x < 0:
                        self.position_x = self.area_x
                    if self.position_y > self.area_y or self.position_y < 0:
                        self.position_y = self.area_y
                    Event('spray', [self.position_x, self.position_y])
                    self.tank -= 1
                    if [self.position_x, self.position_y] in self.sick_coordinate_list:
                        # print("Removing coordinate from list...")
                        try:
                            self.sick_coordinate_list.remove([self.position_x, self.position_y])
                        except :
                            pass
                    self.position_x -= 1
                self.position_y += 1
                self.position_x += 1
                for i in range(3):
                    if self.position_x > self.area_x or self.position_x < 0:
                        self.position_x = self.area_x
                    if self.position_y > self.area_y or self.position_y < 0:
                        self.position_y = self.area_y
                    Event('spray', [self.position_x, self.position_y])
                    self.tank -= 1
                    if [self.position_x, self.position_y] in self.sick_coordinate_list:
                        # print("Removing coordinate from list...")
                        try:
                            self.sick_coordinate_list.remove([self.position_x, self.position_y])
                        except :
                            pass
                    self.position_x += 1
            else:
                # print("Spraying drone: {0}".format(self.number))
                Event('spray', [self.position_x, self.position_y])
                self.tank -= 1

        elif not self.enough_charge():
            print("Not enough charge - returning to base")
        elif not self.enough_tank():
            print("Not enough tank - returning to base")
