import pygame


class Camera:
    def __init__(self, screen_resolution, scroll_size, screen_margin=30, camera_speed=10):
        self.screen_margin = screen_margin
        self.pos_x = 0
        self.pos_y = 0
        self.camera_speed = camera_speed
        self.screen_resolution = screen_resolution
        self.scroll_size = scroll_size

    def move(self):

        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.pos_y += self.camera_speed
        if key[pygame.K_LEFT]:
            self.pos_x += self.camera_speed
        if key[pygame.K_DOWN]:
            self.pos_y -= self.camera_speed
        if key[pygame.K_RIGHT]:
            self.pos_x -= self.camera_speed

        if self.pos_x < self.screen_resolution["WIDTH"] - self.scroll_size["WIDTH"] - self.screen_margin:
            self.pos_x = self.screen_resolution["WIDTH"] - self.scroll_size["WIDTH"] - self.screen_margin
        elif self.pos_x > self.screen_margin:
            self.pos_x = self.screen_margin
        elif self.pos_y < self.screen_resolution["HEIGHT"] - self.scroll_size["HEIGHT"] - self.screen_margin:
            self.pos_y = self.screen_resolution["HEIGHT"] - self.scroll_size["HEIGHT"] - self.screen_margin
        elif self.pos_y > self.screen_margin:
            self.pos_y = self.screen_margin

        return self.pos_x, self.pos_y
