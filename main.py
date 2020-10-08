from Practice import bno055_control
import unit_test
import dif_drive
from Practice import servo_control


def start_up():
    unit_test.test_io()
    # led_control.led_launch()
    # servo_control.servo_drive_test()
    # bno055_control.bno055_setup()
    differential_drive = dif_drive.DifferentialDrive(.105)
    differential_drive.turn_to_angle(8)



if __name__ == '__main__':
    start_up()
