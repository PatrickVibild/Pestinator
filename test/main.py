import pygame
from camera import Camera
from fieldgenerator import FieldGenerator
from drone import Drone
from chargestation import ChargeStation

pygame.init()

def Main(display, clock):
    field = FieldGenerator(400, 400, initial_infection=1.0)

    drone = Drone(field)
    drone.run()

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
        drone.render(display, camera_pos)
        pygame.display.flip()

        #get battery info
        chargestation.get_charge(drone.battery)
        if chargestation.charge_flag[0] == 1:
            chargestation.run()
        if chargestation.charge_flag[0] == 0 and chargestation.battery[0] == 100:
            drone.battery = chargestation.battery[0]
            chargestation.battery[0] = 0
            chargestation.slot[0] = 0
            drone.run()


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
        "WIDTH": 400 * 6, # TODO - make this pixel multiplication constant in entire project. Been spread across multiple classes
        "HEIGHT": 400 * 6
    }
    global screen_resolution
    screen_resolution = {
        "WIDTH": 1820,
        "HEIGHT": 980
    }
    display = pygame.display.set_mode((screen_resolution["WIDTH"], screen_resolution["HEIGHT"]))
    pygame.display.set_caption("Pestinator")
    clock = pygame.time.Clock()

    Main(display, clock)
