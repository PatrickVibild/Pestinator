import threading
from observer import Observer
import matplotlib.pyplot as plt
import numpy as np
import time

class Data_visualizer(Observer):
    def __init__(self, interval):
        self.field_data = np.array([[100,0,0,0]])
        self.interval = interval
        Observer.__init__(self)
        self.spray_quantity = 0
        self.observe('spray', self.spray_callback)# Listening to events 'spray' and calling method cure if trigger
        self.observe('field_data', self.field_callback)
        self.colormap = ["#c8c8c8", "#ff0000", "#ffa500", "#00ff00"]
        self.labels_field = ["Dead ", "Critical", "Infected", "Healthy"]
        
    def spray_callback(self):
        self.spray_quantity += 1

    def field_callback(self, data_list):
        np_data = np.array(data_list)/(15*15)
        self.field_data= np.vstack([self.field_data, np_data])

    def plot_data(self):
        x_axis = np.arange(0,len(self.field_data)*self.interval,self.interval)
        plt.stackplot(x_axis, self.field_data[:,3],self.field_data[:,2],self.field_data[:,1],self.field_data[:,0],colors=self.colormap, labels=self.labels_field)
        plt.legend(loc='upper left')
        plt.title("Field crops' health evolution")
        plt.xlabel('Hours')
        plt.ylabel('Number of crops')
        plt.savefig('field_data.png')
    def data_plot_pipeline(self):
        
        while True:
            try:
                pass
            except KeyboardInterrupt:
                self.plot_data()

    def run(self):
        t1 = threading.Thread(target=self.data_plot_pipeline)
        t1.start()