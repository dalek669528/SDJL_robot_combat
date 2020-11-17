#!/usr/bin/env python3

import sys
import rospy
import argparse
from PIL import Image
from yolo import YOLO
from cv_bridge import CvBridge, CvBridgeError

from sensor_msgs.msg import Image

class Detector(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        # Publications
        #self.DetectResult = rospy.Publisher('DetectResult', , queue_size=1) # publish coordination of max color

        # Subscriptions
        #self.DetectImage = rospy.Subscriber('DetectImage', Image, self.DetectImage_callback, queue_size=1)
        self.DetectImage = rospy.Subscriber('RawRGB', Image, self.DetectImage_callback, queue_size=1)
    
        self.yolo = YOLO()
        self.detect_img()
   
    def detect_img(self):
        while True:
            img = input('Input image filename:')
            try:
                image = Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                r_image,roi_info = self.yolo.detect_image(image)
                print(roi_info)
                r_image.show()
        #self.yolo.close_session()

    def DetectImage_callback(self, data):
       
        rgb_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
        r_image,roi_info = self.yolo.detect_image(rgb_image)
        print(roi_info)
        r_image.show()
    
if __name__ == '__main__':

    rospy.init_node("ImageDetector", anonymous=False)
    detector = Detector()
    detector.yolo.close_session()