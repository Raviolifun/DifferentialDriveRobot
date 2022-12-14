#from Practice import bno055_control
#import unit_test
#import dif_drive
#from Practice import servo_control
from HardwareInterface import remote_nrf24
from threading import Thread
import threading
import time


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
class RobotLoop(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.shutdown_flag = threading.Event()
        self.start()
        
    def run(self):
        while not self.shutdown_flag.is_set():
            self.robot_loop()
    
    # Main robot loop
    def robot_loop(self):
        print("heya")
        time.sleep(1)


# Start the robot from here
if __name__ == '__main__':
    # Startup robot peripherals
    startup_robot()
    # Start Robot stuff!
    radio_thread = remote_nrf24.RadioLoop()
    robot_thread = RobotLoop()
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

