import threading
from observer import Observer
import matplotlib.pyplot as plt
import numpy as np
from chronos import Chronos
import time

class Data_visualizer(Observer):
    def __init__(self, interval):
        self.loop_count = 0
        self.field_data = np.array([[100,0,0,0]])
        self.instant_field_data = np.array([[225000,0,0,0]])
        self.interval = interval
        self.detections = np.zeros((150,150))
        self.spray_field = np.zeros((150,150))
        self.detections_data = np.array([0])
        self.detections_cnt = 0
        self.detections_percentage = np.array([0])
        Observer.__init__(self)
        self.spray_quantity = 0
        self.spray_data = np.array([10])
        self.observe('spray', self.spray_callback)# Listening to events 'spray' and calling method cure if trigger
        self.observe('field_data', self.field_callback)
        self.observe('sick_plant', self.detection_callback)
        self.colormap = ["#c8c8c8", "#ff0000", "#ffa500", "#00ff00"]
        self.labels_field = ["Dead ", "Critical", "Infected", "Healthy"]
        
    def spray_callback(self, pair):
        self.spray_quantity += 1
        self.detections[pair[0],pair[1]] = 0
        self.spray_field[pair[0],pair[1]] += 1

    def detection_callback(self, pair):
        self.detections[pair[0],pair[1]] = 1

    def field_callback(self, data_list):
        np_data = np.array(data_list)/(15*15)
        self.instant_field_data = np.array(data_list)
        self.field_data= np.vstack([self.field_data, np_data])

    def plot_data_field(self):
        x_axis = np.arange(0,len(self.spray_data),step = len(self.spray_data)/len(self.field_data))
        while len(x_axis) > len(self.spray_data):
            x_axis[-1] = None
        plt.stackplot(x_axis, self.field_data[:,3],self.field_data[:,2],self.field_data[:,1],self.field_data[:,0],colors=self.colormap, labels=self.labels_field)
        plt.legend(loc='upper left')
        plt.title("Field crops' health evolution")
        plt.xlabel('Hours')
        plt.ylabel('Crops [%]')
        plt.savefig('field_data.png')
        plt.ylim(top = 20)
        plt.savefig('field_data_closeup.png')

    def plot_data_spray(self):
        plt.clf()
        x_axis = np.arange(0,len(self.spray_data),step = 1)
        plt.plot(x_axis,self.spray_data)
        plt.title("Spray usage")
        plt.xlabel('Hours')
        plt.ylabel('Spray actions')
        plt.savefig('spray_data.png')

    def plot_data_detection(self):
        plt.clf()
        x_axis = np.arange(0,len(self.detections_data),step = 1)
        plt.plot(x_axis,self.detections_data)
        plt.title("Scanning performance")
        plt.xlabel('Hours')
        plt.ylabel('Detected crops [%]')
        plt.savefig('detection_data.png')

    def plot_spray_histogram(self):
        plt.clf()
        plt.pcolormesh(self.spray_field, cmap = plt.cm.inferno)
        plt.colorbar()
        bl_act = int((self.spray_quantity/168)*22500)
        if bl_act == 0: percent = 0.
        else: percent = 100-round((self.spray_quantity/bl_act)*100,2)
        # plt.xlabel(str(self.spray_data[-1])+' spray activations, '+str(percent)+'%% saved.')
        plt.savefig('spray_histogram.png')

    def plot_data(self):
        print("--------------------Plotting...-------------------")
        self.plot_data_field()
        self.plot_data_spray()
        self.plot_data_detection()
        self.plot_spray_histogram()
        print("----------------Plotting finished----------------- \n ----------------------------------------------------------------\n ----------------------------------------------------------------\n ----------------------------------------------------------------\n ----------------------------------------------------------------\n")

    def update_data(self):
        self.spray_data = np.vstack([self.spray_data, self.spray_quantity])
        if np.sum(self.instant_field_data[1:4]) != 0:
            self.detections_percentage = (np.sum(self.detections)/(np.sum(self.instant_field_data[1:4])))*100
        if self.detections_percentage > 100: self.detections_percentage = 100
        self.detections_data = np.vstack([self.detections_data, self.detections_percentage])

    def data_plot_pipeline(self):
        
        while True:
            try:
                if self.loop_count > 24*7*2: # hours/day * days/week * weeks of simulation 
                    self.plot_data()
                    exit()
                time.sleep(Chronos.data_waiting())
                self.update_data()
                self.loop_count += 1

            except KeyboardInterrupt:
                self.plot_data()

    def run(self):
        t1 = threading.Thread(target=self.data_plot_pipeline)
        t1.start()