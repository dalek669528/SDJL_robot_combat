#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import Joy
from time import sleep
import serial
import struct

class Serial_driver(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        self.ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.terminate = False
        self.T = 250        # ms

        self.car_pose = Pose2D()
        self.v_gain = 25

        self.arm_angle = [0, 0, 0, 0]
        self.servo_ptr = 0;
        self.ang_gain = 10;

        self.slide_encoder = 0;
        self.encoder_gain = 30

        # Publications
        self.pub_pos = rospy.Publisher("position", Pose2D, queue_size=1)

        # Subscriptions
        self.sub_cmd = rospy.Subscriber("motor_cmd", String, self.cbMorot, queue_size=1)
        self.sub_cmd = rospy.Subscriber("arm_cmd", String, self.cbArm, queue_size=1)
        self.sub_joy_ = rospy.Subscriber("joy", Joy, self.cbJoy, queue_size=1)
        self.listener()


    def cbJoy(self, joy_msg):
        if(joy_msg.buttons[6]): 
            # terminate node
            self.ser.write("0\n")
            self.terminate = True
        if(joy_msg.buttons[7]):
            # reset car
            cmd = "0\n"
            self.ser.write(cmd)
        # Pose control 
        Vx = joy_msg.axes[0] * self.v_gain * (-1)
        Vy = joy_msg.axes[1] * self.v_gain
        w = joy_msg.axes[3] * self.v_gain * (-0.2) * 180 / 3.14
        if (joy_msg.axes[6] != 0 or joy_msg.axes[7] != 0):
            Vx = joy_msg.axes[6] * self.v_gain * (-1)
            Vy = joy_msg.axes[7] * self.v_gain
        cmd = "1 3 " + str(Vx) + " "  + str(Vy) + " " + str(w) + "\n"
        self.ser.write(cmd)
        # Arm control
        if(joy_msg.buttons[0]):
            self.servo_ptr = 0
        elif(joy_msg.buttons[1]):
            self.servo_ptr = 1
        elif(joy_msg.buttons[2]):
            self.servo_ptr = 2
        elif(joy_msg.buttons[3]):
            self.servo_ptr = 3
        
        angle = [0, 0, 0, 0]
        if(joy_msg.axes[2] == -1 or joy_msg.axes[5] == -1):
            if(joy_msg.axes[2] == -1):
                angle[self.servo_ptr] = self.arm_angle[self.servo_ptr] - self.ang_gain
            if(joy_msg.axes[5] == -1):
                angle[self.servo_ptr] = self.arm_angle[self.servo_ptr] + self.ang_gain

            cmd = "2 121 " + str(angle[0])\
                + " " + str(angle[1])\
                + " " + str(angle[2])\
                + " " + str(angle[3]) +  "\n"
            self.ser.write(cmd)

        if(joy_msg.buttons[4]):
            cmd = "3 2 " + str(self.slide_encoder - self.encoder_gain) + "\n"
            self.ser.write(cmd)
        if(joy_msg.buttons[5]):
            cmd = "3 2 " + str(self.slide_encoder + self.encoder_gain) + "\n"
            self.ser.write(cmd)

    def cbMorot(self, str_msg):
            if(str_msg.data == "q"):
                self.terminate = True
            else:
                cmd = "1 " + str_msg.data + "\n"
                self.ser.write(cmd)

    def cbArm(self, str_msg):
        str_list = str_msg.data.split()
        action = str_list[0]
        y = int(str_list[1])
        z = int(str_list[2])
        self.moveArm(action, y, z)

    def moveArm(self, action, y, z):
        #action_list = ['Stamp', 'Pick', 'Place', 'Push']
        action_flag = False
        action_dict = {'Stamp': [[222], [18, 24], [20]], 'Pick': [[221], [20, 27], [-14]], 
                       'Place': [[222], [18, 24], [20]], 'Push': [[231], [0, 0], [0]]}
        
        if (y > action_dict[action][1][0]) & (y < action_dict[action][1][1]):
            action_flag = True
            z = action_dict[action][2][0]
        else:
            print('Wrong distance !')
          
        if action_flag:
            action_code = action_dict[action][0][0]
            cmd = '2 ' + str(action_code) + ' ' + str(y) + ' ' + str(z) + '\n'
            print(cmd)
            self.ser.write(cmd)

    def listener(self):
        sleep(1)
        while (self.ser.isOpen() and not self.terminate):
            sleep(self.T/1000.0)
            self.ser.write("4\n")
            s = self.ser.readline()
            arr = s.split(' ')
            print arr
            if(len(arr) >= 10 and arr[0].isdigit()):
                self.car_pose.x = float(arr[2])
                self.car_pose.y = float(arr[3])
                self.car_pose.theta = float(arr[4])
                self.arm_angle[0] = float(arr[5])
                self.arm_angle[1] = float(arr[6])
                self.arm_angle[2] = float(arr[7])
                self.arm_angle[3] = float(arr[8])
                self.slide_encoder = int(arr[9])
                self.pub_pos.publish(self.car_pose);

        self.ser.close()
        rospy.on_shutdown()

if __name__ == '__main__':
    rospy.init_node("Serial_driver",anonymous=False)
    serial_driver = Serial_driver()
    rospy.spin()
