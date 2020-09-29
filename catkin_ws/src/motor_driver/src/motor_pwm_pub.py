#!/usr/bin/env python
import rospy
from motor_driver.msg import Pwm
from time import sleep
import serial

class Motor_pwm(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        # Publications
        self.pub_msg = rospy.Publisher("pwm", Pwm, queue_size=1)
        self.pwm = Pwm()
        # Subscriptions
        self.input()

    def input(self):
        while True:
            self.pwm.pwmA = int(raw_input('INPUT A:'))
            self.pwm.pwmB = int(raw_input('INPUT B:'))
            self.pub_msg.publish(self.pwm)

if __name__ == '__main__':
    rospy.init_node("motor_pwm",anonymous=False)
    motor_pwm = Motor_pwm()
    rospy.spin()
