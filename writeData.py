import serial
from os import path
import csv
import json

# settings for data
# if true, then program will print data and error messages to terminal
VERBOSE = 1
# base name for program to write files to in the current directory
FILE_HEAD_NAME = 'test_'
# IMPORTANT
# path of port that arduino is connected to
# Windows path is 'COM*' *is a number
# Linux path is '/dev/tty*'
ARDUINO_PORT = '/dev/ttyACM0'


# opens serial connection with arduino uno and
# writes the data to files
def readarduinoserial():
    try:
        arduino = serial.Serial(port=ARDUINO_PORT, baudrate=9600, timeout=.1)
    except serial.serialutil.SerialException:
        print("Arduino not found on port : ", ARDUINO_PORT)
        return

    while True:
        serial_data = arduino.readline().decode('utf-8')
        if serial_data != '':
            if VERBOSE:
                print(serial_data)
            convertserialdata(serial_data)


# converts data from json to dictionary
def convertserialdata(serial_data):
    try:
        data_dictionary = json.loads(serial_data)
        sortarduinoserialdata(data_dictionary)
    except json.JSONDecodeError:
        if VERBOSE:
            print("not a json")


# sorts data in data_dictionary and calls writedatajson or writedatacsv
# to write it to a file in the correct format
def sortarduinoserialdata(data_dictionary):
    file_path = './Data/' + FILE_HEAD_NAME
    if "Start Time" in data_dictionary:
        file_path = file_path + 'start.json'
        writedatajson(data_dictionary, file_path)
    elif "Address" in data_dictionary:
        if data_dictionary["Address"] == 64 or data_dictionary["Address"] == 65:
            data_dictionary = calculatepower(data_dictionary)
        file_path = file_path + str(data_dictionary.get("Address")) + '.csv'
        writedatacsv(data_dictionary, file_path)


# writes data in data_dictionary_arg to json file at path file_path_arg
def writedatajson(data_dictionary_arg, file_path_arg):
    if VERBOSE:
        print("writing data as csv to path: ", file_path_arg)

    file = open(file_path_arg, 'w')
    json.dump(data_dictionary_arg, file)
    file.close()


# writes data in data_dictionary_arg to csv file at path file_path_arg
def writedatacsv(data_dictionary_arg, file_path_arg):
    if VERBOSE:
        print("writing data as csv to path: ", file_path_arg)

    field_names = data_dictionary_arg.keys()
    if not path.exists(file_path_arg):
        file = open(file_path_arg, 'w')
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        file.close()

    file = open(file_path_arg, 'a')
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writerow(data_dictionary_arg)
    file.close()


def calculatepower(data_dictionary):
    voltage = data_dictionary["Voltage (V)"]
    current = data_dictionary["Current (A)"]
    volt_err = data_dictionary["Voltage Error"]
    curr_err = data_dictionary["Current Error"]
    power = voltage * current
    power_err = ((abs(voltage)*curr_err)**2 + (abs(current)*volt_err)**2)**0.5
    data_dictionary["Power (W)"] = power
    data_dictionary["Power Error"] = power_err
    return data_dictionary


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    readarduinoserial()

