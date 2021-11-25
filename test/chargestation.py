import threading
import time
from observer import Observer
from drone import Drone
from spraydrone import SprayingDrone


class ChargeStation(Observer):
    def __init__(self, capacity, charging_speed):
        Observer.__init__(self)
        self.observe('charge', self.charge)
        self.observe('charge and fill', self.charge_and_fill)
        self.active_drones = []
        self.charging_speed = charging_speed
        self.capacity = capacity

    def charge(self, drone: Drone):
        if len(self.active_drones) < self.capacity:
            drone.is_charging = True
            self.capacity += 1
            self.active_drones.append(drone)

    def charge_and_fill(self, sprayingdrone: SprayingDrone):
        if len(self.active_drones) < self.capacity:
            sprayingdrone.is_charging = True
            sprayingdrone.is_filling = True
            self.capacity += 1
            self.active_drones.append(sprayingdrone)

    def routine(self):
        while True:
            time.sleep(0.2)
            for drone in self.active_drones:
                if drone.battery >= drone.battery_capacity:
                    drone.is_charging = False
                    self.active_drones.remove(drone)
                    self.capacity -= 1
                else:
                    drone.battery += self.charging_speed

            for sprayingdrone in self.active_drones:
                if hasattr(sprayingdrone,'tank'):
                    if sprayingdrone.battery >= sprayingdrone.battery_capacity:
                        sprayingdrone.is_charging = False
                    else:
                        sprayingdrone.battery += self.charging_speed
                    if sprayingdrone.tank >= sprayingdrone.tank_capacity:
                        sprayingdrone.is_filling = False
                    else:
                        sprayingdrone.tank += 20
                    if not sprayingdrone.is_filling and not sprayingdrone.is_charging:
                        self.active_drones.remove(sprayingdrone)
                        self.capacity -= 1

    def run(self):
        t1 = threading.Thread(target=self.routine)
        t1.start()
