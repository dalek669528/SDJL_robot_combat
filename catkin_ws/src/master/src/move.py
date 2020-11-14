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

        self.desire_x = 0
        self.desire_y = 0
        self.desire_theta = 0
        self.x = 0
        self.y = 0
        self.theta = 0
        self.cmd = String()
        self.maps = []
        self.map1 = [['x','-10''y','70'],
                    ['x','-60','y','145'],
                    ['x','-10','y','220'],
                    ['x','-60','y','340','x','0']]
        
        self.map2=[['x','-5','y','85'],
                  ['x','-2.5','y','153'],
                  ['y','125','x','-65','y','125'],
                  [,'x','-67.5','y','193'],
                  ['x','-35','y','350','x','0']]

        self.map3=[['y','244.76','x','-70','y','306.16','x','0']]

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
    
    # def Move2Pos(self,data):
    #     cmd= "4 " + str(data.x) + " "  + str(data.y) + " " + str(data.theta)
    #     self.pub_msg.publish(cmd)
        
    def Move2PosX(self,data):
        self.desire_x = data
        self.cmd.data = "4 " + str(self.desire_x) + " "  + str(self.desire_y) + " " + str(self.desire_theta)
        self.pub_msg.publish(self.cmd)
        while((abs(self.x-self.desire_x)>0.2) or (abs(self.y-self.desire_y)>0.2)): 
            sleep(0.5)
        
    def Move2PosY(self,data):
        self.desire_y = data
        self.cmd.data = "4 " + str(self.desire_x) + " "  + str(self.desire_y) + " " + str(self.desire_theta)
        self.pub_msg.publish(self.cmd)
        while((abs(self.x-self.desire_x)>0.2) or (abs(self.y-self.desire_y)>0.2)): 
            sleep(0.5)
    
    # def Move2Pos1(self):
    #     self.Move2PosY(70)
    
    # def Move2Pos2(self):
    #     self.Move2PosX(-70)
    #     self.Move2PosY(145)
    
    # def Move2Pos3(self):
    #     self.Move2PosX(0)
    #     self.Move2PosY(220)
            
    # def Move2Pos4(self):
    #     self.Move2PosX(-70)
    #     self.Move2PosY(340)
    #     self.Move2PosX(0)
        
    def Move2PosS13(self, stage_index, move_index):
        for i in range(0,len(self.maps[stage_index][move_index]),2):
            if(self.maps[stage_index][move_index][i]=='y'):
                self.Move2PosY(int(self.maps[stage_index][move_index][i+1]))
            else:
                self.Move2PosX(int(self.maps[stage_index][move_index][i+1]))

    # def Move2PosS13(self):

    def stop(self):
        self.cmd.data = "0 "
        self.pub_msg.publish(self.cmd)
    
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
    for i in range(5):
      move.Move2PosS13(1,i);

    move.stop()
