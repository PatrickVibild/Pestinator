import time
import pygame
import threading
from event import Event
from observer import Observer


class ChargeStation(Observer):
    def __init__(self, position_x, position_y, length, width):
        self.position_x = position_x
        self.position_y = position_y
        self.length = length
        self.width = width
        self.battery = 0
        self.charge_flag = 0
        Observer.__init__(self)
        self.observe('need to charge', self.charge)
        #self.observe('need to leave')

    def render(self, display, position, size):
        pygame.draw.rect(display, (104, 85, 108), (position, size), 0)

    def charge(self, battery):
        self.battery = battery
        while self.battery < 1000:
            self.battery += 2
            print('charging: ', self.battery)
            time.sleep(0.2)
        Event('Charge finished', self.battery)


    #def run(self):
    #    t1 = threading.Thread(target=self.charge()
    #    t1.start()
