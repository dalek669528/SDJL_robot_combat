#!/usr/bin/env python

import cv2
import rospy
import numpy as np
import pyrealsense2 as rs
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Int32, Int32MultiArray
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
        self.stage_one = -1
        self.stage_three = -1
        self.target_color = -1
        # Subscribers
        self.RawRGB = rospy.Subscriber('RawRGB', Image, self.RGB_callback, queue_size=1)
        self.RawDepth = rospy.Subscriber('RawDepth', Image, self.Depth_callback, queue_size=1)
        self.RemoveBG = rospy.Subscriber('RemoveBG', Image, self.RemoveBG_callback, queue_size=1)

        # Publishers
        self.Color = rospy.Publisher('Color', Int32, queue_size=1) # publish max detected color
        self.Coord = rospy.Publisher('Coord', Int32MultiArray, queue_size=1) # publish coordination of max color
        #self.Publisher_RGB = rospy.Publisher('CropedRGB', Image, queue_size=1) # RGB publish
        #self.CroppedRBG = rospy.Publisher('CropedRGB', Image, queue_size=1) # Depth publish
        #self. = rospy.Publisher('', Image, queue_size=1) # Removed BG publish

    def StageOne(self, enable, roi_array, color_count):
        if enable < 0:
            return 0
        x1 = roi_array[:, 0]
        y1 = roi_array[:, 1]
        x2 = roi_array[:, 2]
        y2 = roi_array[:, 3]
        w = x2 - x1
        h = y2 - y1
        area = w * h
        max_index = np.argmax(area)
        if max_index < color_count[0]:
            max_color = 0
        elif max_index < color_count[0] + color_count[1]:
            max_color = 1
        elif max_index < color_count.sum:
            max_color = 2
        print(max_color)

        max_roi = roi_array[max_index, :].reshape([1, 4])
        depth_img_array = crop_depth(max_roi, self.depth_image) # return detected array(x, y, depth)
        coordinate_array = calculate_coordinate(depth_img_array)
        print(coordinate_array) # array(x, y(depth), h)

        #publish
        color_msg = Int32()
        coord_msg = Int32MultiArray()
        color_msg.data = max_color
        coord_msg.data = coordinate_array
        self.Color.publish(color_msg)
        self.Coord.publish(coord_msg)

    def StageTwo(self, color, roi_array, color_count):
        #remember to filt if green or blue are not detected!!!
        if (color == 1)&(color_count[1] > 0):
            target_array = roi_array[color_count[0]:color_count[0]+color_count[1], :]
        elif (color == 2)&(color_count[2] > 0):
            target_array = roi_array[color_count[0]+color_count[1]:sum(color_count), :]
        else:
            return

        depth_img_array = crop_depth(target_array, self.depth_image)
        sorted_index = np.argsort(depth_img_array[:, 2])
        closest = depth_img_array[sorted_index[0], :].reshape([1, 3])
        coordination = calculate_coordinate(closest)
        print(coordination)

        #publish
        coord_msg = Int32MultiArray()
        coord_msg.data = coordination
        self.Coord.publish(coord_msg)

    def StageThree(self, enable, roi_array, color_count):
        if (enable < 0) | (color_count[1] == 0):
            return 0
        green_array = roi_array[color_count[0]:color_count[0]+color_count[1]:, :]
        x1 = green_array[:, 0]
        y1 = green_array[:, 1]
        x2 = green_array[:, 2]
        y2 = green_array[:, 3]
        w = x2 - x1
        h = y2 - y1
        area = w * h
        max_index = np.argmax(area)
        max_roi = green_array[max_index, :].reshape([1, 4])
        depth_img_array = crop_depth(max_roi, self.depth_image)
        coordination = calculate_coordinate(depth_img_array)
        print(coordination)

        #publish
        coord_msg = Int32MultiArray()
        coord_msg.data = coordination
        self.Coord.publish(coord_msg)


    def RGB_callback(self, data):
        try:
            raw_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
        except CvBridgeError as e:
            print(e)

        # get detected image and an array of the coordination of the object
        max_color = -1
        max_roi = np.array([1, 4])
        detected_image, roi_array, color_count = detect_color(self.removeBG_image, 0.3)
        cv2.imshow('Detected image', detected_image)
        cv2.waitKey(1)

        if roi_array.shape[0] == 0: # Nothing detected
            print('Nothing')
            return 0


        self.stage_one = 1
        self.StageOne(self.stage_one, roi_array, color_count) # return the coordination and the color of the largest object
        #self.target_color = 2
        self.StageTwo(self.target_color, roi_array, color_count) # return the closest coordination of target color
        #self.stage_three = 1
        self.StageThree(self.stage_three, roi_array, color_count) # return the coordination of the largest green object

        #return 0

        

        # publish
        #msg_RGB = CvBridge().cv2_to_imgmsg(flipped_image)
        #self.Publisher_RGB.publish(msg_RGB)
        #self.Max_color.publish(max_color)
        #self.Max_coord.publish(max_roi)

    def Depth_callback(self, data):
        try:
            raw_image = CvBridge().imgmsg_to_cv2(data, "16UC1")
        except CvBridgeError as e:
            print(e)

        self.depth_image = raw_image.copy()

    def RemoveBG_callback(self, data):
        try:
            raw_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
        except CvBridgeError as e:
            print(e)

	self.removeBG_image = raw_image.copy()



if __name__ == '__main__':
    rospy.init_node("ImagePreprocess",anonymous=False)
    preprocess = Preprocess()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down...")
