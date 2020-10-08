import board
import busio
import adafruit_pca9685


def led_launch():
    i2c = busio.I2C(board.SCL, board.SDA)
    hat = adafruit_pca9685.PCA9685(i2c)
    hat.frequency = 60
    led_channel = hat.channels[0]
    # led_channel.duty_cycle = 0xffff
    # Increase brightness:
    for i in range(0xffff):
        led_channel.duty_cycle = i

    # Decrease brightness:
    for i in range(0xffff, 0, -1):
        led_channel.duty_cycle = i
