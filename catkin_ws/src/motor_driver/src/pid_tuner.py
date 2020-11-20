#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import String, Int32
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import Joy
from time import sleep
import serial
import struct

def shutdowm():
    print("Shotdoun ")

class PID_Turner(object):
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

        self.cmd = ""
        self.is_readed = False
        self.stage = -1

        self.PID[] = [[1, 0.5, 2], [1, 0.5, 2], [1, 0.5, 2], [1, 0.5, 2], [1, 0, 4]]
        
        self.start_timer = 0
        self.timer = 0
        self.x = 0
        self.y = 0
        self.theta = 0
        self.Vx = 0
        self.Vy = 0
        self.w = 0
        self.Va = 0
        self.Vb = 0
        self.Vc = 0
        self.Vd = 0

        self.v_err = [0, 0, 0, 0]
        self.pos_err = 0

        self.slide_encoder = Int32();
        self.encoder_gain = 200

        # Publications

        # Subscriptions
        self.sub_cmd = rospy.Subscriber("serial_cmd", String, self.cbSerial, queue_size=1)
        self.sub_joy = rospy.Subscriber("joy", Joy, self.cbJoy, queue_size=1)
        self.listener()

    def cbSerial(self, str_msg):
        self.cmd = str_msg.data

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
            cmd = "3 2 " + str(self.slide_encoder.data - self.encoder_gain) + "\n"
            # print(cmd)
            self.ser.write(cmd)
        if(joy_msg.buttons[5]):
            cmd = "3 2 " + str(self.slide_encoder.data + self.encoder_gain) + "\n"
            # print(cmd)
            self.ser.write(cmd)

    def listener(self):
        sleep(5)
        self.ser.write("4 2\n")
        for _ in range(8):
            s = self.ser.readline()
        while (self.ser.isOpen() and (not self.terminate) and (not rospy.is_shutdown())):
            s = self.ser.readline()
            arr = s.split(' ')
            print arr
            if(len(arr) == 20 and arr[0].isdigit()):
                self.timer = arr[0]
                self.x = arr[2]
                self.y = arr[3]
                self.theta = arr[4]
                self.Vx = arr[6]
                self.Vy = arr[7]
                self.w = arr[8]
                self.Va = arr[10]
                self.Vb = arr[11]
                self.Vc = arr[12]
                self.Vd = arr[13]
                self.Ena = arr[15]
                self.Enb = arr[16]
                self.Enc = arr[17]
                self.End = arr[18]
            if(not is_readed):
                is_readed = True
                cmd_arr = self.cmd.split(' ')
                if(self.cmd_arr[0] == "q")
                    break;
                elif(self.cmd_arr[0].isdigit())
                    w = int(cmd_arr[0])
                    if(w >= 0 and w <= 4 ):
                        cmd = "1 -1 " + cmd_arr[0] + " "  + cmd_arr[1] + " " + cmd_arr[2] + " " + cmd_arr[3] + "\n"
                        self.ser.write(cmd)
                    elif(w == -1):
                        cmd = "1 -1 0 "  + cmd_arr[1] + " " + cmd_arr[2] + " " + cmd_arr[3] + "\n"
                        self.ser.write(cmd)
                        cmd = "1 -1 1 "  + cmd_arr[1] + " " + cmd_arr[2] + " " + cmd_arr[3] + "\n"
                        self.ser.write(cmd)
                        cmd = "1 -1 2 "  + cmd_arr[1] + " " + cmd_arr[2] + " " + cmd_arr[3] + "\n"
                        self.ser.write(cmd)
                        cmd = "1 -1 3 "  + cmd_arr[1] + " " + cmd_arr[2] + " " + cmd_arr[3] + "\n"
                        self.ser.write(cmd)
                elif(self.cmd_arr[0] == "s"):
                    self.is_start = True
                    self.start_timer = self.timer
            if(self.is_start):

                    cmd = "1 3 0 10 0\n"
                    self.ser.write(cmd)


                    cmd = "1 3 0 10 0\n"
                    self.ser.write(cmd)






        self.ser.write("4 0\n")
        self.ser.close()
        sys.exit(0)
        
if __name__ == '__main__':
    rospy.init_node("PID_Turner", anonymous=False)
    turner = PID_Turner()
    # rospy.spin()
