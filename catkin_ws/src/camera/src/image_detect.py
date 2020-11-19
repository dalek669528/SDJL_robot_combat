#!/usr/bin/env python3

import sys
import rospy
import argparse
import numpy as np
from PIL import Image as Img
from yolo import YOLO
from time import sleep
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray

class Detector(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))
        self.yolo = YOLO()
        image = Img.open('/home/dick/SDJL_robot_combat/catkin_ws/src/camera/src/init.png')
        r_image = self.yolo.detect_image(image)
        #self.image_array = np.zeros((360, 640, 3))
        #self.is_yolo_ready = True

        # Publications
        self.DetectResult = rospy.Publisher('DetectResult', Float32MultiArray, queue_size=1)
        # Subscriptions
        self.DetectImage = rospy.Subscriber('DetectImage', Image, self.DetectImage_callback, queue_size=1)
        sleep(1)
        self.DetectResult.publish(Float32MultiArray(data=np.array([0.0])))
   

    def DetectImage_callback(self, data):
        
        array = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
        image_array = array.copy()
        image_array[:, :, 0] = array[:, :, 2]
        image_array[:, :, 2] = array[:, :, 0]

        rgb_image = Img.fromarray(image_array) 
        #rgb_image.show()
        r_image,roi_info = self.yolo.detect_image(rgb_image)
        roi_info_array = roi_info if (roi_info != []) else [0.0]
        roi_info_array = np.array(roi_info_array).flatten()
        print('Result', roi_info_array)
        #r_image.show()
        ros_roi_array = Float32MultiArray(data=roi_info_array)
        self.DetectResult.publish(ros_roi_array)

if __name__ == '__main__':
    rospy.init_node("ImageDetector", anonymous=False)
    detector = Detector()
    rospy.spin()
    
