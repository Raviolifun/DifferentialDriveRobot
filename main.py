#from Practice import bno055_control
#import unit_test
#import dif_drive
#from Practice import servo_control
from adafruit_servokit import ServoKit
from HardwareInterface import remote_nrf24
from HardwareInterface import bno055_control
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
    magnitude = (-float(joy_x)/input_norm)**3
    direction = (-float(joy_y)/input_norm)**3

    left = output_norm * (magnitude - direction * abs(magnitude) + magnitude - direction)/2
    right = output_norm * (magnitude + direction * abs(magnitude) + magnitude + direction)/2

    if abs(left) > output_norm:
        left = math.copysign(output_norm, left)
    elif abs(left) * output_norm < 0.005:
        left = 0

    if abs(right) > output_norm:
        right = math.copysign(output_norm, right)
    elif abs(right) * output_norm < 0.005:
        right = 0

    return left, right


class StreamingMovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = []
        self.sum = 0

    def process(self, value):
        self.values.append(value)
        self.sum += value
        if len(self.values) > self.window_size:
            self.sum -= self.values.pop(0)
        return float(self.sum) / len(self.values)


class RobotLoop(Thread):
    def __init__(self, input_radio_thread):
        Thread.__init__(self)

        # Add the radio as an object to pull data from
        self.command_input = input_radio_thread

        # Initialize Gyro and start its thread
        self.IMU_thread = bno055_control.IMULoop()

        # I dont like putting this here, got to change this later
        # TODO
        self.kit = ServoKit(channels=16)
        self.joy_y_average = StreamingMovingAverage(5)
        self.joy_x_average = StreamingMovingAverage(5)

        # Thread Overhead
        self.shutdown_flag = threading.Event()
        self.start()
        
    def run(self):
        # This provides an exit strategy if both 6 and 7 are pressed
        while not self.shutdown_flag.is_set() and not (((self.command_input.buttons >> 6) & 1) and ((self.command_input.buttons >> 7) & 1)):
            self.robot_loop()
            time.sleep(.05)
        self.kit.continuous_servo[0].throttle = 0
        self.kit.continuous_servo[1].throttle = 0
        self.IMU_thread.shutdown_flag.set()
        self.IMU_thread.join()
        self.shutdown_flag.set()

    # Main robot loop
    def robot_loop(self):
        address = self.command_input.address

        if not address:
            joy_y = self.command_input.joy_y
            joy_x = self.command_input.joy_x
            buttons = self.command_input.buttons

            # self.command_input.send_error = 0
            self.command_input.send_status = buttons

            if (buttons >> 3) & 1:
                joy_y = self.joy_y_average.process(joy_y)
                joy_x = self.joy_x_average.process(joy_x)

                [left, right] = control_mixing(joy_y, joy_x, 3500, 1, 0.005)
                # print("Updating Robot Commands: ", left, ", ", right)
                self.kit.continuous_servo[0].throttle = -left
                # Found it was drifting a little bit
                self.kit.continuous_servo[1].throttle = right
                # Now lets see what buttons are set

            elif (buttons >> 4) & 1:
                # Now it's time to do error correction for gyro
                error = self.command_input.angle - self.IMU_thread.euler_angle[0]
                # To avoid angle discontinuities for Gyro
                if error > 180:
                    error = error - 360
                elif error < -180:
                    error = error + 360

                proportional_gain = 0.005
                proportional_term = error * proportional_gain
                if abs(proportional_term) > 1:
                    proportional_term = math.copysign(1, proportional_term)
                elif abs(proportional_term) < 0.005:
                    proportional_term = 0

                self.kit.continuous_servo[0].throttle = proportional_term
                self.kit.continuous_servo[1].throttle = proportional_term

                self.command_input.send_error = int(error)

                print("Gyro Mode, Error: ", error)

            elif (buttons >> 5) & 1:
                print("Human Mode")
                # time to track human faces!

            elif (buttons >> 6) & 1:
                print("Undefined Mode 1")

            elif (buttons >> 7) & 1:
                print("Undefined Mode 2")

            else:
                # make sure the motors aren't moving if a panic stop was done
                self.kit.continuous_servo[0].throttle = 0
                self.kit.continuous_servo[1].throttle = 0

        else:
            print("Different Address, setting velocity to zero")
            self.kit.continuous_servo[0].throttle = 0
            self.kit.continuous_servo[1].throttle = 0


# Start the robot from here
if __name__ == '__main__':
    # Startup robot peripherals
    startup_robot()

    # Start Robot stuff!
    radio_thread = remote_nrf24.RadioLoop()
    robot_thread = RobotLoop(radio_thread)

    # If the user presses space, stop the device
    try:
        while not robot_thread.shutdown_flag.is_set():
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

