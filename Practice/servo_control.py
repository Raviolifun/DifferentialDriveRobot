"""Simple test for a standard servo on channel 0 and a continuous rotation servo on channel 1."""
import time
from adafruit_servokit import ServoKit


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
