#from Practice import bno055_control
#import unit_test
#import dif_drive
#from Practice import servo_control
from adafruit_servokit import ServoKit
from HardwareInterface import remote_nrf24
from threading import Thread
import threading
import time
import math


# Run these to start the robot, then call robot_loop() to continue
def startup_robot():
    # unit_test.test_io()
    # led_control.led_launch()
    # servo_control.servo_drive_test()
    # bno055_control.bno055_setup()
    # differential_drive = dif_drive.DifferentialDrive(.105)
    # differential_drive.turn_to_angle(8)
    pass


# Make sure to safely exit and call these before the robot powers down
def exit_robot():
    pass


# Make sure to NOT run this twice, currently there is no protection
def control_mixing(joy_y, joy_x, input_norm, output_norm, threshold):
    magnitude = joy_y/input_norm
    direction = joy_x/input_norm

    if abs(magnitude) * input_norm < threshold:
        magnitude = 0

    left = output_norm * magnitude * (1 + direction - direction * math.copysign(1, direction))
    right = output_norm * magnitude * (1 - direction - direction * math.copysign(1, direction))

    return left, right


class RobotLoop(Thread):
    def __init__(self, input_radio_thread):
        Thread.__init__(self)

        # Add the radio as an object to pull data from
        self.command_input = input_radio_thread

        # I dont like putting this here, got to change this later
        # TODO
        self.kit = ServoKit(channels=16)

        # Thread Overhead
        self.shutdown_flag = threading.Event()
        self.start()
        
    def run(self):
        while not self.shutdown_flag.is_set():
            self.robot_loop()
            time.sleep(25)

    # Main robot loop
    def robot_loop(self):
        address = self.command_input.self.address

        if not address:
            joy_y = self.command_input.self.joy_y
            joy_x = self.command_input.self.joy_x
            buttons = self.command_input.self.buttons

            [left, right] = control_mixing(joy_y, joy_x, 2048, 1, 50)
            self.kit.continuous_servo[0].throttle = left
            self.kit.continuous_servo[1].throttle = right
        else:
            self.kit.continuous_servo[0].throttle = 0
            self.kit.continuous_servo[1].throttle = 0


# Start the robot from here
if __name__ == '__main__':
    # Startup robot peripherals
    startup_robot()
    # Start Robot stuff!
    radio_thread = remote_nrf24.RadioLoop()
    robot_thread = RobotLoop(radio_thread)
    # Wait until something possibly errors out

    # If the user presses space, stop the device
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    print("Exiting Robot Program")

    # Shutdown Robot Threads
    robot_thread.shutdown_flag.set()
    robot_thread.join()
    radio_thread.shutdown_flag.set()
    radio_thread.join()

    # Call any required exit functions
    exit_robot()

