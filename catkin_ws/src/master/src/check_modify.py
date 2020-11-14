#!/usr/bin/env python
import time
from move import *
from camera.msg import Coordination

def check_modify(self, target_color):
    #subscribe color and coordination
    self.tolerance = 10 #(mm)
    self.target_color = target_color # [?, ?] 0:R, 1:G, 2:B
    self.target_coord = np.array([0, 150]) # [0,15](cm)
    self.object_color = ""
    self.object_coord = np.array([-1, -1, -1])
    # self.color_subscriber = rospy.Subscriber('Color', Int32, self.color_callback, queue_size=1)
    self.coord_subscriber = rospy.Subscriber('Coord', Coordination, self.coord_callback, queue_size=1)
    self.move = Move()

    if ((self.object_color != self.target_color[0]) or (self.object_color != self.target_color[1])):
        print('Not target color')
        return 0
    while(1):
        if (abs(self.target_coord[0] - self.object_coord[0]) > self.tolerance) or (abs(self.target_coord[1] - self.object_coord[1]) > self.tolerance):
            #move to self.object_coord
            Move2PosX(self.target_coord[0]-self.object_coord[0])
            Move2PosY(self.target_coord[1]-self.object_coord[1])
            #sleep
        else:
            print('modify finished')
            return 1

def coord_callback(self, msg):
    try:
        self.object_coord = np.array(msg.data)
        self.object_color = msg.color
    except:
        print('Something wrong in coord Subscriber callback')

# def color_callback(self, msg):
#     try:
#         self.object_color = msg
#     except:
#         print('Something wrong in color Subscriber callback')
def check_modify(self, target_color):
        #subscribe color and coordination
        
        target_color = target_color # [?, ?] 0:R, 1:G, 2:B
        target_coord = np.array([0, 150]) # [0,15](cm)
        
        if ((self.object_color != target_color[0]) or (self.object_color != target_color[1])):
            print('Not target color')
            return 0
        while(1):
            if (abs(target_coord[0] - self.object_coord[0]) > self.tolerance_camera) or (abs(target_coord[1] - self.object_coord[1]) > self.tolerance_camera):
                #move to self.object_coord
                self.Move2Pos_related(target_coord[0]-self.object_coord[0], target_coord[1]-self.object_coord[1])
            else:
                print('modify finished')
                return 1, target_coord