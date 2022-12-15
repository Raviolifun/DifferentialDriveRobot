import time
import board
import busio
import adafruit_bno055
import threading
from threading import Thread


# Make sure to NOT run this twice, currently there is no protection
class IMULoop(Thread):
    def __init__(self):
        Thread.__init__(self)

        # Sensor Initialization
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)

        # Sensor Data Saving
        self.euler_angle = self.sensor.euler

        # Handle Thread Stuff
        self.shutdown_flag = threading.Event()
        self.start()

    def run(self):
        self.gyro_loop()

    def gyro_loop(self):
        while not self.shutdown_flag.is_set():
            # print("Temperature: {} degrees C".format(self.sensor.temperature))
            # print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
            # print("Magnetometer (microteslas): {}".format(sensor.magnetic))
            # print("Gyroscope (rad/sec): {}".format(self.sensor.gyro))
            self.euler_angle = self.sensor.euler
            # print("Quaternion: {}".format(sensor.quaternion))
            # print("Linear acceleration (m/^2): {}".format(sensor.linear_acceleration))
            # print("Gravity (m/s^2): {}".format(sensor.gravity))
            time.sleep(0.025)


