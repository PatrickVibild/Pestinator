import random
import pygame


class RandomAgent:
    def __init__(self, width, height, max_width, max_height):
        self.width = width
        self.height = height
        self.max_width = max_width
        self.max_height = max_height
        self.x = max_width / 2
        self.y = max_height / 2

    def action(self, sim_window):
        direction = random.randint(0, 3)
        distance = random.randint(1, 5)
        if direction == 0:
            self.x += distance
        if direction == 1:
            self.x -= distance
        if direction == 2:
            self.y += distance
        if direction == 3:
            self.y -= distance
        self.__apply_boundaries()
        pygame.draw.rect(sim_window, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def __apply_boundaries(self):
        def bound(low, high, value):
            return max(low, min(high, value))

        self.x = bound(0, self.max_width, self.x)
        self.y = bound(0, self.max_height, self.y)
