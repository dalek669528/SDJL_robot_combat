#!/usr/bin/env python3

import sys
import rospy
import argparse
import numpy as np
from PIL import Image as Img
from yolo import YOLO
#from cv_bridge import CvBridge, CvBridgeError
from time import sleep
from sensor_msgs.msg import Image

class Detector(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))
        self.yolo = YOLO()
        image = Img.open('/home/dick/SDJL_robot_combat/catkin_ws/src/camera/src/init.png')
        r_image = self.yolo.detect_image(image)

        # Publications
        #self.DetectResult = rospy.Publisher('DetectResult', , queue_size=1) # publish coordination of max color

        # Subscriptions
        #self.DetectImage = rospy.Subscriber('DetectImage', Image, self.DetectImage_callback, queue_size=1)
        self.DetectImage = rospy.Subscriber('RawRGB', Image, self.DetectImage_callback, queue_size=1)
    
        #self.detect_img()
   
    def DetectImage_callback(self, data):
        array = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
        image_array = array.copy()
        image_array[:, :, 0] = array[:, :, 2]
        image_array[:, :, 2] = array[:, :, 0]

        rgb_image = Img.fromarray(image_array) 
        #rgb_image.show()
        r_image,roi_info = self.yolo.detect_image(rgb_image)
        print('Result', roi_info)
        #r_image.show()
    
if __name__ == '__main__':

    rospy.init_node("ImageDetector", anonymous=False)
    detector = Detector()
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        detector.yolo.close_session()
        print("Shutting Down...")

