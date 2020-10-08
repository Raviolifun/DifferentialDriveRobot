import time
import board
import busio
import adafruit_bno055


def bno055_setup():
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bno055.BNO055_I2C(i2c)

    while True:
        print("Temperature: {} degrees C".format(sensor.temperature))
        print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
        print("Magnetometer (microteslas): {}".format(sensor.magnetic))
        print("Gyroscope (rad/sec): {}".format(sensor.gyro))
        print("Euler angle: {}".format(sensor.euler))
        print("Quaternion: {}".format(sensor.quaternion))
        print("Linear acceleration (m/^2): {}".format(sensor.linear_acceleration))
        print("Gravity (m/s^2): {}".format(sensor.gravity))
        print()

        time.sleep(1)