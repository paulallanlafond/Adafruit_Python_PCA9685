# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
from PySide import QtGui, QtCore
import sys
import cwiid
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
import logging
#logging.basicConfig(level=logging.DEBUG)

import ui.slider_gui as slider_gui

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
#servo_min = 150  # Min pulse length out of 4096
#servo_max = 600  # Max pulse length out of 4096
servo_min = 170  # Min pulse length out of 4096
servo_max = 580  # Max pulse length out of 4096
CHANNLE_DICT = {'table': 1, 'arm': 0, 'elbow': 2, 'forearm': 4, 'wrist_spin': 3, 'wrist_spin_2': 5}


# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)


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


def move_servo(channel, pulse):
    pwm.set_pwm(channel, 0, pulse)


def get_safe_pulse(value):
    if int(value) < servo_min:
        print('pulse too low, yo')
        return servo_min
    if int(value) > servo_max:
        return servo_max
    return int(value)


def print_paths():
    for path in sys.path:
        print(path)


class slider_interface(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(slider_interface, self).__init__(parent)
        self.ui = slider_gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.reset_robot()
        self.setup_signals()

    def reset_robot(self):
        move_servo(CHANNLE_DICT['table'], 300)
        self.ui.slider_table.setValue(300)
        move_servo(CHANNLE_DICT['arm'], 500)
        self.ui.slider_arm.setValue(500)
        move_servo(CHANNLE_DICT['elbow'], 400)
        self.ui.slider_elbow.setValue(400)
        move_servo(CHANNLE_DICT['forearm'], 200)
        self.ui.slider_forearm.setValue(200)
        move_servo(CHANNLE_DICT['wrist_spin'], 400)
        self.ui.slider_wrist_spin.setValue(400)
        move_servo(CHANNLE_DICT['wrist_spin_2'], 400)
        self.ui.slider_wrist_spin_2.setValue(400)

        move_servo(2, 100)
        move_servo(3, 300)
        move_servo(4, 300)
        move_servo(5, 300)

    def setup_signals(self):
        self.ui.slider_arm.valueChanged.connect(lambda: self.slider_moved(axis='arm'))
        self.ui.slider_table.valueChanged.connect(lambda: self.slider_moved(axis='table'))
        self.ui.slider_elbow.valueChanged.connect(lambda: self.slider_moved(axis='elbow'))
        self.ui.slider_forearm.valueChanged.connect(lambda: self.slider_moved(axis='forearm'))
        self.ui.slider_wrist_spin.valueChanged.connect(lambda: self.slider_moved(axis='wrist_spin'))
        self.ui.slider_wrist_spin_2.valueChanged.connect(lambda: self.slider_moved(axis='wrist_spin_2'))

    def slider_moved(self, axis):
        value = eval('self.ui.slider_{}.value()'.format(axis))
        pulse = get_safe_pulse(value)
        channel = CHANNLE_DICT[axis]
        move_servo(channel, pulse)


if __name__ == '__main__':
    print_paths()
    app = QtGui.QApplication(sys.argv)
    gui = slider_interface()
    gui.show()
    app.exec_()
    sys.exit()

