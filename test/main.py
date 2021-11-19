import pygame
from camera import Camera
from fieldgenerator import FieldGenerator
from chargestation import ChargeStation
from scanningdrone import ScanningDrone
from spraydrone import SprayingDrone
from weather_sim import forecast
pygame.init()

no_sprayingdrones = 3
no_scanningdrones = 3

def Main(display, clock):
    field = FieldGenerator(150, 150, initial_infection=-1)

    charge_station = ChargeStation(capacity=2, charging_speed=5)
    charge_station.run()

    # drone_scan = ScanningDrone(field)
    # drone_scan.run()
    #
    # drone_spray = SprayingDrone(field)
    # drone_spray.run()

    scanning_drones = [ScanningDrone(field) for i in range(no_scanningdrones)]
    for drone_scan in scanning_drones:
        drone_scan.run()

    spraying_drones = [SprayingDrone(field) for i in range(no_sprayingdrones)]
    for drone_spray in spraying_drones:
        drone_spray.run()

    camera = Camera(screen_margin=50, camera_speed=20, screen_resolution=screen_resolution, scroll_size=scroll_size)
    field.run()

    fc = forecast(6, 4, 10, interval=0.5) # interval is every hours. in this case 0.5 is 30min.
    fc.run()

    while True:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        camera_pos = camera.move()
        display.fill(colors["WHITE"])
        surface = pygame.surfarray.make_surface(field.obtain_render_image())
        # keeps the layer of the image. that is been render.
        display.blit(surface, camera_pos)

        for drone_scan in scanning_drones:
            drone_scan.render(display, camera_pos)

        for drone_spray in spraying_drones:
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
