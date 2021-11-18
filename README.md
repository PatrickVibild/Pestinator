## Forecast class documentation
### Instantiation 

```
from weather_sim.py import forecast
foo = forecast(month, day, hour, interval)
```
### Usage
```
foo.run()
```
```
from observer import Observer
Observer.__init__(self)
observe('weather', self.weather_update)
```
And then define the desired callback function weather_update.
### Attributes

```forecast.cloud_coverage```: type: float, default: 0 . From 0 (no clouds) to 100 (fully covered).

```forecast.day```: type: float, run() argument. Day of the month (1 - 31) when the forecast is calculated.

```forecast.elapsed_time```: type: float, default: 0 . Time in hours since last forecast.

```forecast.hour```: type: float, run() argument. Hour of the day (0 - 24) when the forecast is calculated.

```forecast.interval```: type: float, run() argument. Time step of the simulation in hours, how many hours will pass from forecast to the next one. Time step size is fixed for the whole simulation.

```forecast.month```: type: float, run() argument. Month of the year (1 - 12) when the forecast is calculated.

```forecast.night```: type: bool, default: False . True when it is night (after sunset and before dawn).

```forecast.rain_mm```: type: float, default: 0 . Indicates the amount of rain in mm for the given time interval.

```forecast.rain_state```: type: bool, default: False . True when it is raining.

```forecast.sun```: type: bool, default: False . True when it is sunny.

```forecast.temperature```: type: float, default: 0 . Temperature in Celsius degrees.

```forecast.visibility```: type: float, default: 0 . From 0 (no visibility) to 100 (perfect visibility).

```forecast.wind_direction```: type: float, default: 0 . Angle in degrees of wind direction (0 - 360).

```forecast.wind_speed```: type: float, default: 0 . Speed in m/s of the wind.


