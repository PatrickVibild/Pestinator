import threading
from observer import Observer
import matplotlib.pyplot as plt
import numpy as np


class Data_visualizer(Observer):
    def __init__(self, interval):
        self.field_data = np.array([[100, 0, 0, 0]])
        self.interval = interval
        self.detections = np.array([0, 0])
        self.detections_data = np.array([0])
        self.detections_cnt = 0
        Observer.__init__(self)
        self.spray_quantity = 0
        self.spray_data = np.array([10])
        self.observe('spray', self.spray_callback)  # Listening to events 'spray' and calling method cure if trigger
        self.observe('field_data', self.field_callback)
        self.observe('sick_plant', self.detection_callback)
        self.colormap = ["#c8c8c8", "#ff0000", "#ffa500", "#00ff00"]
        self.labels_field = ["Dead ", "Critical", "Infected", "Healthy"]

    def spray_callback(self, coordinates):
        self.spray_quantity += 1

    def detection_callback(self, pair):
        if self.detections_cnt == 0:
            self.detections = np.array(pair)
            self.detections_cnt += 1
        elif not (pair == self.detections).all().any():
            self.detections = np.vstack([self.detections, pair])
            self.detections_cnt += 1

    def field_callback(self, data_list):
        np_data = np.array(data_list) / (15 * 15)
        self.field_data = np.vstack([self.field_data, np_data])
        self.spray_data = np.vstack([self.spray_data, self.spray_quantity])
        self.detections_data = np.vstack([self.detections_data, self.detections_cnt])

    def plot_data_field(self):
        self.x_axis = np.arange(0, len(self.field_data) * self.interval, self.interval)
        plt.stackplot(self.x_axis, self.field_data[:, 3], self.field_data[:, 2], self.field_data[:, 1],
                      self.field_data[:, 0], colors=self.colormap, labels=self.labels_field)
        plt.legend(loc='upper left')
        plt.title("Field crops' health evolution")
        plt.xlabel('Hours')
        plt.ylabel('Crops [%]')
        plt.savefig('field_data.png')

    def plot_data_spray(self):
        plt.clf()
        if len(self.x_axis) < len(self.spray_data):
            plt.plot(self.x_axis, self.spray_data[:-1])
        else:
            plt.plot(self.x_axis, self.spray_data)
        plt.title("Spray usage")
        plt.xlabel('Hours')
        plt.ylabel('Spray actions')
        plt.savefig('spray_data.png')

    def plot_data_detection(self):
        plt.clf()
        detections_percentage = np.divide(self.detections_data.transpose(),
                                          np.sum(self.field_data[:, 1:4], axis=1) * (15 * 15)) * 100
        if len(self.x_axis) < len(np.transpose(detections_percentage)):
            plt.plot(self.x_axis, np.transpose(detections_percentage)[:-1])
        else:
            plt.plot(self.x_axis, np.transpose(detections_percentage))
        plt.title("Scanning performance")
        plt.xlabel('Hours')
        plt.ylabel('Detected crops [%]')
        plt.savefig('detection_data.png')

    def plot_data(self):
        print("Plotting...")
        self.plot_data_field()
        self.plot_data_spray()
        self.plot_data_detection()
        print("Plotting finished")

    def data_plot_pipeline(self):

        while True:
            try:
                pass
            except KeyboardInterrupt:
                self.plot_data()

    def run(self):
        t1 = threading.Thread(target=self.data_plot_pipeline)
        t1.start()
