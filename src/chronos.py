import pygame.key


def bound(value, min_v, max_v):
    return max(min(value, max_v), min_v)


class Chronos:
    time = 1
    drone_cycle = 0.2
    field_cycle = 180
    weather_cycle = 90
    charging_cycle = 0.5

    def __init__(self):
        self.max_time = 20

    def get_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_1]:
            Chronos.time += 1
        if key[pygame.K_2]:
            Chronos.time -= 1

        Chronos.time = bound(Chronos.time, 1, self.max_time)

    @staticmethod
    def drone_waiting():
        return Chronos.drone_cycle / Chronos.time

    @staticmethod
    def field_waiting():
        return Chronos.field_cycle / Chronos.time

    @staticmethod
    def weather_waiting():
        return Chronos.weather_cycle / Chronos.time

    @staticmethod
    def charging_waiting():
        return Chronos.charging_cycle / Chronos.time
