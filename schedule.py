import requests

class Schedule:
    # times are in utc
    # ignore dst for now
    controllers = {
        'Kitchen': {'on': '00:24', 'off': '02:30', 'twilight': True},
        'Stairs': {'on': '02:00', 'off': '02:45'}
    }

    def __init__(self):
        self.update()

    def update(self):
        lat = requests.get('http://ip-api.com/json').json()['lat']
        lon = requests.get('http://ip-api.com/json').json()['lon']
        url = 'https://api.sunrise-sunset.org/json?lat=' + str(lat) + '&lng=' + str(lon) + '&formatted=0'
        twilight_end = requests.get(url).json()['results']['civil_twilight_end'].split('T')[1][:5]
        for controller in Schedule.controllers:
            if Schedule.controllers[controller].__contains__('twilight'):
                Schedule.controllers[controller]['on'] = twilight_end
