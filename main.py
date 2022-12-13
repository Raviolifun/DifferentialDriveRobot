from Practice import bno055_control
import unit_test
import dif_drive
from Practice import servo_control
from HardwareInterface import remote_nrf24


def startup_robot():
    # unit_test.test_io()
    # led_control.led_launch()
    # servo_control.servo_drive_test()
    # bno055_control.bno055_setup()
    # differential_drive = dif_drive.DifferentialDrive(.105)
    # differential_drive.turn_to_angle(8)
    initialize_radio()


def exit_robot():
    remote_nrf24.exit_radio()


if __name__ == '__main__':
    try:
        startup_robot()
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Powering down radio.")
        exit_robot()

