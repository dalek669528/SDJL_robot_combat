#!/usr/bin/env python

import sys
import rospy
import serial
import time
import numpy as np
from std_msgs.msg import String

class Master(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing..." %(self.node_name))
        
        # Publications
        self.pub_msg = rospy.Publisher("arm_cmd", String, queue_size=1)
        self.cmd = String()
        
    #Move
    #def MovetoPoint(self):
    
    
    #def testMove(self):
    
    #Arm   
    def publishArm(self, action, y, z):
        self.cmd.data = action + ' ' + str(y) + ' '  + str(z)
        self.pub_msg.publish(self.cmd)
        
    #def moveArm(self):
    
    
    #def testArm(self):
    
        
    #Camera
    #def testCamera(self):
    
    
    
    #Combine
    #def CheckAndModify(self):
    
        
    def stage_1(self):
        finish_flag = False
        movement = ['Move', 'CheckAndModify', 'MoveArm']
        move_count = 0
        move_number = 4
        while finish_flag == False:
            print('Stage 1 : ', movement)
            if movement == 'Move':
                if move_count < move_number:
                    self.MovetoPoint(move_count)
                    move_count += 1
                    movement = 'CheckAndModify'
                
            elif movement == 'CheckAndModify':
                do_action = self.CheckAndModify()
                movement  = 'MoveArm' if do_action else 'Move'
                
            elif movement == 'MoveArm':
                self.publishArm('Pick', 21, -14)
                movement = 'Move'
      
if __name__ == '__main__':
    rospy.init_node("master",anonymous=False)
    master = Master()
    #master.stage_1()
    
    while(1):
        master.publishArm('Pick', 21, 0)
        time.sleep(10)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down...")

