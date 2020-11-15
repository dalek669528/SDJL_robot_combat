#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from time import sleep

class Motor_pwm(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        self.cmd = String()

        # Publications
        self.pub_msg = rospy.Publisher("serial_cmd", String, queue_size=1)
        self.input()

    def input(self):
        while True:
            self.cmd.data = raw_input('INPUT (\'q\' to quit):')
            self.pub_msg.publish(self.cmd)
            if(self.cmd.data == "q"):
                break
            sleep(0.5)
            
if __name__ == '__main__':
    rospy.init_node("motor_pwm",anonymous=False)
    motor_pwm = Motor_pwm()
    # rospy.spin()
