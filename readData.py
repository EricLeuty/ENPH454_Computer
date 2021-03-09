
import json
import pandas as pd




# settings for data
# if true, then program will print data and error messages to terminal
VERBOSE = 0
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
def processconfiginfo():
    configInfo = readconfiginfo()
    sensors = []
    for sensor in configInfo["Sensors"]:
        if VERBOSE:
            print(configInfo["Sensors"][sensor]["Name"])
        sensors.append(configInfo["Sensors"][sensor])
    return sensors





