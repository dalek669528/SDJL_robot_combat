#!/usr/bin/env python
import rospy
from time import sleep
import serial

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# ser.write("start\n")
# sleep(0.005)
s = raw_input('INPUT:')
ser.write(s)
ser.write("\n")
print '--', s, '--'
sleep(0.005)

try:
    while 1:
        while ser.in_waiting:
            x = ser.readline()
            print x, "-"
            x = ''
            sleep(0.005)
            s = raw_input('INPUT:')
            ser.write(s)
            ser.write("\n")
            print '--', s, '--'
            sleep(0.005)
except KeyboardInterrupt:
    ser.close()
    print('\nBye.')
