#!/usr/bin/env python

import sys
import rospy
import serial
import numpy as np
from std_msgs.msg import String

class Arm_driver(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing..." %(self.node_name))
        
        # Subscriptions
        self.sub_cmd = rospy.Subscriber("arm_cmd", String, self.cbCMD, queue_size=1)
        
        self.ser = serial.Serial(
            port='/dev/ttyACM1',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )   
        
        
    def cbCMD(self, str_msg):
        str_list = str_msg.data.split()
        action = str_list[0]
        y = int(str_list[1])
        z = int(str_list[2])
        self.moveArm(action, y, z)
        
    def moveArm(self, action, y, z):
        #action_list = ['Stamp', 'Pick', 'Place', 'Push']
        action_flag = False
        action_dict = {'Stamp': [[211], [0, 0], [0]],    'Pick': [[221], [20, 27], [-14]], 
                       'Place': [[222], [18, 24], [20]], 'Push': [[231], [0, 0], [0]]}
        
        if (y > action_dict[action][1][0]) & (y < action_dict[action][1][1]):
            action_flag = True
            z = action_dict[action][2][0]
        else:
            print('Wrong distance !')
          
        if action_flag:
            action_code = action_dict[action][0][0]
            cmd = str(action_code) + ' ' + str(y) + ' ' + str(z) + '\n'
            print(cmd)  
            self.ser.write(cmd)
        
if __name__ == '__main__':
    rospy.init_node("arm_driver",anonymous=False)
    arm_driver = Arm_driver()
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down...")
