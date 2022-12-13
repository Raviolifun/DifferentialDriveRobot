"""
A simple example of sending data from 1 nRF24L01 transceiver to another.
This example was written to be used on 2 devices acting as 'nodes'.
"""
import sys
import argparse
import time
import struct
import threading
from RF24 import RF24, RF24_PA_LOW

########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/pyRF24/readme.md
# Radio CE Pin, CSN Pin, SPI Speed
# CE Pin uses GPIO number with BCM and SPIDEV drivers, other platforms use
# their own pin numbering
# CS Pin addresses the SPI bus number at /dev/spidev<a>.<b>
# ie: RF24 radio(<ce_pin>, <a>*10+<b>); spidev1.0 is 10, spidev1.1 is 11 etc..

# Generic:
radio = RF24(6, 0)

# Variable to store values in
payload = [None]*4


# def master():
#     """Transmits an incrementing float every second"""
#     radio.stopListening()  # put radio in TX mode
#     failures = 0
#     while failures < 6:
#         # use struct.pack() to packet your data into the payload
#         # "<f" means a single little endian (4 byte) float value.
#         buffer = struct.pack("<f", payload[0])
#         start_timer = time.monotonic_ns()  # start timer
#         result = radio.write(buffer)
#         end_timer = time.monotonic_ns()  # end timer
#         if not result:
#             print("Transmission failed or timed out")
#             failures += 1
#         else:
#             print(
#                 "Transmission successful! Time to Transmit:",
#                 f"{(end_timer - start_timer) / 1000} us. Sent: {payload[0]}",
#             )
#             payload[0] += 0.01
#         time.sleep(1)
#     print(failures, "failures detected. Leaving TX role.")


def slave(timeout=6):
    """Listen for any payloads and print the transaction

    :param int timeout: The number of seconds to wait (with no transmission)
        until exiting function.
    """
    radio.startListening()  # put radio in RX mode

    start_timer = time.monotonic()
    while (time.monotonic() - start_timer) < timeout:
        has_payload, pipe_number = radio.available_pipe()
        if has_payload:
            # fetch 1 payload from RX FIFO
            buffer = radio.read(radio.payloadSize)
            # use struct.unpack() to convert the buffer into usable data
            # expecting a little endian float, thus the format string "<f"
            # buffer[:4] truncates padded 0s in case payloadSize was not set
            payload[0] = struct.unpack(">H", buffer[0:2])[0]
            payload[1] = struct.unpack(">h", buffer[2:4])[0]
            payload[2] = struct.unpack(">h", buffer[4:6])[0]
            payload[3] = struct.unpack(">H", buffer[6:8])[0]
            # print details about the received packet
            print(
                f"Received {radio.payloadSize} bytes",
                f"on pipe {pipe_number}: {payload[0]}, {payload[1]}, {payload[2]}, {payload[3]}",
            )
            start_timer = time.monotonic()  # reset the timeout timer

    print("Nothing received in", timeout, "seconds. Leaving RX role")
    # recommended behavior is to keep in TX mode while idle
    radio.stopListening()  # put the radio in TX mode


def exit_radio():
    radio.powerDown()


def initialize_radio():
    # Initialize the nRF24L01 on the spi bus
    if not radio.begin():
        raise RuntimeError("radio hardware is not responding")

    # Set Address
    address = [b"1Node", b"2Node"]

    # set the Power Amplifier level to -12 dBm since this test example is
    # usually run with nRF24L01 transceivers in proximity of each other
    radio.setPALevel(RF24_PA_LOW)  # RF24_PA_MAX is default

    # set the TX address of the RX node into the TX pipe
    radio.openWritingPipe(address[1])  # always uses pipe 0

    # set the RX address of the TX node into a RX pipe
    radio.openReadingPipe(1, address[0])  # using pipe 1

    # Set payload to max size (transmission time is inconsequential)
    radio.payloadSize = 32

    # for debugging, we have 2 options that print a large block of details
    # (smaller) function that prints raw register values
    # radio.printDetails()
    # (larger) function that prints human-readable data
    # radio.printPrettyDetails()

    slave(timeout=1)


