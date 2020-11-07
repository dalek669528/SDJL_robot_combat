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
        self.v_gain = 25

        # Publications
        self.pub_msg = rospy.Publisher("motor_cmd", String, queue_size=1)
        
        # Subscriptions
        self.sub_joy_ = rospy.Subscriber("joy", Joy, self.cbJoy, queue_size=1)

        self.input()


    def cbJoy(self, joy_msg):
        Vx = joy_msg.axes[0] * self.v_gain * (-1)
        Vy = joy_msg.axes[1] * self.v_gain
        w = joy_msg.axes[3] * self.v_gain * (-0.2) * 180 / 3.14
        self.cmd.data = "3 " + str(Vx) + " "  + str(Vy) + " " + str(w)
        self.pub_msg.publish(self.cmd)

    def input(self):
        while True:
            # self.cmd.data = raw_input('INPUT (\'q\' to quit):')
            self.cmd.data = "4 " + str(0) + " "  + str(0) + " " + str(0)
            self.pub_msg.publish(self.cmd)
            if(self.cmd.data == "q"):
                break
            sleep(0.5)
            
if __name__ == '__main__':
    rospy.init_node("motor_pwm",anonymous=False)
    motor_pwm = Motor_pwm()
    # rospy.spin()
