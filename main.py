#!/usr/bin/python
import serial
import time
import json
import signal
import threading
import subprocess
import os

# def _sleep_handler(signum, frame):
#     # print("SIGINT Received. Stopping CAF")
#     raise KeyboardInterrupt

# def _stop_handler(signum, frame):
#     # print("SIGTERM Received. Stopping CAF")
#     raise KeyboardInterrupt

# signal.signal(signal.SIGTERM, _stop_handler)
# signal.signal(signal.SIGINT, _sleep_handler)

sensors = {}
class SerialThread(threading.Thread):
    def __init__(self):
        super(SerialThread, self).__init__()
        self.name = "SerialThread"
        self.setDaemon(True)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        serial_dev = os.getenv("HOST_DEV1")
        if serial_dev is None:
            serial_dev="/dev/ttyS1"

        sdev = serial.Serial(port=serial_dev, baudrate=921600) 
        sdev.bytesize = serial.EIGHTBITS #number of bits per bytes
        sdev.parity = serial.PARITY_NONE #set parity check: no parity
        sdev.stopbits = serial.STOPBITS_ONE #number of stop bits
        sdev.timeout = 5

        while True:
            if self.stop_event.is_set():
                break
            while sdev.inWaiting() > 0:
                sensVal = sdev.readline()
                # write to 25888
                time.sleep(1)
        sdev.close()

try:
    p = SerialThread()
    p.start()
except:
    print("error")