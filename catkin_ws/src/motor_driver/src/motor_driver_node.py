#!/usr/bin/env python
import rospy
from motor_driver.msg import Pwm
from std_msgs.msg import String
from time import sleep
import serial
import struct

class Motor_driver(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))
        self.encoder = 0
        self.ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.terminate = False
        # Publications

        # Subscriptions
        self.sub_cmd = rospy.Subscriber("motor_cmd", String, self.cbCMD, queue_size=1)
        self.listener()

    def cbCMD(self, str_msg):
            if(str_msg.data == "q"):
                self.terminate = True
            else:
                s = str_msg.data + "\n"
                self.ser.write(s)

    def listener(self):
        while (self.ser.isOpen() and not self.terminate):
            if self.ser.in_waiting:
                s = self.ser.readline()
                arr = s.split(' ')
                print arr
                # self.encoder = self.ser.readline()
        self.ser.close()

if __name__ == '__main__':
    rospy.init_node("motor_driver",anonymous=False)
    motor_driver = Motor_driver()
    # rospy.spin()
