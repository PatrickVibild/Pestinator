import pygame

from camera import Camera

pygame.init()

def Main(display, clock):
    world = pygame.Surface((scroll_size["WIDTH"], scroll_size["HEIGHT"]))
    world.fill(colors["BLACK"])
    for x in range(10):
        pygame.draw.rect(world, colors["BLUE"], ((x * 100, x * 100), (20, 20)))
    #
    camera = Camera(screen_margin=50, camera_speed=20, screen_resolution=screen_resolution, scroll_size=scroll_size )

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        camera_pos = camera.move()

        display.fill(colors["WHITE"])  # Fill The Background White To Avoid Smearing
        world.fill(colors["BLACK"])  # Refresh The World So The Player Doesn't Smear
        for x in range(10):
            pygame.draw.rect(world, colors["BLUE"], ((x * 100, x * 100), (20, 20)))
        display.blit(world, camera_pos)
        pygame.display.flip()


if __name__ in "__main__":
    global colors
    colors = {
        "WHITE": (255, 255, 255),
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "BLUE": (0, 0, 255),
        "BLACK": (0, 0, 0)
    }
    global scroll_size
    scroll_size = {
        "WIDTH": 3000,
        "HEIGHT": 3000
    }
    global screen_resolution
    screen_resolution = {
        "WIDTH": 1820,
        "HEIGHT": 980
    }
    display = pygame.display.set_mode((screen_resolution["WIDTH"], screen_resolution["HEIGHT"]))
    pygame.display.set_caption("Scrolling Camera")
    clock = pygame.time.Clock()

    Main(display, clock)
