#%%
import numpy as np
import csv
import random
from time import sleep
import threading
from event import Event
from chronos import Chronos


#%%

#%%


class Forecast:
    class Month:
        def __init__(self,h,r):
            j=0
            for attribute in h:
                setattr(self,attribute,float(r[j]))
                j= j+1
        
        
    class Seed:
        def __init__(self):
            self.months = 12
    
    month_dict = { 1 : "january",
                        2 : "february",
                        3 : "march",
                        4 : "april",
                        5 : "may",
                        6 : "june",
                        7 : "july",
                        8 : "august",
                        9 : "september",
                        10 : "october",
                        11 : "november",
                        12 : "december"
                    }

    def __init__(self,month, day,hour,interval):
        self.wind_speed = 0
        self.wind_direction = 0
        self.rain_state = False
        self.rain_mm = 0
        self.temperature = 0
        self.visibility = 0
        self.cloud_coverage = 0
        self.sun = False
        self.night = False

        self.__past_forecast = False
        self.__past_month = 0
        self.__past_time = 0
        self.__past_wind_speed = 0
        self.__past_wind_direction = 0
        self.__past_rain_state = False
        self.__past_rain_mm = 0
        self.__past_temperature = 0
        self.__past_visibility = 100
        self.__past_cloud_coverage = 0
        self.__past_sun = False
        self.__past_night = False

        self.elapsed_time = 0
        self.month = month
        self.day = day
        self.hour = hour
        self.interval = interval
    def load_seed(self):

        rows = []
        seed = self.Seed()
        months_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
                       "november", "december"]
        #os.system("pwd")
        with open("src/cph.csv", 'r') as file:
            csvred = csv.reader(file)
            header = next(csvred)
            it = 0
            for row in csvred:
                rows.append(row)
                temp = self.Month(header,row)
                setattr(seed,months_list[it],self.Month(header,row))
                # print(it,months_list[it])
                # print(row)
                it = it +1
        return seed
                
    def is_it_night(self, month, time):
        M = getattr(self.seed, self.month_dict[int(month)])
        if time > M.Dawn and time < M.Sunset:
            return False
        else: return True
    
    def is_it_raining(self,month):
        M = getattr(self.seed, self.month_dict[int(month)])
        if self.__past_forecast:
            return 0.8*self.__past_rain_mm +0.2*round(random.random(),2) < M.RainDays/30
        else: return round(random.random(),2) < M.RainDays/30
    
    def get_cloud_coverage(self, month):
        M = getattr(self.seed, self.month_dict[int(month)]) 
        if self.__past_forecast:
            temp = 0.9*self.__past_cloud_coverage + random.choice((-1,1))*0.1*random.random()*100
            if temp < M.Sunshine:
                return 0.0
            else: return round(temp,2)
        elif random.random()*100 < M.Sunshine: 
            return 0.0
        else:
            return round(random.random(),2) * 100 
    
    def get_temperature(self, month, time):
        M = getattr(self.seed, self.month_dict[int(month)])
        Tmax = M.Tmax
        Tmin = M.Tmin
        Tmean = M.Tmean
        Trange = Tmax - Tmin
        Tmin_calc = Tmin
        Tmax_calc = Tmax
        # TODO: time correction
        if self.night:
            Tmax_calc = Tmean
        else:
            Tmin_calc = Tmin + 0.2*Trange
        if self.cloud_coverage < 0.5:
            Tmin_calc = Tmin_calc + (1-self.cloud_coverage)*0.25*Trange
        
        temp = Tmin_calc + round(random.random(),2)*(Tmax_calc-Tmin_calc)
        return round(temp,2)

    def get_wind(self,month):
        M = getattr(self.seed, self.month_dict[int(month)])
        if self.__past_forecast:
            wind_speed = 0.8 * self.__past_wind_speed + random.choice((-1,1))*0.2*round(random.random(),2)*M.WindSpeed*2
            wind_direction = 0.9 * self.__past_wind_direction + random.choice((-1,1))*0.1*round(random.random(),2)*360
            if wind_direction > 360:
                wind_direction = wind_direction - 360
            elif wind_direction < 0:
                wind_direction = 360 + wind_direction
            if wind_speed < 0:
                wind_speed = 0
        else:
            wind_speed = round(random.random(),2)*M.WindSpeed*2
            wind_direction = round(random.random(),2)*360
        return round(wind_speed,2), round(wind_direction,2)

    def get_visibility(self):
        max = 100
        minim = 30
        if self.rain_state:
            max -= 10
            if self.wind_speed > 5:
                max = 60
        elif self.cloud_coverage > 80:
            max -= 5
        else: minim = 50
        if self.sun:
            minim = 60
            max = 100
        if self.wind_speed > 3 and not self.rain_state:
            minim += 30
        if self.night:
            max = 30
            minim = 0
        if not self.night and self.__past_night:
            self.__past_visibility = 60
        if self.__past_forecast:
            vis = 0.5*self.__past_visibility + 0.5*random.randint(minim,max)
        else: vis = random.randint(minim,max)
        if vis > 100: vis = 100
        elif vis < 0: vis = 0
        
        return round(vis,2)

    def predict(self, month, day, time):
        self.seed= self.load_seed()
        M = getattr(self.seed, self.month_dict[int(month)])
        M_next = getattr(self.seed, self.month_dict[int(month)+1])
        if self.__past_forecast:
            self.elapsed_time = time-self.__past_time
            self.update_past_forecast()
        self.night = self.is_it_night(month,time)
        self.rain_state = self. is_it_raining(month)
        if self.rain_state:
            if self.__past_forecast:
                self.rain_mm = round(0.8*self.__past_rain_mm + 0.2*random.choice((-1,1))*round(np.random.normal(M.RainAvg,M.RainAvg/(3))*self.interval/12,2),2)
                if self.rain_mm > 100: self.rain_mm = 100
                elif self.rain_mm < 0: 
                    self.rain_mm = 0
                    self.rain_state = False
            else:
                self.rain_mm = round(np.random.normal(M.RainAvg,M.RainAvg/(3))*self.interval/12,2)
            self.cloud_coverage = 100.0
        else: 
            self.cloud_coverage = self.get_cloud_coverage(month)
            self.rain_mm = 0.0
        if self.cloud_coverage < 0.2:
            self.sun = True
        self.temperature = self.get_temperature(month,time)
        [self.wind_speed,self.wind_direction] = self.get_wind(month)
        self.visibility = self.get_visibility()
        if not self.__past_forecast:
            self.__past_forecast = True

    def update_past_forecast(self):

        self.__past_month = self.month
        self.__past_time = self.hour
        self.__past_wind_speed = self.wind_speed
        self.__past_wind_direction = self.wind_direction
        self.__past_rain_state = self.rain_state
        self.__past_rain_mm = self.rain_mm
        self.__past_temperature = self.temperature
        self.__past_visibility = self.visibility
        self.__past_cloud_coverage = self.cloud_coverage
        self.__past_sun = self.sun
        self.__past_night = self.night

    def print_forecast(self):
        if self.night:
            print("Night")
        else: print("Day")
        print("Wind speed: ",self.wind_speed)
        print("Wind direction: ",self.wind_direction)
        print("Raining?: ",self.rain_state)
        print("Rain mm: ",self.rain_mm)
        print("Temperature: ",self.temperature)
        print("Visibility: ",self.visibility)
        print("Cloud coverage: ",self.cloud_coverage)
    
    def correct_time(self,month, day, hour):
        if hour > 24: 
            day += 1
            hour = hour - 24
        if day > 31: 
            month += 1
            day = day - 31
        if month > 12:
            month = month - 12
        return month, day, hour

    def prediction_pipeline(self):
        fc=Forecast(self.month,self.day,self.hour,self.interval)
        # month = int(input("Starting month (number): "))
        month = self.month
        # day = int(input("Starting day (number): "))
        day = self.day
        # hour = float(input("Starting hour (number): "))
        hour = self.hour
        self.month,self.day,self.hour=fc.correct_time(self.month, self.day, self.hour)
        # inter = float(input("Simulation interval: "))
        inter = self.interval
        seed = fc.Seed()
        count = 0
        while True:
            fc.predict(self.month,self.day,self.hour)
            #fc.print_forecast()
            Event('weather', fc)
            self.hour += self.interval
            self.month,self.day,self.hour=self.correct_time(self.month,self.day,self.hour)
            count += 1
            sleep(Chronos.weather_waiting())
    def run(self):
        tl = threading.Thread(target=self.prediction_pipeline)
        tl.start()
