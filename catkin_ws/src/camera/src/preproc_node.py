#!/usr/bin/env python

import cv2
import sys
import rospy
import numpy as np
import pyrealsense2 as rs
import time
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Int32
from camera.msg import Coordination, Master_info
from geometry_msgs.msg import Pose2D
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
        self.stage_index = -1
        self.t = time.time()
        self.depth_scale = 0.0010000000474974513
        self.seq_rgb = 0
        self.seq_depth = 0
        self.frame_loss = 1
        self.pos_x = 0
        self.right_bound = 120 #(mm)
        self.left_bound = -820 #(mm)
        self.detect_bounding_x1 = 0
        self.detect_bounding_x2 = 0
        self.detect_bounding_y1 = 0
        self.detect_bounding_y2 = 0
        self.open_flag = 0
        self.target_color = [0, 0, 0]
        # Subscribers
        self.master_info = rospy.Subscriber('master_info', Master_info, self.master_info_callback, queue_size=1)
        self.GetPos = rospy.Subscriber('position', Pose2D, self.GetPos_callback, queue_size=1)
        self.RawRGB = rospy.Subscriber('RawRGB', Image, self.RGB_callback, queue_size=1)
        self.RawDepth = rospy.Subscriber('RawDepth', Image, self.Depth_callback, queue_size=1)


        # Publishers
        # self.Color = rospy.Publisher('Color', Int32, queue_size=1) # publish max detected color
        self.Coord = rospy.Publisher('Coord', Coordination, queue_size=1) # publish coordination of max color
        
    def get_filted_image(self, meter, rgb_image, depth_image, image_type): # get distance-filted image type:rgb, depth
        clipping_distance = meter / self.depth_scale
        grey_color = 0
        if image_type == 'rgb': # rgb image
            depth = np.dstack((depth_image, depth_image, depth_image))
            image = rgb_image.copy()
        elif image_type == 'depth': # depth image
            depth = depth_image.copy()
            image = depth_image.copy()
        filted_image = np.where(
                (depth > clipping_distance) | (depth <= 0),
                grey_color,
                image,
            )
        return filted_image

    def StageOne(self, rgb_image, depth_image):
        # color_msg = Int32()
        coord_msg = Coordination()
        meter = 1
        detected_image, roi_array, color_count = detect_color(rgb_image, 0.3)
        #detected_image, roi_array, color_count = detect_color(removeBG_rgb, 0.3)
        removeBG_rgb = self.get_filted_image(meter, rgb_image, depth_image, 'rgb')
        # cv2.imshow('removeBG_rgb', removeBG_rgb)

        cv2.imshow('Detected image', detected_image)
        cv2.waitKey(1)
        if roi_array.shape[0] == 0: # Nothing detected
            print('First stage: Nothing detected.')
            coord_msg.data = [0, -1, 0]
            coord_msg.color = 'Nothing'
            self.Coord.publish(coord_msg)
            return 0

        # depth_image_array = crop_depth(roi_array, removeBG_depth)
        depth_image_array = crop_depth(roi_array, depth_image)
        coordination = calculate_coordinate(depth_image_array)

        # self.pos_x = 0
        bound_filter = ((coordination > (self.left_bound - self.pos_x)) & (coordination < (self.right_bound - self.pos_x)))[:,0]
        # print(coordination)
        # print('bound filter : ', bound_filter) 
        roi_array[np.logical_not(bound_filter), 0] = roi_array[np.logical_not(bound_filter), 2]
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
            max_color_string = 'red'
        elif max_index < color_count[0] + color_count[1]:
            max_color = 1
            max_color_string = 'green'
        elif max_index < color_count.sum:
            max_color = 2
            max_color_string = 'blue'

        #publish
        # color_msg.data = max_color
        coord_msg.data = coordination[max_index, :].flatten().tolist()
        coord_msg.color = max_color_string
        # self.Color.publish(color_msg)
        self.Coord.publish(coord_msg)
        
        # print(coordination)

    def StageTwo(self, rgb_image, depth_image):
        coord_msg = Coordination()
        meter = 0.5
        removeBG_rgb = self.get_filted_image(meter, rgb_image, depth_image, 'rgb')
        removeBG_depth = self.get_filted_image(meter, rgb_image, depth_image, 'depth')
        detected_image, roi_array, color_count = detect_color(removeBG_rgb, 0.3, red = False)
        # cv2.imshow('filted rgb', removeBG_rgb)
        cv2.imshow('detected', detected_image)
        cv2.waitKey(1)
        if roi_array.shape[0] == 0: # Nothing detected
            print('Second stage: Nothing detected.')
            coord_msg.data = [0, -1, 0]
            coord_msg.color = 'Nothing'
            self.Coord.publish(coord_msg)
            return 0
        #remember to filt if green or blue are not detected!!!
        if (color_count[1] > 0):
            target_array = roi_array[color_count[0]:color_count[0]+color_count[1], :]
            target_color_string = 'green'
        elif (color_count[2] > 0):
            target_array = roi_array[color_count[0]+color_count[1]:sum(color_count), :]
            target_color_string = 'blue'
        else:
            return 0

        depth_img_array = crop_depth(target_array, removeBG_depth)
        sorted_index = np.argsort(depth_img_array[:, 2])
        closest = depth_img_array[sorted_index[0], :].reshape([1, 3])
        coordination = calculate_coordinate(closest)
        print(coordination)

        #publish
        coord_msg = Coordination()
        coord_msg.data = coordination.flatten().tolist()
        coord_msg.color = target_color_string
        self.Coord.publish(coord_msg)

    def StageThree(self, rgb_image, depth_image):
        coord_msg = Coordination()
        meter = 0.5
        removeBG_rgb = self.get_filted_image(meter, rgb_image, depth_image, 'rgb')
        removeBG_depth = self.get_filted_image(meter, rgb_image, depth_image, 'depth')
        detected_image, roi_array, color_count = detect_color(removeBG_rgb, 0.3, red = False, blue=False)
        if color_count[1] == 0: # Green 'E' is not detected
            print('Third stage: Nothing detected.')
            coord_msg.data = [0, -1, 0]
            coord_msg.color = 'Nothing'
            self.Coord.publish(coord_msg)
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
        depth_img_array = crop_depth(max_roi, removeBG_depth)
        coordination = calculate_coordinate(depth_img_array)
        #print(coordination)

        #publish
        coord_msg = Coordination()
        coord_msg.data = coordination.flatten().tolist()
        self.Coord.publish(coord_msg)

    def RGB_callback(self, data):
        try:
            if not self.open_flag:
                return
            self.seq_rgb = data.header.seq
            #print('RGB_callback: %d' % (self.seq_rgb))
            if (self.seq_depth - self.seq_rgb) > self.frame_loss:
                # print('drop frame:', self.seq_rgb)
                return
            else:
                # print('seq: rgb/depth', self.seq_rgb, self.seq_depth)
                rgb_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
                depth_image = self.depth_image.copy()
        except CvBridgeError as e:
            print(e)
        #cv2.imwrite('b.jpg', rgb_image)
        # cv2.imshow('rgb', rgb_image)
        # cv2.waitKey(1)

        self.rgb_image = rgb_image.copy()

        # get detected image and an array of the coordination of the object
        
        # self.t = time.time()        
        
        #print('1', time.time()-self.time)
        rgb_image[:, 0:self.detect_bounding_x1] = [0, 0, 0]
        rgb_image[:, rgb_image.shape[1]-self.detect_bounding_x2:rgb_image.shape[1]] = [0, 0, 0]
        rgb_image[0:self.detect_bounding_y1, :] = [0, 0, 0]
        rgb_image[rgb_image.shape[0]-self.detect_bounding_y2:rgb_image.shape[0], :] = [0, 0, 0]
        # self.stage_index = 1
        if self.stage_index == 0:
            self.StageOne(rgb_image, depth_image) # return the coordination and the color of the largest object
        elif self.stage_index == 1:
            self.StageTwo(rgb_image, depth_image) # return the closest coordination of target color
        elif self.stage_index == 2:
            self.StageThree(rgb_image, depth_image) # return the coordination of the largest green object

        #return 0

    def Depth_callback(self, data):
        try:
            depth_image = CvBridge().imgmsg_to_cv2(data, "16UC1")
            self.seq_depth = data.header.seq
            #print('Depth_callback: %d' % (self.seq_depth))
            #print(sys.getsizeof(raw_image))
        except CvBridgeError as e:
            print(e)

        self.depth_image = depth_image.copy()

    def GetPos_callback(self, data):
        try:
            self.pos_x = data.x
        except:
            print("GetPos callback error")

    def master_info_callback(self, data):
        try:
            self.stage_index = data.stage
            self.detect_bounding_x1 = data.bounding[0]
            self.detect_bounding_x2 = data.bounding[1]
            self.detect_bounding_y1 = data.bounding[2]
            self.detect_bounding_y2 = data.bounding[3]
            self.open_flag = data.open_flag
            self.target_color = data.color
        except:
            print('Something wrong in Master_info Subscriber')

if __name__ == '__main__':
    rospy.init_node("ImagePreprocess",anonymous=False)
    preprocess = Preprocess()
    
    # preprocess.stage_index = 0
    # preprocess.detect_bounding_x1 = 100
    # preprocess.detect_bounding_x2 = 100
    # preprocess.detect_bounding_y1 = 0
    # preprocess.detect_bounding_y2 = 0
    # preprocess.open_flag = 1
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down...")