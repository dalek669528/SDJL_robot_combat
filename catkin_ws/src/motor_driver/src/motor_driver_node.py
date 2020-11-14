#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D
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
        self.last_t = 0     # ms
        self.T = 250        # ms

        # Publications
        self.pub_pos = rospy.Publisher("position", Pose2D, queue_size=1)

        # Subscriptions
        self.sub_cmd = rospy.Subscriber("motor_cmd", String, self.cbCMD, queue_size=1)
        self.listener()

    def cbCMD(self, str_msg):
            if(str_msg.data == "q"):
                self.terminate = True
            else:
                s = "1 " + str_msg.data + "\n"
                self.ser.write(s)

    def listener(self):
        # for _ in range(10):
        #     if(self.ser.isOpen() and not self.terminate):
        #         self.ser.readline()
        # while (self.ser.isOpen() and not self.terminate):
        #     if self.ser.in_waiting:
        #         s = self.ser.readline()
        #         arr = s.split(' ')
        #         if(len(arr) >= 5 and arr[0].isdigit()):
        #             if((int(arr[0]) - self.last_t) >= self.T):
        #                 print arr[3:6]
        #                 self.last_t = int(arr[0])
        #                 pose = Pose2D()
        #                 pose.x = float(arr[3])
        #                 pose.y = float(arr[4])
        #                 pose.theta = float(arr[5])
        #                 self.pub_pos.publish(pose);
        sleep(1)
        while (self.ser.isOpen() and not self.terminate):
            sleep(self.T/1000.0)
            self.ser.write("2\n")
            s = self.ser.readline()
            arr = s.split(' ')
            if(len(arr) >= 5 and arr[0].isdigit()):
                print arr[:6]
                self.last_t = int(arr[0])
                pose = Pose2D()
                pose.x = float(arr[3])
                pose.y = float(arr[4])
                pose.theta = float(arr[5])
                self.pub_pos.publish(pose);
        self.ser.close()

if __name__ == '__main__':
    rospy.init_node("motor_driver",anonymous=False)
    motor_driver = Motor_driver()
    # rospy.spin()
