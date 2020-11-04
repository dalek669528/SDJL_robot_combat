#!/usr/bin/env python

import cv2
import rospy
import numpy as np
import pyrealsense2 as rs
import time
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Int32, Float32MultiArray, Int32MultiArray
from camera.msg import Coordination
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
        self.rgb_image = np.zeros((360, 640))
        self.depth_image = np.zeros((360, 640))
        self.removeBG_image = np.zeros((360, 640))
        self.stage_one = -1
        self.stage_three = -1
        self.target_color = -1
        self.time = time.time()
        self.depth_scale = 0.0010000000474974513
        # Subscribers
        self.RawRGB = rospy.Subscriber('RawRGB', Image, self.RGB_callback, queue_size=1)
        self.RawDepth = rospy.Subscriber('RawDepth', Image, self.Depth_callback, queue_size=1)
        self.RemoveBG = rospy.Subscriber('RemoveBG', Image, self.RemoveBG_callback, queue_size=1)

        # Publishers
        self.Color = rospy.Publisher('Color', Int32, queue_size=1) # publish max detected color
        self.Coord = rospy.Publisher('Coord', Coordination, queue_size=1) # publish coordination of max color
        #self.Publisher_RGB = rospy.Publisher('CropedRGB', Image, queue_size=1) # RGB publish
        #self.CroppedRBG = rospy.Publisher('CropedRGB', Image, queue_size=1) # Depth publish
        #self. = rospy.Publisher('', Image, queue_size=1) # Removed BG publish

    def get_filted_image(self, meter):
        clipping_distance = meter / self.depth_scale
        grey_color = 0
        depth_image_3d = np.dstack((self.depth_image, self.depth_image, self.depth_image))
        bg_removed_rgb = np.where(
            (depth_image_3d > clipping_distance) | (depth_image_3d <= 0),
            grey_color,
            self.rgb_image,
        )
        return bg_removed_rgb

    def StageOne(self, enable):
        meter = 1
        removeBG_image = self.get_filted_image(meter)
        detected_image, roi_array, color_count = detect_color(removeBG_image, 0.3)
        cv2.imshow('Detected image', detected_image)
        cv2.waitKey(1)
        if roi_array.shape[0] == 0: # Nothing detected
            print('Nothing')
            return 0
        t = time.time()
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
        print('2', time.time()-t)
        if max_index < color_count[0]:
            max_color = 0
        elif max_index < color_count[0] + color_count[1]:
            max_color = 1
        elif max_index < color_count.sum:
            max_color = 2
        print(max_color)

        max_roi = roi_array[max_index, :].reshape([1, 4])
        t = time.time()
        depth_img_array = crop_depth(max_roi, self.depth_image) # return detected array(x, y, depth)
        print('3', time.time()-t)
        t = time.time()
        coordination = calculate_coordinate(depth_img_array)
        print('4', time.time()-t)
        print(coordination) # array(x, y(depth), h)

        #publish
        color_msg = Int32()
        coord_msg = Coordination()
        color_msg.data = max_color
        coord_msg.data = coordination.flatten().tolist()
        self.Color.publish(color_msg)
        self.Coord.publish(coord_msg)

    def StageTwo(self, color):
        meter = 0.5
        removeBG_image = self.get_filted_image(meter)
        detected_image, roi_array, color_count = detect_color(removeBG_image, 0.3)
        if roi_array.shape[0] == 0: # Nothing detected
            print('Nothing')
            return 0
        #remember to filt if green or blue are not detected!!!
        if (color == 1)&(color_count[1] > 0):
            target_array = roi_array[color_count[0]:color_count[0]+color_count[1], :]
        elif (color == 2)&(color_count[2] > 0):
            target_array = roi_array[color_count[0]+color_count[1]:sum(color_count), :]
        else:
            return 0


        depth_img_array = crop_depth(target_array, self.depth_image)
        sorted_index = np.argsort(depth_img_array[:, 2])
        closest = depth_img_array[sorted_index[0], :].reshape([1, 3])
        coordination = calculate_coordinate(closest)
        print(coordination)

        #publish
        coord_msg = Coordination()
        coord_msg.data = coordination.flatten().tolist()
        self.Coord.publish(coord_msg)

    def StageThree(self, enable):
        meter = 0.5
        removeBG_image = self.get_filted_image(meter)
        detected_image, roi_array, color_count = detect_color(removeBG_image, 0.3)
        if roi_array.shape[0] == 0: # Nothing detected
            print('Nothing')
            return 0
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
        coord_msg = Coordination()
        coord_msg.data = coordination.flatten().tolist()
        self.Coord.publish(coord_msg)

    def RGB_callback(self, data):
        try:
            raw_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
        except CvBridgeError as e:
            print(e)
        self.rgb_image = raw_image.copy()

        # get detected image and an array of the coordination of the object
        
        self.time = time.time()        
        
        print('1', time.time()-self.time)

        self.stage_one = 1
        self.StageOne(self.stage_one) # return the coordination and the color of the largest object
        #self.target_color = 2
        self.StageTwo(self.target_color) # return the closest coordination of target color
        #self.stage_three = 1
        self.StageThree(self.stage_three) # return the coordination of the largest green object

        #return 0

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
