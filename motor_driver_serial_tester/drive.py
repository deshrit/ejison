#!/usr/bin/env python3

import sys
import time
import serial
import threading

DEFAULT_SERIAL_PORT = "/dev/ttyACM0"
DEFAULT_BAUD_RATE = 115200
VALID_BAUD_RATES = [9600, 19200, 38400, 57600, 115200]


def read_serial(ser: serial.Serial, stop_event: threading.Event):
    while not stop_event.is_set():
        try:
            line = ser.readline()
            if not line:
                continue
            text = line.decode(errors="ignore").strip()
            if text:
                print(f"\r{text}")
                print(">> ", end="", flush=True)
        except serial.SerialException:
            print("\nSerial disconnected")
            stop_event.set()


def prase_args():
    port = DEFAULT_SERIAL_PORT
    baud_rate = DEFAULT_BAUD_RATE

    if len(sys.argv) > 1:
        device = sys.argv[1]
        if not device.startswith("/"):
            print("Invalid device!")
            sys.exit(1)
        port = device

    if len(sys.argv) > 2:
        try:
            rate = int(sys.argv[2])
            if rate not in VALID_BAUD_RATES:
                raise ValueError
            baud_rate = rate
        except ValueError:
            print(f"Error baud rates can only be: {VALID_BAUD_RATES}")
            sys.exit(1)
    return port, baud_rate


def print_help(port: str, baud_rate: int) -> None:
    print(f"Device: {port}\tBaud rate: {baud_rate}")
    print("""
For testing:

>> s         # Stop both motors
>> m s1 s2   # Run left and right motor with `s1` and `s2` speed respectively (range `±300`)
>> c         # Continue last speed
>> p         # Print current speed
>> t         # Print motor steps in same order as speed separated by a space
>> r         # Reset motor steps

Running with ROS:

>> d s1 s2   # Same as `m` and also publish motor steps along side


To exit: Ctrl + C 
""")


def main():
    port, baud_rate = prase_args()

    stop_event = threading.Event()

    with serial.Serial(port, baud_rate, timeout=0.5) as ser:
        print_help(port, baud_rate)

        # Read serial data
        read_thread = threading.Thread(target=read_serial, args=(ser, stop_event))
        read_thread.start()

        time.sleep(1.0)

        # Write serial data
        try:
            while not stop_event.is_set():
                msg = input(">> ")
                if msg:
                    ser.write((msg + "\n").encode())
        except serial.SerialException as e:
            print(f"\nSerial error: {e}")
        except (EOFError, KeyboardInterrupt):
            print("\nStopping...")
        finally:
            stop_event.set()
            read_thread.join()


if __name__ == "__main__":
    main()
