#!/usr/bin/python3
# apt-get install python3-pip
# pip install pyHS100
import datetime
import time

import pyHS100

from home_automation.schedule import Schedule


# abstract this so you can do more than one kind
def control(controller, state='query'):
    devices = 'N'
    count = 0
    while len(devices) < len(Schedule.controllers) and count < 20:
        devices = pyHS100.Discover.discover()
        time.sleep(5)
        count += 1

    for device in devices:
        if devices[device].alias == controller:
            if state == 'query':
                return devices[device].is_on
            elif state == 'on':
                devices[device].turn_on()
            else:
                devices[device].turn_off()


def main():
    while True:
        controllers = Schedule()
        for controller in controllers.controllers:
            now = datetime.datetime.utcnow()
            active_controller = controllers.controllers[controller]
            scheduled_on = now.replace(hour=int(active_controller['on'].split(':')[0]), minute=int(active_controller['on'].split(':')[1]))
            scheduled_off = now.replace(hour=int(active_controller['off'].split(':')[0]), minute=int(active_controller['off'].split(':')[1]))
            if now < scheduled_on:
                continue
            elif now >= scheduled_off:
                if control(controller):
                    control(controller, 'off')
            else:
                if not control(controller):
                    control(controller, 'on')
        time.sleep(60)


if __name__ == "__main__":
    main()