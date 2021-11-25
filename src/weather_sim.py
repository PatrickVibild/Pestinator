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
        self.__past_visibility = 0
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
        with open("cph.csv", 'r') as file:
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
        return round(random.random(),2) < M.RainDays/30
    
    def get_cloud_coverage(self, month):
        M = getattr(self.seed, self.month_dict[int(month)]) 
        if random.random() < M.Sunshine:
            return 0.0
        else: return round(random.random(),2) * 100 
    
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
        return temp

    def get_wind(self,month):
        M = getattr(self.seed, self.month_dict[int(month)])
        wind_speed = round(random.random(),2)*M.WindSpeed*2
        wind_direction = round(random.random(),2)*360
        return wind_speed, wind_direction

    

    def predict(self, month, day, time):
        self.seed= self.load_seed()
        M = getattr(self.seed, self.month_dict[int(month)])
        M_next = getattr(self.seed, self.month_dict[int(month)+1])
        if self.__past_forecast:
            self.elapsed_time = time-self.__past_time
        self.night = self.is_it_night(month,time)
        self.rain_state = self. is_it_raining(month)
        if self.rain_state:
            self.rain_mm = round(np.random.normal(M.RainAvg/(24*4),M.RainAvg/(24*20*4)),2)
            self.cloud_coverage = 100.0
        else:
            self.cloud_coverage = self.get_cloud_coverage(month)
        if self.cloud_coverage < 0.2:
            self.sun = True
        self.temperature = self.get_temperature(month,time)
        [self.wind_speed,self.wind_direction] = self.get_wind(month)


    def print_forecast(self):
        print("Wind speed: ",self.wind_speed)
        print("Wind direction: ",self.wind_direction)
        print("Raining?: ",self.rain_state)
        print("Rain mm: ",self.rain_mm)
        print("Temperature: ",self.temperature)
        print("Visibility: ",self.visibility)
        print("Cloud coverage: ",self.cloud_coverage)
        if self.night:
            print("Night")
        else: print("Day")
    
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
            fc.print_forecast()
            Event('weather', fc)
            hour += inter
            self.month,self.day,self.hour=self.correct_time(self.month,self.day,self.hour)
            count += 1
            sleep(Chronos.weather_waiting())
    def run(self):
        tl = threading.Thread(target=self.prediction_pipeline)
        tl.start()
