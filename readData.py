import re
import time
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# settings for data
# if true, then program will print data and error messages to terminal
VERBOSE = 1
# base name for program to write files to in the current directory
FILE_HEAD_NAME = 'test_'


# reads configinfo from file
def readconfiginfo():
    file_path = './Data/' + FILE_HEAD_NAME + 'start.json'
    try:
        file = open(file_path, 'r')
        configInfo = json.load(file)
        file.close()
        if VERBOSE:
            print(configInfo)
        return configInfo
    except FileNotFoundError:
        if VERBOSE:
            print("File not found at path: ", file_path)


# reads data for sensor at address from file
def readsensordata(address):
    file_path = './Data/' + FILE_HEAD_NAME + str(address) + '.csv'

    try:
        dataframe = pd.read_csv(file_path)
        if VERBOSE:
            print(dataframe)
        return dataframe
    except FileNotFoundError:
        if VERBOSE:
            print("File not found at path: ", file_path)


# finds and returns an array of the sensor addresses
def processconfiginfo(configInfo):
    sensors = []
    for sensor in configInfo["Sensors"]:
        if VERBOSE:
            print(configInfo["Sensors"][sensor]["Name"])
        sensors.append(configInfo["Sensors"][sensor])
    return sensors


# finds and returns an array of the column labels of the dependent variables
# it finds every column that does not contain the words: address, time, and error
def processsensordata(dataframe):
    column_labels = dataframe.columns
    if VERBOSE:
        print(column_labels)

    valid_labels = []
    search_words = ["address", "time", "error"]
    for column_label in column_labels:
        valid_label = True
        for search_word in search_words:
            if(re.search(search_word, column_label.lower()) != None):
                valid_label = False

        if valid_label:
            valid_labels.append(column_label)

    return valid_labels

class PlotSensorData(animation.FuncAnimation):
    def __init__(self, address):
        self.address = address
        self.data = readsensordata(self.address)
        self.labels = processsensordata(self.data.head())
        fig = plt.figure()
        self.ax = fig.subplots(len(self.labels), 1)
        self.lines = []

        for idx in range(len(self.ax)):
            line = self.ax[idx].errorbar([], [], yerr=([], []), fmt='.')
            self.ax[idx].set_xlabel("Time (s)")
            self.ax[idx].set_ylabel(self.labels[idx])
            self.lines.append(line)

        animation.FuncAnimation.__init__(self, fig, func=self._draw_frame, interval=50, repeat=True)

    def _init_draw(self):
        for idx in range(len(self.labels)):
            self.lines[idx][0].set_xdata([])
            self.lines[idx][0].set_ydata([])

    def _draw_frame(self, framedata):
        i = framedata
        self.data = readsensordata(self.address)
        for idx in range(len(self.labels)):
            self.lines[idx][0].set_xdata(self.data["Timestamp"].tail(120))
            self.lines[idx][0].set_ydata(self.data[self.labels[idx]].tail(120))
            self.ax[idx].relim()
            self.ax[idx].autoscale_view()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    #ani = animation.FuncAnimation(fig, func, init_func=init, interval=1000, frames=25, repeat=True)
    ani = PlotSensorData(118)
    plt.show()


