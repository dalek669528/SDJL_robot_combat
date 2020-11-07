#!/usr/bin/env python
import time
from camera.msg import Coordination

def check_modify(self, target_color):
    #subscribe color and coordination
    self.target_color = target_color
    self.target_coord = np.array([x, y])
    self.object_color = -1
    self.object_coord = np.array([-1, -1, -1, -1])
    self.color_subscriber = rospy.Subscriber('Color', Int32, self.color_callback, queue_size=1)
    self.coord_subscriber = rospy.Subscriber('Coord', Coordination, self.coord_callback, queue_size=1)

    if self.object_color != self.target_color:
        print('Not target color')
        return 
    while(1):
        if self.target_coord != self.object_coord:
            #move to self.object_coord
            move(self.target_coord[0]-self.object_coord, self.target_coord[1]-self.object_coord)
        else:
            print('modify finished')


def color_callback(self, msg):
    self.object_color = msg



    
def coord_callback(self, msg):
    self.object_coord = np.array(msg.data)