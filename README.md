# netatmo-sensors
CLI utility which is reading and printing current Netatmo Weather Station telemetry
Its work based on lnetatmo library: https://github.com/Straumleaf/netatmo-sensors.git

Work in progress
    - going to add --station-name: flag to make possible request any user station without editing script
    for the momemnt station name is hardcoded. 

To setup netatmo-sensors.py you need
    - install Python (most recent version)
    - install pip utility
    - with the help of pip utility install 'lnetatmo' library
        "pip install lnetatmo"
    - clone this repository
    - go to https://dev.netatmo.com and make registration
        login ther and go to 'My apps' through the top right menu
        or go straight to https://dev.netatmo.com/apps/ , whatever you prefer
        and create app by choosing 'Create' button
        then fill such fields as: 'app name', 'description', 'data protection officer name' and 'data protection officer email' with appropriate information
        and push the button 'Save', after that you will get access to: client ID, client secret
        and also access to Token generator which is required to get access to your Weather Station
    - copy 'client ID', 'client secret' and generated token and paste it in the file '.netatmo.credentials'
    - place '.netatmo.credentials' file to your home directory/folder
    - open 'netatmo-sensors.py' and find line 6 with 'stationName' variable and change its value to the name of your Netatmo weather station as it stated
      on the left top corner of netatmo web-page
    - now everything is ready, just type: 'python3 netatmo-sensors.py' or './netatmo-sensors.py' making sure that executable flag is on
     
