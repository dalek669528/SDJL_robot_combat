#!/usr/bin/env python
import rospy
from motor_driver.msg import Pwm
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

        # Publications

        # Subscriptions
        self.sub_pwm = rospy.Subscriber("pwm", Pwm, self.cbPWM, queue_size=1)
        self.listener()

    def cbPWM(self, pwm_msg):
            s = str(pwm_msg.pwmA) + " " + str(pwm_msg.pwmB) + "\n"
            print self.encoder, "/", s,
            self.ser.write(s)

    def listener(self):
        while self.ser.isOpen():
            if self.ser.in_waiting:
                s = self.ser.readline()
                arr = s.split(' ')
                print arr
                # self.encoder = self.ser.readline()

if __name__ == '__main__':
    rospy.init_node("motor_driver",anonymous=False)
    motor_driver = Motor_driver()
    # rospy.spin()
