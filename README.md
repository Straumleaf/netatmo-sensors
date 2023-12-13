# netatmo-sensors

CLI utility which is reading and printing current Netatmo Weather Station telemetry.<br>
Its work based on [lnetatmo](https://github.com/philippelt/netatmo-api-python) library: https://github.com/philippelt/netatmo-api-python

## Work in progress

+ right now working mostly on cosmetic things and optimizations of code. 

## To setup netatmo-sensors.py you need

+ install Python (most recent version).
+ install pip utility.
+ with the help of pip utility install [lnetatmo](https://github.com/philippelt/netatmo-api-python) library

        pip install lnetatmo

+ clone this repository.
+ go to https://dev.netatmo.com and make registration
    -  login there and go to **My apps** through the top right menu
       or go straight to https://dev.netatmo.com/apps/ , whatever you prefer.
    -  and create app by choosing **Create** button.
    -  then fill such fields as: **app name**, **description**, **data protection officer name** and **data protection officer email** with appropriate information.
    -  and push the button **Save**, after that you will get access to: client ID, client secret
        and also access to Token generator which is required to get access to your Weather Station.
+ copy **client ID**, **client secret** and generated token and paste it in the file **.netatmo.credentials**.
+ place **.netatmo.credentials** file to your home directory, please.

       cp .netatmo.credentials ~/

+ now everything is ready, just type:
 
       python3 netatmo-sensors.py <station name>
 
  or simply if you set executable flag of netatmo-sensors.py 
 
        ./netatmo-sensors.py <station name>
 
 making sure that executable flag is set on and change `<station name>` to your actual weather station name which you can find on Netatmo weather station web-page, top right coner.
 
 Though the CLI should look like:
 
        ./netatmo-sensors.py MyWeatherStationName

## Run netatmo-sensors in CLI
### usage: netatmo-sensors.py [-h] [-c] [-t {f,c}] [-p {mb,in,mm}] station_name

+ `station_name` - Netatmo weather station name for eg.: `netatmo-sensors MyWeatherStation`
+ optional parameters:
    - `-c, --color`   color scheme application output. Default is B/W .
    - `-t {f,c}, --temp {f,c}`   temperature units - Fahrenheit or Celsius. Put `f` for Fahrenheit, default is Celsius.
    - `-p {mb,in,mm}, --pressure {mb,in,mm}`    pressure units - `mb` for mbar, `in` for inHg and `mm` for mmHg.  
