import time

import pygame
from camera import Camera
from fieldgenerator import FieldGenerator
from chargestation import ChargeStation
from scanningdrone import ScanningDrone
from spraydrone import SprayingDrone
from WeatherDisplay import WeatherDisplay
from chronos import Chronos
from scanning_map import ScanningMap
from parameters import Parameters
from weather_sim import Forecast
from spraying_organizer import Spraying_Organizer

from data_acq import Data_visualizer

pygame.init()

no_sprayingdrones = Parameters.nr_spraying_drones
no_scanningdrones = Parameters.nr_scanning_drones


def Main(display, clock):
    interval = 1
    data = Data_visualizer(interval)
    data.run()

    general_time = Chronos()
    field = FieldGenerator(150, 150, initial_infection=Parameters.initial_infection, spread_times=6)

    charge_station = ChargeStation(capacity=Parameters.charging_station_capacity, charging_speed=80)
    charge_station.run()

    fc = Forecast(6, 4, 10, interval)

    spraying_organizer = Spraying_Organizer(field)
    scanning_map = ScanningMap(150, 150)

    scanning_drones = [ScanningDrone(field, fc, routine=Parameters.scanning_routine, scanning_map=scanning_map) for i in
                       range(no_scanningdrones)]


    spraying_drones = [SprayingDrone(field, spraying_organizer, i, grid=(not Parameters.precision_spraying)) for i in range(no_sprayingdrones)]


    camera = Camera(screen_margin=50, camera_speed=20, screen_resolution=screen_resolution, scroll_size=scroll_size)
    field.run()

    fc.run()

    weather_display = WeatherDisplay()
    # we sleep so we can normalize the values of the map.
    time.sleep(10)
    for drone_spray in spraying_drones:
        drone_spray.run()
    for drone_scan in scanning_drones:
        drone_scan.run()
    while True:
        try:
            clock.tick(30)
            general_time.get_input()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            camera_pos = camera.move()

            if weather_display.wind:
                background_color = colors["LIGHT_BLUE"] if weather_display.day_light else colors["DARK_BLUE"]
            else:
                background_color = colors["WHITE"] if weather_display.day_light else colors["BLACK"]
            display.fill(background_color)

            surface = pygame.surfarray.make_surface(field.obtain_render_image())
            # keeps the layer of the image. that is been render.
            display.blit(surface, camera_pos)
            for drone_scan in scanning_drones:
                drone_scan.render(display, camera_pos)

            for drone_spray in spraying_drones:
                drone_spray.render(display, camera_pos)
            pygame.display.flip()
        except KeyboardInterrupt:
            # data.plot_data()
            exit()


if __name__ in "__main__":
    global colors
    colors = {
        "WHITE": (255, 255, 255),
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "LIGHT_BLUE": (173, 216, 230),
        "DARK_BLUE": (0, 0, 139),
        "BLACK": (0, 0, 0)
    }
    global scroll_size
    scroll_size = {
        "WIDTH": 150 * 6,
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
