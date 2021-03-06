import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from readData import *

# settings for data
# if true, then program will print data and error messages to terminal
VERBOSE = 0
# base name for program to write files to in the current directory
FILE_HEAD_NAME = 'test_'


# plots a separate figure for each connected sensor
def plotdata():
    figures = []
    sensors = processconfiginfo()
    for idx in range(len(sensors)):
        figures.append(PlotSensorData(sensors[idx], idx))
    plt.show()


# class for plotting data from an individual sensor
class PlotSensorData:
    def __init__(self, sensor, num):
        self.name = sensor["Name"]
        self.address = sensor["Address"]
        self.data = readsensordata(self.address)
        self.labels = []
        self.processsensordata()
        self.fig = plt.figure(num, figsize=(10, 8), dpi=82)
        self.ax = self.fig.subplots(len(self.labels), 1)
        self.fig.tight_layout(pad=6, h_pad=4, w_pad=4)
        self.lines = []

        for idx in range(len(self.ax)):
            line = self.ax[idx].errorbar(self.data["Timestamp"], self.data[self.labels[idx]], yerr=self.geterror(self.labels[idx]), fmt='.')
            self.ax[idx].set_xlabel("Time (s)")
            self.ax[idx].set_ylabel(self.labels[idx])
            self.ax[idx].grid()
            self.lines.append(line)

    # finds and returns an array of the column labels of the dependent variables
    # it finds every column that does not contain the words: address, time, and error
    def processsensordata(self):
        column_labels = self.data.columns
        if VERBOSE:
            print(column_labels)

        search_words = ["address", "time", "error"]
        for column_label in column_labels:
            valid_label = True
            for search_word in search_words:
                if re.search(search_word, column_label.lower()) != None:
                    valid_label = False

            if valid_label:
                self.labels.append(column_label)

    # gets column label of the error for the data in column label
    def geterror(self, label):
        for column_label in self.data.columns:
            if (re.search(label, column_label.lower()) != None):
                if (re.search("error", column_label.lower) != None):
                    return self.data[column_label]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    plotdata()
