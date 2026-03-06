#!/usr/bin/env python3

import sys
import time
import serial
import threading

serial_port = "/dev/ttyACM0"
baud_rate = 115200

valid_baud_rates = [9600, 19200, 38400, 57600, 115200]


def read_serial(ser: serial.Serial):
    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode(errors="ignore").strip()
                if data:
                    print(f"\r{data}")
                    print(">> ", end="", flush=True)
        except KeyboardInterrupt:
            break


def main():
    global serial_port, baud_rate, valid_baud_rates

    if len(sys.argv) > 1:
        device = sys.argv[1]
        if not device.startswith("/"):
            print("Invalid device!")
            sys.exit(1)
        serial_port = device

    if len(sys.argv) > 2:
        if (rate := int(sys.argv[2])) and (rate in valid_baud_rates):
            baud_rate = rate
        else:
            print(f"Error baud rates can only be: {valid_baud_rates}")
            sys.exit(1)

    ser = serial.Serial(serial_port, baud_rate, timeout=3.0)

    print(f"Device: {serial_port}\tBaudrate: {baud_rate}")
    print("""
>> s         # Stop both motors
>> m s1 s2   # Run left and right motor with `s1` and `s2` speed respectively (range `±300`)
>> c         # Continue last speed
>> p         # Print current speed

To exit: Ctrl + C 
""")

    # Read serial data
    rt = threading.Thread(target=read_serial, args=(ser,), daemon=True)
    rt.start()

    time.sleep(2.0)

    # Write serial data
    try:
        while True:
            msg = input(">> ")
            if msg:
                ser.write((msg + "\n").encode())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
