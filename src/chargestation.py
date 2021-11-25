import threading
import time
from observer import Observer
from drone import Drone
from spraydrone import SprayingDrone
from scanningdrone import ScanningDrone
from chronos import Chronos


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

    def charge_routine(self):
        scanning = (scanning for scanning in self.active_drones if isinstance(scanning, ScanningDrone))
        spraying = (spray for spray in self.active_drones if isinstance(spray, SprayingDrone))

        while True:
            time.sleep(Chronos.charging_waiting())
            for scanning_drone in self.active_drones:
                if not hasattr(scanning_drone, 'tank'):
                    if scanning_drone.battery >= scanning_drone.battery_capacity:
                        scanning_drone.is_charging = False
                        self.active_drones.remove(scanning_drone)
                        self.capacity -= 1
                    else:
                        scanning_drone.battery += self.charging_speed

            for spraying_drone in self.active_drones:
                if hasattr(spraying_drone, 'tank'):
                    if spraying_drone.battery >= spraying_drone.battery_capacity and \
                            spraying_drone.tank >= spraying_drone.tank_capacity:
                        spraying_drone.is_charging = False
                        self.active_drones.remove(spraying_drone)
                        self.capacity -= 1

                    if spraying_drone.battery < spraying_drone.battery_capacity:
                        spraying_drone.battery += self.charging_speed

                    if spraying_drone.tank < spraying_drone.tank_capacity:
                        spraying_drone.tank += 20

    def run(self):
        t1 = threading.Thread(target=self.charge_routine)
        t1.start()
