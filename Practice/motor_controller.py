"""
Motor Control Library
Author: Oren Anderson
Version: 1
Date Created: 11/21/2022
"""

import time
from adafruit_servokit import ServoKit


class MotorController:
    servo_kit = None

    def __init__(self, motor, encoder=None, p_gain=0, i_gain=0, d_gain=0, use_filter=None):
        """
        :param motor:         Motor you want to control
        :param p_gain:        Proportional gain of the PID control for the motor
        :param i_gain:        Integral gain of the PID control for the motor
        :param d_gain:        Derivative gain of the PID control for the motor
        :param use_filter:    Whether to use the basic moving average filter for position
        """

        # TODO decide if I am only doing PID on position or also on velocity
        # can't do either as it is xD

        self.motor = motor
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain

        self.speed_old = 0
        self.speed_new = 0
        self.position_old = 0
        self.position_new = 0

        if not ServoController.servo_kit:
            ServoController.servo_hat_initialize()

        if use_filter:
            raise ValueError("Either use filtering or the observer, cannot use both")

    @staticmethod
    def servo_hat_initialize():
        # only verified to work with PI servo Hat
        ServoController.servo_kit = ServoKit(channels=16)

    def run_motor_for_millis(self, run_time):
        pass

    def run_motor_for_distance(self, radius, distance):
        pass

    def run_motor_for_angle(self, angle):
        pass

    def run_motor_at_speed(self, speed):
        ServoController.servo_kit.continuous_servo[self.motor_index].throttle = speed

    def


def servo_drive_test():
    # Set channels to the number of servo channels on your kit.
    # 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
    kit = ServoKit(channels=16)

    intensity = 0.2

    kit.continuous_servo[0].throttle = -intensity
    kit.continuous_servo[1].throttle = intensity
    time.sleep(0.2)
    kit.continuous_servo[0].throttle = 0
    kit.continuous_servo[1].throttle = 0
    time.sleep(0.2)
    kit.continuous_servo[0].throttle = intensity
    kit.continuous_servo[1].throttle = -intensity
    time.sleep(0.2)
    kit.continuous_servo[0].throttle = 0
    kit.continuous_servo[1].throttle = 0
