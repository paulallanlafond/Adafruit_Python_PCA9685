
import time

from approxeng.input.selectbinder import ControllerResource

while True:
    try:
        with ControllerResource() as joystick:
            print('found a joystick')

        print('connection to joystick lost')

    except IOError:
        print('cant find joystick')
        time.sleep(1.0)
