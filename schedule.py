#!/usr/bin/python3

import requests

class Schedule:
    # times are in utc
    # ignore dst for now
    def __init__(self):
        self.controllers = {
        'Front': {'active': True, 'on': '00:24', 'off': '02:30', 'sunset': True, 'twilight': True},
        'Kitchen': {'active': False, 'on': '00:24', 'off': '02:30', 'sunset': True},
        'Stairs': {'active': False, 'on': '02:00', 'off': '02:45'}
        }
        self.update()

    def update(self):
        lat = requests.get('http://ip-api.com/json').json()['lat']
        lon = requests.get('http://ip-api.com/json').json()['lon']
        url = 'https://api.sunrise-sunset.org/json?lat=' + str(lat) + '&lng=' + str(lon) + '&formatted=0'
        sunset = requests.get(url).json()['results']['sunset'].split('T')[1][:5]
        twilight_begin = requests.get(url).json()['results']['civil_twilight_begin'].split('T')[1][:5]
        print ("sun set and twilight " + sunset + " " + twilight_begin)
        for controller in self.controllers:
            if self.controllers[controller]['active']:
                print(str(controller) + " Is being examined for sunset/twilight")
                if self.controllers[controller].__contains__('sunset'):
                    print ('updating sunset for ' + str(controller))
                    self.controllers[controller]['on'] = sunset
                if self.controllers[controller].__contains__('twilight'):
                    print ('updating twilight for ' + str(controller))
                    self.controllers[controller]['off'] = twilight_begin

