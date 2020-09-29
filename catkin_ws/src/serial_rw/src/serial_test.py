#!/usr/bin/env python
import rospy
from time import sleep
import serial

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# ser.write("start\n")
# sleep(0.005)
pwmA = raw_input('INPUT A:')
pwmB = raw_input('INPUT B:')
s = pwmA + "\n" + pwmB + "\n"
ser.write(s)

try:
    while 1:
        while ser.in_waiting:
            x = ser.readline()
            print x, "-"
            # x = ''
            # pwmA = raw_input('INPUT A:')
            # pwmB = raw_input('INPUT B:')
            # s = pwmA + "\n" + pwmB + "\n"
            # ser.write(s)
except KeyboardInterrupt:
    ser.close()
    print('\nBye.')
