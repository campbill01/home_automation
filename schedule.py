#!/usr/bin/python3

import requests
import os
import json
import pyHS100
import time


class Schedule:
    # times are in utc
    # ignore dst for now
    def __init__(self):
        if os.environ.get('CONFIG_FILE') and os.environ.get('KUBERNETES_PORT'):
            config_file=(os.environ.get('CONFIG_FILE'))
            self._get_controllers(config_file)
            self.run_type = 'container'
        else:
            self.controllers = {
            'Front': {'active': True, 'on': '00:24', 'off': '02:30', 'sunset': True, 'twilight': True},
            'Kitchen': {'active': False, 'on': '00:24', 'off': '02:30', 'sunset': True, 'twilight': False},
            'Stairs': {'active': False, 'on': '02:00', 'off': '02:45','sunset': False, 'twilight': False}
            }
            self.run_type = 'local'
        self.update()

    def _get_controllers(self,config_file='/etc/config/data.json'):
        data = open(config_file).read()
        json_data = json.loads(data)
        # name, on, off, active, sunset,twilight
        self.controllers = {}
        for item in json_data['config']:
            self.controllers[item['name']] = {'active':item['active'],'on':item['on'],'off':item['off'],'sunset':item['sunset'],'twilight':item['twilight'], 'address':item['address']}

    def update(self):
        try:
            location_data = requests.get('http://ip-api.com/json').json()
        except requests.exceptions.ConnectionError as e:
            print(e)
            return
        lat = location_data['lat']
        lon = location_data['lon']
        sun_data_url = 'https://api.sunrise-sunset.org/json?lat=' + str(lat) + '&lng=' + str(lon) + '&formatted=0'
        try:
            sun_data = requests.get(sun_data_url).json()['results']
        except requests.exceptions.ConnectionError as e:
            print(e)
            return
        sunset = sun_data['sunset'].split('T')[1][:5]
        twilight_begin = sun_data['civil_twilight_begin'].split('T')[1][:5]
        print ("sun set and twilight " + sunset + " " + twilight_begin)
        for controller in self.controllers:
            if self.controllers[controller]['active']:
                print(str(controller) + " Is being examined for sunset/twilight")
                if self.controllers[controller]['sunset']:
                    print ('updating sunset for ' + str(controller))
                    self.controllers[controller]['on'] = sunset
                if self.controllers[controller]['twilight']:
                    print ('updating twilight for ' + str(controller))
                    self.controllers[controller]['off'] = twilight_begin

        def discover(self):
            if self.run_type == 'local':
                devices = 'N'
                count = 0
                while len(devices) < len(self.controllers) and count < 20:
                    devices = pyHS100.Discover.discover()
                    time.sleep(5)
                    count += 1
            else:
                devices = []
                for controller in self.controllers:
                    devices.append(pyHS100.Discover.discover_single(self.controllers[controller]['address']))

            return devices

