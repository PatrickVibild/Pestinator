import threading
import time
from observer import Observer
from drone import Drone


class ChargeStation(Observer):
    def __init__(self, capacity, charging_speed):
        Observer.__init__(self)
        self.observe('charge', self.charge)
        self.active_drones = []
        self.charging_speed = charging_speed
        self.capacity = capacity

    def charge(self, drone: Drone):
        if len(self.active_drones) < self.capacity:
            drone.is_charging = True
            self.capacity += 1
            self.active_drones.append(drone)

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

    def run(self):
        t1 = threading.Thread(target=self.routine)
        t1.start()
