#!/usr/bin/python3
# apt-get install python3-pip
# pip install pyHS100
import datetime
from schedule import Schedule
import time

# abstract this so you can do more than one kind
def control(controller_obj,controller, state='query'):
    devices = controller_obj.discover()

    for device in devices:
        if devices[device].alias == controller:
            if state == 'query':
                return devices[device].is_on
            elif state == 'on':
                devices[device].turn_on()
            else:
                devices[device].turn_off()


def main():
    controllers = Schedule()
    while True:
        for controller in controllers.controllers:
            # json data true is string, and therefore always true?
            active_controller = controllers.controllers[controller]
            if active_controller['active'] == 'True':
                now = datetime.datetime.utcnow()
                scheduled_on = now.replace(hour=int(active_controller['on'].split(':')[0]),
                                           minute=int(active_controller['on'].split(':')[1]))
                scheduled_off = now.replace(hour=int(active_controller['off'].split(':')[0]),
                                            minute=int(active_controller['off'].split(':')[1]))
                if (scheduled_on > now < scheduled_off) or (scheduled_on < now > scheduled_off):
                    if not control(controllers,controller):
                         print("Turning " + str(active_controller) + " on")
                         control(controllers,controller, 'on')
                else:
                     if control(controllers,controller):
                          print("turning " + str(active_controller) + " off")
                          control(controllers,controller, 'off')
            if abs((now - now.replace(hour=0, minute=5)).total_seconds()) % 14400 == 0:
                    print("Updating sunset and twilight values")
                    controllers.update()
        print('sleeping...')
        time.sleep(60)


if __name__ == "__main__":
    main()

