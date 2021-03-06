import json
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# settings for data
# if true, then program will print data and error messages to terminal
VERBOSE = 0
# base name for program to write files to in the current directory
FILE_HEAD_NAME = 'test_'


def readconfiginfo():
    file_path = './Data/' + FILE_HEAD_NAME + 'start.json'
    try:
        file = open(file_path, 'r')
        configInfo = json.loads(file.read())
        if VERBOSE:
            print(configInfo)
        return configInfo
    except FileNotFoundError:
        if VERBOSE:
            print("File not found at path: ", file_path)


def readsensordata(address):
    file_path = './Data/' + FILE_HEAD_NAME + str(address) + '.csv'

    try:
        data = pd.read_csv(file_path)
        if VERBOSE:
            print(data)
        return data
    except FileNotFoundError:
        if VERBOSE:
            print("File not found at path: ", file_path)

def getalldata():
    configInfo = readconfiginfo()
    for sensor in configInfo["Sensors"]:
        name = configInfo["Sensors"][sensor]["Name"]
        address = configInfo["Sensors"][sensor]["Address"]
        data = readsensordata(address)
        print(data)


def animate(i):
    data = readsensordata(118)
    x = data["Timestamp"]
    y1 = data["Temperature"]
    y2 = data["Pressure"]

    plt.cla()

    plt.plot(x, y1, label="Temperature")
    #plt.plot(x, y2, label="Pressure")

    plt.tight_layout()


def animatedata():
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.tight_layout()
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    animatedata()
