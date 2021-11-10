import time
import  pygame
import threading

class ChargeStation:
    def __init__(self, position_x, position_y, length, width):
        self.position_x = position_x
        self.position_y = position_y
        self.length = length
        self.width = width
        self.slot = [0, 0, 0]
        self.battery = [0, 0, 0]
        self.charge_flag = [0, 0, 0]

    def render(self, display, position, size):
        pygame.draw.rect(display, (104, 85, 108), (position, size), 0)

    def get_charge(self, battery):
        if battery == 0:
            if self.slot[0] == 0:
                self.slot[0] = 1
                print("The drone is in NO.1 slot")
                self.battery[0] = battery
                if self.battery[0] == 0:
                    self.charge_flag[0] = 1
                    print('charge station is ready')
                else:
                    self.charge_flag[0] = 0
            elif self.slot[1] == 0:
                self.slot[1] = 1
                print("The drone is in NO.2 slot")
                self.battery[1] = battery
                if self.battery[1] == 0:
                    self.charge_flag[1] = 1
                    print('charge station is ready')
                else:
                    self.charge_flag[1] = 0
            elif self.slot[2] == 0:
                self.slot[2] = 1
                print("The drone is in NO.3 slot")
                self.battery[2] = battery
                if self.battery[2] == 0:
                    self.charge_flag[2] = 1
                    print('charge station is ready')
                else:
                    self.charge_flag[2] = 0
            else:
                print("Charge station is full.")


    def charge(self):
        while self.charge_flag[0]:
            if self.battery[0] >= 100:
                self.charge_flag[0] = 0
                print('NO.1 slot: Charge is finished!')
            else:
                self.battery[0] += 2
                print('NO.1 slot: battery is charging: ', self.battery[0])
            time.sleep(0.2)
        while self.charge_flag[1]:
            if self.battery[1] >= 100:
                self.charge_flag[1] = 0
                print('NO.2 slot:Charge is finished!')
            else:
                self.battery[1] += 2
                print('NO.2 slot:battery is charging: ', self.battery[1])
            time.sleep(0.2)
        while self.charge_flag[2]:
            if self.battery[2] >= 100:
                self.charge_flag[2] = 0
                print('NO.3 slot:Charge is finished!')
            else:
                self.battery[2] += 2
                print('NO.3 slot:battery is charging: ', self.battery[2])
            time.sleep(0.2)


    def run(self):
        t1 = threading.Thread(target=self.charge())
        t1.start()


