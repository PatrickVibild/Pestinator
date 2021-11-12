import pygame
from camera import Camera
from fieldgenerator import FieldGenerator
from drone import Drone

pygame.init()

def Main(display, clock):
    field = FieldGenerator(150, 150, initial_infection=1.0)

    drone_scan = Drone(field, 'scan')
    drone_scan.run()

    drone_spray = Drone(field, 'spray')
    drone_spray.run()

    camera = Camera(screen_margin=50, camera_speed=20, screen_resolution=screen_resolution, scroll_size=scroll_size )
    field.run()

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        camera_pos = camera.move()
        display.fill(colors["WHITE"])
        surface = pygame.surfarray.make_surface(field.obtain_render_image())
        # keeps the layer of the image. that is been render.
        display.blit(surface, camera_pos)
        drone_scan.render(display, camera_pos)
        drone_spray.render(display, camera_pos)
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
        "WIDTH": 150 * 6, # TODO - make this pixel multiplication constant in entire project. Been spread across multiple classes
        "HEIGHT": 150 * 6
    }
    global screen_resolution
    screen_resolution = {
        "WIDTH": 1000,
        "HEIGHT": 1000
    }
    display = pygame.display.set_mode((screen_resolution["WIDTH"], screen_resolution["HEIGHT"]))
    pygame.display.set_caption("Pestinator")
    clock = pygame.time.Clock()

    Main(display, clock)
