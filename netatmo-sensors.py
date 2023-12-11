#!/usr/bin/env python
import lnetatmo
import datetime

# station name as on the Netatmo web site
stationName = 'Homeworld'

# ANSI color codes
DEFAULT = '\033[0m' 
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# function just add to value ANSI color tag
def wrap_in_color_tag(val, color = None):
    if color is None:
        return f"{DEFAULT}{val}"
    else:
        return f"{color}{val}{DEFAULT}"

# coloring outputs depending of its value
def value_in_color (val, sensor):
    match sensor:
        case 'Temperature':
            if val < 3:
                return wrap_in_color_tag(val, BLUE)
            if val < 15:
                return wrap_in_color_tag(val, GREEN)
            if val < 27:
                return wrap_in_color_tag(val, YELLOW)
            else:
                return wrap_in_color_tag(val, RED)
        case 'CO2':
            if val < 500:
                return wrap_in_color_tag(val, GREEN)
            if val < 1500:
                return wrap_in_color_tag(val, YELLOW)
            else:
                return wrap_in_color_tag(val, RED)
        case 'battery_percent':
            if val < 30:
                return wrap_in_color_tag(val, RED)
            if val < 60:
                return wrap_in_color_tag(val, YELLOW)
            else:
                return wrap_in_color_tag(val, GREEN)
        case 'Humidity':
            if val < 40 or val > 60:
                return wrap_in_color_tag(val, RED)
            else:
                return wrap_in_color_tag(val, GREEN)
        case _:
            return wrap_in_color_tag(val)

# generating ending/type for the given value 
def value_postfix(sensor):
    match sensor:
        case 'Temperature':
            return '°C'
        case 'CO2':
            return ' ppm'
        case 'Humidity':
            return '%'
        case 'battery_percent':
            return '%'
        case 'Pressure':
            return ' mbar'

# return sensor alias if available
def sensor_alias(sensor):
    match sensor:
        case 'battery_percent':
            return f"{sensor}:\t"
        case 'Humidity':
            return f"{sensor}:\t\t"
        case 'Temperature':
            return f"{sensor}:\t\t"
        case 'CO2':
            return f"{sensor}:\t\t\t"
        case 'Pressure':
            return f"{sensor}:\t\t"
        case _:
            return sensor
                
def str_min_max_TH(sensor, val_minmaxTH):
    match sensor:
        case 'Temperature':
            return f" min = {val_minmaxTH[0]}{value_postfix(sensor)},\tmax = {val_minmaxTH[1]}{value_postfix(sensor)}"
        case 'Humidity':
            return f" min = {val_minmaxTH[2]}{value_postfix(sensor)},\tmax = {val_minmaxTH[3]}{value_postfix(sensor)}"
        case _:
            return ""

def str_trend(lastStationData, station, sensor):
    match sensor:
        case 'Temperature':
            return f",\ttrend = {lastStationData[station]['temp_trend']}"
        case 'Pressure':
            return f"\t\t\ttrend = {lastStationData[station]['pressure_trend']}"
        case _:
            return ""

# initializing the list of weather station sensors
def list_of_sensors(numberOfModules):
    listOfSensors = [[]] * numberOfModules

    # initialization of standard modules (one indoor + one outdoor) 
    listOfSensors[0] = ['Temperature', 'battery_percent']
    listOfSensors[-1] = ['Temperature', 'Humidity', 'CO2', 'Pressure']

    # initialization of additional modules
    i=1
    if numberOfModules > 2:
        while i < (numberOfModules - 1):
            listOfSensors[i] = ['Temperature', 'Humidity', 'CO2', 'battery_percent']
            i += 1

    return listOfSensors

# -----------------------------------------------------------------------------------

now = datetime.datetime.now()
print(f'>>> station name: {stationName} -', now.strftime('%H:%M:%S %d/%m/%Y'))

#1 : Authenticate
authorization = lnetatmo.ClientAuth()

try:
    # 2 : Creating class loaded with devices list and all telemetry
    stationData = lnetatmo.WeatherStationData(authorization)
    # getting list of weather station modules
    stationModulesList = stationData.modulesNamesList(stationName)
    # getting most recent telemetry from station
    lastStationData = stationData.lastData()
    
    # counting existing modules
    numberOfModules = len(stationModulesList)
    listOfSensors = list_of_sensors(numberOfModules)

    str_buffer = f""
    for station, sensorList in zip(stationModulesList, listOfSensors):
        str_buffer += f"\n{station}\n"
        for sensor in sensorList:
            str_buffer += f"  {sensor_alias(sensor)}{value_in_color(lastStationData[station][sensor], sensor)}{value_postfix(sensor)}\t{str_min_max_TH(sensor, stationData.MinMaxTH(station,'day'))}{str_trend(lastStationData, station, sensor)}\n"

except:
    # Something getting wrong
    str_buffer = 'Netatmo Server request failed!'

print (str_buffer)