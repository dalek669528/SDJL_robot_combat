#!/usr/bin/env python

import cv2
import rospy
import numpy as np
import pyrealsense2 as rs
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from detectROI import detect_color
from crop_ROI  import crop_depth
from calculateXY import calculate_coordinate

class Preprocess(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing..." %(self.node_name))
        self.image_width  = 640
        self.image_height = 360
        self.fps = 15
        self.pipeline = rs.pipeline()
        self.depth_image = np.zeros((360, 640))
        self.removeBG_image = np.zeros((360, 640))

        # Subscribers
        self.RawRGB = rospy.Subscriber('RawRGB', Image, self.RGB_callback, queue_size=1)
        self.RawDepth = rospy.Subscriber('RawDepth', Image, self.Depth_callback, queue_size=1)
        self.RemoveBG = rospy.Subscriber('RemoveBG', Image, self.RemoveBG_callback, queue_size=1)

        # Publishers
        #self.Publisher_RGB = rospy.Publisher('CropedRGB', Image, queue_size=1) # RGB publish
        #self.CroppedRBG = rospy.Publisher('CropedRGB', Image, queue_size=1) # Depth publish
        #self. = rospy.Publisher('', Image, queue_size=1) # Removed BG publish

    def RGB_callback(self, data):
        try:
            raw_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
        except CvBridgeError as e:
            print(e)

        flipped_image = cv2.flip(raw_image, -1)

        # get detected image and an array of the coordination of the object
        detected_image, roi_array = detect_color(self.removeBG_image)
        #print(roi_array)
        cv2.imshow('Detected image', detected_image)
        cv2.waitKey(1)

        
        depth_img_array = crop_depth(roi_array, self.depth_image) # return image (x, y, depth)
        print(depth_img_array)
        coordinate_array = calculate_coordinate(depth_img_array)
        print(coordinate_array) # (x, y(depth), h)

        # publish
        #msg_RGB = CvBridge().cv2_to_imgmsg(flipped_image)
        #self.Publisher_RGB.publish(msg_RGB)

    def Depth_callback(self, data):
        try:
            raw_image = CvBridge().imgmsg_to_cv2(data, "16UC1")
        except CvBridgeError as e:
            print(e)

        flipped_image = cv2.flip(raw_image, -1)
        self.depth_image = flipped_image.copy()

    def RemoveBG_callback(self, data):
        try:
            raw_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
        except CvBridgeError as e:
            print(e)

        flipped_image = cv2.flip(raw_image, -1)
	self.removeBG_image = flipped_image.copy()

    #def PublishMSG(self, msg):

if __name__ == '__main__':
    rospy.init_node("ImagePreprocess",anonymous=False)
    preprocess = Preprocess()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down...")
