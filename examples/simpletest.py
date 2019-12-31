# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
from PySide import QtGui, QtCore
import sys
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
#servo_min = 150  # Min pulse length out of 4096
#servo_max = 600  # Max pulse length out of 4096
servo_min = 170  # Min pulse length out of 4096
servo_max = 580  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    print('channel:{}  pulse:{}'.format(channel, pulse))
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)


def move_servo(channel, pulse):
    print('Moving servo on channel {}, press Ctrl-C to quit...\n'.format(channel))
    pwm.set_pwm(channel, 0, pulse)
    time.sleep(1)


def get_user_input():
    return input('enter channel and pulse. ex: 1,200\n').split(',')


def get_safe_pulse(value):
    if int(value) < servo_min:
        print('pulse too low, yo')
        return servo_min
    if int(value) > servo_max:
        return servo_max
    return int(value)


if __name__ == '__main__':
    # app = QtGui.QApplication(sys.argv)
    # label = QtGui.QLabel('fart face')
    # label.show()
    # app.exec_()
    # sys.exit()
    while True:
        channel, pulse = get_user_input()
        pulse = get_safe_pulse(pulse)
        move_servo(int(channel), pulse)
        #set_servo_pulse(int(channel), float(pulse))
