#!/usr/bin/env python
import lnetatmo
import datetime
import argparse
import json
import types

# ANSI color codes
DEFAULT = '\033[0m' 
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# standard netatmo sensors resources
constants = types.SimpleNamespace()
constants.TEMP = 'Temperature'
constants.HUMID = 'Humidity'
constants.CO2 = 'CO2'
constants.PRES = 'Pressure'
constants.BAT = 'battery_percent'

# units type
CELSIUS = '°C' 
FAHREHEIT = '°F'
MBAR = ' mbar'
IN_HG = ' inHg'
MM_HG = ' mmHg'

# function just add to value ANSI color tag
def wrap_in_color_tag(val, color = None):
    return f"{DEFAULT}{val}" if color is None else f"{color}{val}{DEFAULT}"

# coloring outputs depending of its value
def value_in_color (val, sensor):
    if args.color:
        match sensor:
            case constants.TEMP:
                if val < 3:
                    return wrap_in_color_tag(val, BLUE)
                if val < 15:
                    return wrap_in_color_tag(val, GREEN)
                if val < 27:
                    return wrap_in_color_tag(val, YELLOW)
                else:
                    return wrap_in_color_tag(val, RED)
            case constants.CO2:
                if val < 500:
                    return wrap_in_color_tag(val, GREEN)
                if val < 1500:
                    return wrap_in_color_tag(val, YELLOW)
                else:
                    return wrap_in_color_tag(val, RED)
            case constants.BAT:
                if val < 30:
                    return wrap_in_color_tag(val, RED)
                if val < 60:
                    return wrap_in_color_tag(val, YELLOW)
                else:
                    return wrap_in_color_tag(val, GREEN)
            case constants.HUMID:
                if val < 40 or val > 60:
                    return wrap_in_color_tag(val, RED)
                else:
                    return wrap_in_color_tag(val, GREEN)
            case _:
                return wrap_in_color_tag(val)
    else:
        return wrap_in_color_tag(val)

# placing a unit type to the end of the given value 
def value_postfix(sensor):
    match sensor:
        case constants.TEMP:
            unit_degree = FAHREHEIT if tempUnits == 'f' else CELSIUS
            return unit_degree
        case constants.CO2:
            return ' ppm'
        case constants.HUMID:
            return '%'
        case constants.BAT:
            return '%'
        case constants.PRES:
            unit_pressure = MM_HG if pressureUnits == 'mm' else IN_HG if pressureUnits == 'in' else MBAR
            return unit_pressure

# change sensor name by alias if they available and add tabs
def sensor_alias(sensor):
    match sensor:
        case constants.BAT:
            return f"{sensor}:\t"
        case constants.HUMID:
            return f"{sensor}:\t\t"
        case constants.TEMP:
            return f"{sensor}:\t\t"
        case constants.CO2:
            return f"{sensor}:\t\t\t"
        case constants.PRES:
            return f"{sensor}:\t\t"
        case _:
            return sensor
                
# formating temperature and humidity max and min                
def str_min_max_TH(sensor, val_minmaxTH):
    match sensor:
        case constants.TEMP:
            return f" min = {val_minmaxTH[0]}{value_postfix(sensor)},\tmax = {val_minmaxTH[1]}{value_postfix(sensor)}"
        case constants.HUMID:
            return f" min = {val_minmaxTH[2]}{value_postfix(sensor)},\tmax = {val_minmaxTH[3]}{value_postfix(sensor)}"
        case _:
            return ""

# reading temperature and pressure trends
def str_trend(lastStationData, station, sensor):
    try:
        match sensor:
            case constants.TEMP:
                return f",\ttrend = {lastStationData[station]['temp_trend']}"
            case constants.PRES:
                return f"\t\t\ttrend = {lastStationData[station]['pressure_trend']}"
            case _:
                return ""
    except:
        return "N/A yet"

# initializing the list of weather station sensors
def list_of_sensors(numberOfModules):
    listOfSensors = [[]] * numberOfModules

    # initialization of standard modules (one indoor + one outdoor) 
    listOfSensors[0] = [constants.TEMP, constants.BAT]
    listOfSensors[-1] = [constants.TEMP, constants.HUMID, constants.CO2, constants.PRES]

    # initialization of additional modules
    i=1
    if numberOfModules > 2:
        while i < (numberOfModules - 1):
            listOfSensors[i] = [constants.TEMP, constants.HUMID, constants.CO2, constants.BAT]
            i += 1

    return listOfSensors

# MAIN -----------------------------------------------------------------------------------

# parsing CLI arguments
parser = argparse.ArgumentParser(description = 'print telemetry data of Netatmo weather station',
                                  formatter_class = argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('station_name', type = str,
                     help = 'Netatmo weather station name')                                  # name of weather station
parser.add_argument('-c','--color', action = 'store_true',
                     help = 'color or b/w output')                                           # color or b/w
parser.add_argument('-t','--temp', choices = ['f', 'c'], type = str,
                     help = 'f - for Fahrenheit, c - for Celsius ', default = 'c')           # temp units
parser.add_argument('-p','--pressure', choices = ['mb', 'in', 'mm'], type = str,
                     help = 'mb - for mbar, in - for inHg, mm - for mmHg', default = 'mb')   # pressure units
parser.add_argument('-d', '--debug', action = 'store_true',
                     help = 'raw telemetry information')                                          # printing stations JSON file

args = parser.parse_args()

stationName = args.station_name
tempUnits = args.temp
pressureUnits = args.pressure

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
if args.debug:
    print (json.dumps(lastStationData, indent = 2))