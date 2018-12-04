#!/usr/bin/python3
# apt-get install python3-pip
# pip install pyHS100
import datetime
from schedule import Schedule


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
            if controllers.controllers[controller]['active']:
                now = datetime.datetime.utcnow()
                active_controller = controllers.controllers[controller]
                scheduled_on = now.replace(hour=int(active_controller['on'].split(':')[0]),
                                           minute=int(active_controller['on'].split(':')[1]))
                scheduled_off = now.replace(hour=int(active_controller['off'].split(':')[0]),
                                            minute=int(active_controller['off'].split(':')[1]))
                if now < scheduled_on and not active_controller['sunset']:
                    #print('skipping..')
                    continue
                elif scheduled_off < now < scheduled_on and active_controller['sunset']:
                     if control(controllers,controller):
                        print("turning " + str(active_controller) + " off")
                        control(controllers,controller, 'off')
                elif now >= scheduled_off and not active_controller['sunset']:
                    #print(controller)
                    if control(controllers,controller):
                        print("turning not sunset " + str(active_controller) + " off")
                        control(controllers,controller, 'off')
                else:
                    #print(controller)
                    if not control(controllers,controller):
                        print("turning " + str(active_controller) + " on")
                        control(controllers,controller, 'on')
                if abs((now - now.replace(hour=0, minute=5)).total_seconds()) % 14400 == 0:
                    controllers.update()
        print('sleeping...')
        time.sleep(60)


if __name__ == "__main__":
    main()

