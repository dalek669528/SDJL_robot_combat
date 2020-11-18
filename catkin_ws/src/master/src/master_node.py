#!/usr/bin/env python

import sys
import time
import rospy
import serial
import numpy as np
from time import sleep

from std_msgs.msg import Int32, String
from geometry_msgs.msg import Pose2D
from camera.msg import Coordination, Master_info

class Master(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing..." %(self.node_name))
        

        self.cmd = String()


        # Publications
        self.pub_master_info_msg = rospy.Publisher('master_info', Master_info, queue_size=1)
        self.pub_arm_msg   = rospy.Publisher("arm_cmd", String, queue_size=1)
        self.pub_motor_msg = rospy.Publisher('motor_cmd', String, queue_size=1)
        self.pub_serial_msg = rospy.Publisher('serial_cmd', String, queue_size=1)
        

        # Subscribers
        self.GetPos = rospy.Subscriber('car_pose',Pose2D, self.GetPos_callback, queue_size=1)
        self.coord_subscriber = rospy.Subscriber('Coord', Coordination, self.coord_callback, queue_size=1)
        self.GetPos_arm = rospy.Subscriber('arm_pose',Pose2D, self.GetPosArm_callback, queue_size=1)
    

        self.stage_index = 0
        #Arm variable
        self.arm_y = 0
        self.arm_z = 0
        self.arm_action_list =  [['Stamp'],
                                ['Pick','Place'],
                                ['Push']]
        self.armflag = 0
        self.armY = 0
        self.armZ = 0

        #Camera variable
        self.master_info = Master_info()
        self.target_color_list = [['red', 'green'], ['green', 'blue'], ['green']]
        self.target_offset_list = [1, 1.5, 7.5, 2]
        self.target_coord_list = [[0, 200], [0, 185], [0, 100]]
        self.color_list = [[1, 1, 0], [0, 1, 1], [0, 1, 0]]
        self.detect_bounding_list = [[100, 100, 0, 100], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.object_color = ""
        self.object_coord = np.array([-1, -1, -1])
        self.tolerance_camera = 10 #(mm)
        

        #Move variable
        self.desire_x = 0
        self.desire_y = 0
        self.desire_theta = 0
        self.x = 0
        self.y = 0
        self.theta = 0
        self.tolerance_move = 1
        self.cmd = String()
        self.maps = []
        self.map1 = [['x','-10','y','50'],
                    ['x','-70','y','125'],
                    ['x','-10','y','200'],
                    ['x','-70','y','340']]
        
        self.map2=[['x','-5','y','70'],
                  ['x','-2.5','y','133'],
                  ['y','110','x','-65'],
                  ['x','-67.5','y','173'],
                  ['x','-35','y','350']]

        self.map3=[['y','244.76','x','-70','y','306.16','x','0']]
        # the map for doing calibration by the board
        # self.map3=[['y','244.76'],
        #           ['x','-70','y','306.16','x','0']]
        self.maps.append([self.map1, self.map2, self.map3])
        self.maps = self.maps[0]

        self.stop()


    #Camera
    def coord_callback(self, msg):
        try:
            self.object_coord = np.array(msg.data)
            self.object_color = msg.color
        except:
            print('Something wrong in coord Subscriber callback')
        
    #Move
    def GetPos_callback(self, data):
        self.x = data.x
        self.y = data.y
        self.theta = data.theta

    def Move2Pos(self,x, y):
        self.desire_x = x
        self.desire_y = y
        cmd= "4 " + str(x) + " "  + str(y) + " " + str(self.desire_theta)
        self.pub_motor_msg.publish(cmd)
        while((abs(self.x-self.desire_x)>self.tolerance_move) or (abs(self.y-self.desire_y)>self.tolerance_move)): 
            pass

    def Move2Pos_related(self,x, y):
        self.desire_x += x
        self.desire_y += y
        cmd = "5 " + str(x) + " "  + str(y) + " " + str(self.desire_theta)
        #cmd= "4 " + str(self.desire_x) + " "  + str(self.desire_y) + " " + str(self.desire_theta)
        self.pub_motor_msg.publish(cmd)
        print('In move while !')
        t = time.time()
        while((abs(self.x-self.desire_x)>self.tolerance_move) or (abs(self.y-self.desire_y)>self.tolerance_move)): 
            #print(self.x, self.y)
            #print(self.desire_x, self.desire_y)
            #print('\n')
            if((time.time()-t)>3):
                print("wait too long")
                break
            pass
        print('Out move while !')

    def Move2PosX(self,data):
        self.desire_x = data
        self.cmd.data = "4 " + str(self.desire_x) + " "  + str(self.desire_y) + " " + str(self.desire_theta)
        self.pub_motor_msg.publish(self.cmd)
        while((abs(self.x-self.desire_x)>self.tolerance_move) or (abs(self.y-self.desire_y)>self.tolerance_move)): 
            pass
        
    def Move2PosY(self,data):
        self.desire_y = data
        self.cmd.data = "4 " + str(self.desire_x) + " "  + str(self.desire_y) + " " + str(self.desire_theta)
        self.pub_motor_msg.publish(self.cmd)
        while((abs(self.x-self.desire_x)>self.tolerance_move) or (abs(self.y-self.desire_y)>self.tolerance_move)): 
            pass

    def Move2PosS13(self, stage_index, move_index):
        for i in range(0,len(self.maps[stage_index][move_index]),2):
            if(self.maps[stage_index][move_index][i]=='y'):
                self.Move2PosY(float(self.maps[stage_index][move_index][i+1]))
            else:
                self.Move2PosX(float(self.maps[stage_index][move_index][i+1]))
    
    def stop(self):
        self.cmd.data = "0 "
        self.pub_serial_msg.publish(self.cmd)
    
    #Arm   
    def publishArm(self, action, y, z):
        self.cmd.data = action + ' ' + str(y) + ' '  + str(z)
        self.pub_arm_msg.publish(self.cmd)
    
    def GetPosArm_callback(self, data):
        self.armY = data.x
        self.armZ = data.y
        self.armflag = data.theta

    #Combine
    def check_modify(self, target_color, move_count):
        #subscribe color and coordination
        self.master_info.stage = self.stage_index
        self.master_info.open_flag = 1
        self.master_info.bounding = self.detect_bounding_list[self.stage_index]
        self.master_info.color = self.color_list[self.stage_index]
        self.pub_master_info_msg.publish(self.master_info)

        # sleep(5)
        target_coord =  self.target_coord_list[self.stage_index]# [0,20](cm)
        print(self.object_color)
        if ((self.object_color != target_color[0]) and (self.object_color != target_color[1])):
            if self.stage_index == 0:
                self.Move2Pos_related(0, 20)

            print('Skip')
            return False, 0, 0
        else:
            object_coord = self.object_coord.copy()
            print(object_coord)
        
        while(abs(self.object_coord[0] - target_coord[0]) > self.tolerance_camera):
            if(self.object_color == 'Nothing'): # Nothing detected!!!
                print('Nothing detected!!!')
                break
            print('move: '+str((self.object_coord[0] - target_coord[0])/10))
            self.Move2Pos_related((self.object_coord[0] - target_coord[0])/10, 0)
            sleep(1)
        
            #if ((abs(target_coord[0] - object_coord[0]) > self.tolerance_camera)) or ((abs(target_coord[1] - object_coord[1]) > self.tolerance_camera)):
        # print('Object pos : ', self.object_coord[0], self.object_coord[1])
        # print('Desire move(relatef): ', (self.object_coord[0] - target_coord[0])/10, (self.object_coord[1] - target_coord[1])/10)
        # self.Move2Pos_related((self.object_coord[0] - target_coord[0])/10, 0)
        # sleep(3)
        object_coord = self.object_coord.copy()
        self.Move2Pos_related(0, (object_coord[1] - target_coord[1])/10)
        sleep(1)
        
        self.master_info.open_flag = 0
        self.pub_master_info_msg.publish(self.master_info)
        print('modify finished', object_coord[1])
        if self.stage_index == 0:
            return True, (target_coord[1])/10, object_coord[2]/10
        elif (self.stage_index == 1) and move_count%2 == 0:
            return True, (self.object_coord[1]+1.5)/10, self.object_coord[2]/10
        elif (self.stage_index == 1) and move_count%2 == 1:
            return True, (self.object_coord[1]+7.5)/10, self.object_coord[2]/10
        elif self.stage_index == 2:
            return True, (self.object_coord[1]+2)/10, self.object_coord[2]/10

    def stage(self, index):
        finish_flag = False
        self.master_info.open_flag = 0
        self.pub_master_info_msg.publish(self.master_info)
        self.stage_index = index
        move_number = len(self.maps[self.stage_index])
        arm_action_number = len(self.arm_action_list[self.stage_index])
        print('\n\nGet in Stage ' + str(self.stage_index) + ',  move_munber : ' + str(move_number) + ' arm_action_number : ' + str(arm_action_number))
        
        # self.pub_master_info_msg.publish(self.stage_index) # publish current stage to preproc_node.py to change between rgb/BGremoved_rgb
        move_count = 0
        arm_action_count = 0
        movement = 'Move'
        while finish_flag == False and (not rospy.is_shutdown()):
            print('\nMovement : ' + movement)
            if movement == 'Move':
                if move_count < (move_number):
                    print('Move task : '+  str(move_count))
                    self.Move2PosS13(self.stage_index,move_count)
                    move_count += 1
                    movement = 'CheckAndModify'
                else:
                    finish_flag = True    
                
            elif movement == 'CheckAndModify':
                action_flag, self.arm_y, self.arm_z= self.check_modify(self.target_color_list[self.stage_index], move_count)                
                print('Do action or not : ' + str(action_flag))
                movement  = 'MoveArm' if action_flag else 'Move'

            elif movement == 'MoveArm':
                arm_action = self.arm_action_list[self.stage_index][arm_action_count % arm_action_number]
                print(arm_action + ' ' + str(self.arm_y) + ' ' + str(self.arm_z))
                if(self.arm_y > self.armY):
                    self.publishArm(arm_action, self.arm_y, self.arm_z)
                sleep(0.5)
                while(not(self.armflag)):
                    pass
                self.Move2Pos_related(0,self.arm_y-self.armY)
                arm_action_count += 1
                movement = 'Move'
        self.master_info.open_flag = 0
        self.pub_master_info_msg.publish(self.master_info)
        print('\n\nGet out Stage ' + str(self.stage_index))

    def test(self, index):
        finish_flag = False
        self.master_info.open_flag = 0
        self.pub_master_info_msg.publish(self.master_info)
        self.stage_index = index
        move_number = len(self.maps[self.stage_index])
        arm_action_number = len(self.arm_action_list[self.stage_index])
        print('\n\nGet in Stage ' + str(self.stage_index) + ',  move_munber : ' + str(move_number) + ' arm_action_number : ' + str(arm_action_number))
        
        # self.pub_master_info_msg.publish(self.stage_index) # publish current stage to preproc_node.py to change between rgb/BGremoved_rgb
        move_count = 0
        arm_action_count = 0
        movement = 'Move'
        action_flag, self.arm_y, self.arm_z= self.check_modify(self.target_color_list[self.stage_index], move_count)                
        print('Do action or not : ' + str(action_flag))
        movement  = 'MoveArm' if action_flag else 'Move'
        arm_action = self.arm_action_list[self.stage_index][arm_action_count % arm_action_number]
        print(arm_action + ' ' + str(self.arm_y) + ' ' + str(self.arm_z))
        if(self.arm_y > self.armY):
            self.publishArm(arm_action, self.arm_y, self.arm_z)
        sleep(0.5)
        while(not(self.armflag)):
            pass
        self.Move2Pos_related(0,self.arm_y-self.armY)
        arm_action_count += 1
        movement = 'Move'


if __name__ == '__main__':
    rospy.init_node("master",anonymous=False)
    master = Master()
    sleep(0.5)

    #master.stage(0)
    master.stage(1)
    # master.test(0)

    master.stop()

    # while(not rospy.is_shutdown()):
    #     master.cmd.data = raw_input('INPUT (\'q\' to quit):')
    #     if(master.cmd.data == "q"):
    #         break
    #     master.pub_arm_msg.publish(master.cmd)
        