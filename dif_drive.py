""" this is the differential drive robot object"""

import time
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_bno055
import PID


class DifferentialDrive:

    def __init__(self, track_width):
        self._tack_width = track_width
        self._i2c = busio.I2C(board.SCL, board.SDA)
        self._sensor = adafruit_bno055.BNO055_I2C(self._i2c)
        self._kit = ServoKit(channels=16)
        self._angle_pid = PID.PIDController(self._sensor, "gyro", 1, 0, 0, 200)
        # self._sensor.gyro

    def turn_to_angle(self, angle):
        self._angle_pid.set_goal(angle)
        while True:
            print(self._angle_pid.get_controller_output())



