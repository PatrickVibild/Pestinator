import threading
import time

from drone import Drone
from event import Event
from fieldgenerator import FieldGenerator
from observer import Observer


class ScanningDrone(Drone, Observer):
    def __init__(self, world: FieldGenerator, speed=2, color=(0, 0, 255)):
        Observer.__init__(self)
        # TODO implement observers
        Drone.__init__(self, world, speed, color)

    def run(self):
        t1 = threading.Thread(target=self.drone_routine)
        t1.start()

    def drone_routine(self):
        while True:
            self.flight_route()

            if self.field.is_crop_infected(self.position_x, self.position_y):
                Event('sick_plant', [self.position_x, self.position_y])
            time.sleep(0.2)

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
