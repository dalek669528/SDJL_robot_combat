#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D
import struct
from time import sleep
import numpy as np

class Move(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing..." %(self.node_name))
        self.x = 0
        self.y = 0
        self.theta = 0
        self.cmd = String()
        self.maps = []
        self.map1 = [['y','70'],
                    ['x','-70','y','145'],
                    ['x','0','y','220'],
                    ['x','-70','y','340','x','0']]
        
        self.map2=[]
        self.map3=[['y','244.76','x','-70','y','306.16']]

        self.maps.append([self.map1, self.map2, self.map3])
        self.maps = self.maps[0]
        
        # Subscribers
        self.GetPos = rospy.Subscriber('position',Pose2D, self.GetPos_callback, queue_size=1)

        # Publishers
        self.pub_msg = rospy.Publisher('motor_cmd', String, queue_size=1)
        

    def GetPos_callback(self, data):
        self.x = data.x;
        self.y = data.y;
        self.theta = data.theta;
    
    def Move2Pos(self,data):
        cmd= "4 " + str(data.x) + " "  + str(data.y) + " " + str(data.theta)
        self.pub_msg.publish(cmd)
        
    def Move2PosX(self,data):
        self.cmd.data = "4 " + str(data) + " "  + str(self.y) + " " + str(self.theta)
        self.pub_msg.publish(self.cmd)
        while(abs(self.x-data)>0.5): 
            sleep(0.5)
        
    def Move2PosY(self,data):
        self.cmd.data = "4 " + str(self.x) + " "  + str(data) + " " + str(self.theta)
        self.pub_msg.publish(self.cmd)
        while(abs(self.y-data)>0.5): 
            sleep(0.5)
    
    def Move2Pos1(self):
        self.Move2PosY(70)
    
    def Move2Pos2(self):
        self.Move2PosX(-70)
        self.Move2PosY(145)
    
    def Move2Pos3(self):
        self.Move2PosX(0)
        self.Move2PosY(220)
            
    def Move2Pos4(self):
        self.Move2PosX(-70)
        self.Move2PosY(340)
        self.Move2PosX(0)
        
    def Move2PosS1(self, stage_index, move_index):
        for i in range(0,len(self.maps[stage_index][move_index]),2):
            if(self.maps[stage_index][move_index][i]=='y'):
                self.Move2PosY(int(self.maps[stage_index][move_index][i+1]))
            else:
                self.Move2PosX(int(self.maps[stage_index][move_index][i+1]))
    
if __name__ == '__main__':
    rospy.init_node("Move",anonymous=False)
    move = Move()
    sleep(0.5)
#    print('1')
#    move.Move2Pos1()
#    print(move.x,move.y)
#    print('2')
#    move.Move2Pos2()
#    print(move.x,move.y)
#    print('3')
#    move.Move2Pos3()
#    print(move.x,move.y)
#    print('4')
#    move.Move2Pos4()
#    print(move.x,move.y)
    for i in range(4):
      move.Move2PosS1(0,i);
