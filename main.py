#!/usr/bin/python
import serial
import time
import os
import socket

debug = True
HOST = "52.45.17.177"
IQ_PORT = 24888
DEBUG_PORT = 25888 

def debugPrint(msg):
    if (debug and not tcpDebugClient._closed):
        tcpDebugClient.sendall(msg)

def _main_():
    # COM PORT
    debugPrint(b"Opening Com")
    serial_dev = os.getenv("HOST_DEV")
    if serial_dev is None:
        debugPrint(b'Port not found')
        serial_dev="COM3" #COM3 testing windows

    serialPort = serial.Serial(port=serial_dev, baudrate=921600) 
    serialPort.bytesize = serial.EIGHTBITS # number of bits per bytes
    serialPort.parity = serial.PARITY_NONE # set parity check: no parity
    serialPort.stopbits = serial.STOPBITS_ONE # number of stop bits
    serialPort.timeout = 5

    while True:
        while serialPort.inWaiting() > 0:
            packet = serialPort.readline()
            tcpMainClient.sendall(packet)
    debugPrint(b"Not waiting for serial port; close.")
    serialPort.close()

# Start
tcpMainClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpMainClient.connect((HOST, IQ_PORT))

tcpDebugClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpDebugClient.connect((HOST, DEBUG_PORT))

debugPrint(b"New Connection!")
_main_()
