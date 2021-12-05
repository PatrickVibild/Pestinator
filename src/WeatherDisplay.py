from observer import Observer
from parameters import Parameters
from weather_sim import Forecast


class WeatherDisplay(Observer):
    weather = None
    day_light = True
    wind = False
    def __init__(self):
        Observer.__init__(self)
        self.observe('weather', self.weather_update)

    def weather_update(self, w_data: Forecast):
        print('Field updated the weather')
        self.weather = w_data
        self.wind = self.weather.wind_speed >= Parameters.wind_threshold
        self.day_light = not self.weather.night

