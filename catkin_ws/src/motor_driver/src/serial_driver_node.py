#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import Joy
from time import sleep
import serial
import struct

def shutdowm():
    print("Shotdoun ")

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
        self.T = 500        # ms

        self.car_pose = Pose2D()
        self.v_gain = 25

        self.arm_angle = [0, 0, 0, 0]
        self.servo_ptr = 0;
        self.ang_is_moving = False;

        self.slide_encoder = 0;
        self.encoder_gain = 200

        # Publications
        self.pub_pos = rospy.Publisher("position", Pose2D, queue_size=1)

        # Subscriptions
        self.sub_cmd = rospy.Subscriber("serial_cmd", String, self.cbSerial, queue_size=1)
        self.sub_cmd = rospy.Subscriber("motor_cmd", String, self.cbMorot, queue_size=1)
        self.sub_cmd = rospy.Subscriber("arm_cmd", String, self.cbArm, queue_size=1)
        self.sub_joy = rospy.Subscriber("joy", Joy, self.cbJoy, queue_size=1)
        self.listener()


    def cbJoy(self, joy_msg):
        if(joy_msg.buttons[6]): 
            # terminate node
            self.ser.write("0\n")
            self.terminate = True
        if(joy_msg.buttons[7]):
            # reset car
            cmd = "0\n"
            # print(cmd)
            self.ser.write(cmd)
        # Pose control 
        Vx = joy_msg.axes[0] * self.v_gain * (-1)
        Vy = joy_msg.axes[1] * self.v_gain
        w = joy_msg.axes[3] * self.v_gain * (-0.2) * 180 / 3.14
        if (joy_msg.axes[6] != 0 or joy_msg.axes[7] != 0):
            Vx = joy_msg.axes[6] * self.v_gain * (-1)
            Vy = joy_msg.axes[7] * self.v_gain
        cmd = "1 3 " + str(Vx) + " "  + str(Vy) + " " + str(w) + "\n"
        # print(cmd)
        self.ser.write(cmd)
        # Arm control
        if(joy_msg.buttons[0]):
            self.servo_ptr = 0
        elif(joy_msg.buttons[1]):
            self.servo_ptr = 1
        elif(joy_msg.buttons[2]):
            self.servo_ptr = 2

        if(joy_msg.buttons[3]):
            cmd = "2 311\n"
            # print(cmd)
            self.ser.write(cmd)
        
        angle = [0, 0, 0, 0]
        for i in range(4):
            angle[i] = self.arm_angle[i]
        if(joy_msg.axes[2] < 0 or joy_msg.axes[5] < 0):
            self.ang_is_moving = True
            ratio = 0
            direct = 0
            if(joy_msg.axes[2] != 1):
                ratio = (joy_msg.axes[2] - 1) * -0.5
                direct = 1
            if(joy_msg.axes[5] != 1):
                ratio = (joy_msg.axes[5] - 1) * -0.5
            cmd = "2 122 " + str(self.servo_ptr) + " " + str(ratio) + " " + str(direct) +  "\n"
            # print(cmd)
            self.ser.write(cmd)
        elif(self.ang_is_moving):
            self.ang_is_moving = False
            cmd = "2 122 -1 0 \n"
            # print(cmd)
            self.ser.write(cmd)
        if(joy_msg.buttons[4]):
            cmd = "3 2 " + str(self.slide_encoder - self.encoder_gain) + "\n"
            # print(cmd)
            self.ser.write(cmd)
        if(joy_msg.buttons[5]):
            cmd = "3 2 " + str(self.slide_encoder + self.encoder_gain) + "\n"
            # print(cmd)
            self.ser.write(cmd)

    def cbSerial(self, str_msg):
        if(str_msg.data == "q"):
            self.terminate = True
        else:
            cmd = str_msg.data + "\n"
            self.ser.write(cmd)

    def cbMorot(self, str_msg):
        cmd = "1 " + str_msg.data + "\n"
        self.ser.write(cmd)

    def cbArm(self, str_msg):
        str_list = str_msg.data.split()
        action = str_list[0]
        y = float(str_list[1])
        z = float(str_list[2])
        self.moveArm(action, y, z)

    def moveArm(self, action, y, z):
        #action_list = ['Stamp', 'Pick', 'Place', 'Push']
        action_flag = False
        action_dict = {'Stamp': [[222], [7, 26], [20]], 'Pick': [[221], [12.5, 21.5], [-14]], 
                       'Place': [[222], [7, 26], [20]], 'Push': [[222], [7, 26], [20]]}
        
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
        while (self.ser.isOpen() and (not self.terminate) and (not rospy.is_shutdown())):
            # sleep(self.T/1000.0)
            # self.ser.write("4\n")
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
        sys.exit(0)
        
if __name__ == '__main__':
    rospy.init_node("Serial_driver", anonymous=False)
    serial_driver = Serial_driver()
    # rospy.spin()
