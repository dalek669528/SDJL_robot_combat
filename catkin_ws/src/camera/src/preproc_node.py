#!/usr/bin/env python

import cv2
import sys
import rospy
import numpy as np
import pyrealsense2 as rs
import time
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
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
        self.rgb_image = np.zeros((360, 640, 3), np.uint8)
        self.depth_image = np.zeros((360, 640, 1), np.uint16)
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
        self.yolo_detect_finish_flag = False
        self.roi_info = []
        # Subscribers
        self.master_info = rospy.Subscriber('master_info', Master_info, self.master_info_callback, queue_size=1)
        self.GetPos = rospy.Subscriber('car_pose', Pose2D, self.GetPos_callback, queue_size=1)
        self.RawRGB = rospy.Subscriber('RawRGB', Image, self.RGB_callback, queue_size=1)
        self.RawDepth = rospy.Subscriber('RawDepth', Image, self.Depth_callback, queue_size=1)
        self.DetectResult = rospy.Subscriber('DetectResult', Float32MultiArray, self.Detect_callback, queue_size=1)
       
        # Publishers
        # self.Color = rospy.Publisher('Color', Int32, queue_size=1) # publish max detected color
        self.Coord = rospy.Publisher('Coord', Coordination, queue_size=1) # publish coordination of max color
        self.DetectImage = rospy.Publisher('DetectImage', Image, queue_size=1)
        self.ResultImage = rospy.Publisher('ResultImage', Image, queue_size=1)

        self.processImage()
        
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

    def Yolo(self, rgb_image):
        print('Publish to yolo')
        msg_rgb_frame = CvBridge().cv2_to_imgmsg(rgb_image)
        self.DetectImage.publish(msg_rgb_frame)
        self.yolo_detect_finish_flag = False
        t = time.time()
        while self.yolo_detect_finish_flag == False:
            time.sleep(0.1)
            if((time.time()-t)>3):
            	print('wait too long')
            	break

        #print(self.roi_info)
        detected_image = rgb_image.copy()
        color_count = np.array([0,0,0])
        if len(self.roi_info) == 1 : 
            return detected_image, np.array([]), color_count

        roi_array = np.reshape(self.roi_info, (-1, 6))
 
        roi_array = np.sort(roi_array, axis=0)
        for roi in roi_array:
            calsses = int(roi[0])
            x1 = int(roi[2])
            y1 = int(roi[3])
            x2 = int(roi[4])
            y2 = int(roi[5])
            if calsses == 0:
                color = (0, 0, 255)
                color_string = 'Red'
            elif calsses == 1:
                color = (0, 255, 0)
                color_string = 'Green'
            elif calsses == 2:
                color = (255, 0, 0)
                color_string = 'Blue'
            color_count[calsses] += 1

            cv2.rectangle(detected_image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(detected_image, color_string, (x1, y1+14), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 1, cv2.LINE_AA)
        #print(color_count)
        roi_array = roi_array[:, 2:].astype(int)
        #print(roi_array)
        #cv2.imshow('Yolo', detected_image)
        #cv2.waitKey(1)

        return detected_image, roi_array, color_count

    def StageOne(self, rgb_image, depth_image):
        # color_msg = Int32()
        coord_msg = Coordination()
        meter = 1
        
        detected_image, roi_array, color_count = self.Yolo(rgb_image)
        self.ResultImage.publish(CvBridge().cv2_to_imgmsg(detected_image))

        #detected_image, roi_array, color_count = detect_color(rgb_image, 0.3)
        #detected_image, roi_array, color_count = detect_color(removeBG_rgb, 0.3)
        # removeBG_rgb = self.get_filted_image(meter, rgb_image, depth_image, 'rgb')
        cv2.imshow('Stage1', detected_image)
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
        print(coordination)
        # self.pos_x = 0
        bound_filter = ((coordination > (self.left_bound - self.pos_x)) & (coordination < (self.right_bound - self.pos_x)))[:,0]
        # print(coordination)
        print(bound_filter) 
        roi_array[np.logical_not(bound_filter), 0] = roi_array[np.logical_not(bound_filter), 2]
        x1 = roi_array[:, 0]
        y1 = roi_array[:, 1]
        x2 = roi_array[:, 2]
        y2 = roi_array[:, 3]
        w = x2 - x1
        h = y2 - y1
        area = w * h
        max_index = np.argmax(area)

        if area[max_index] == 0:
            print('First stage: Out of bound.')
            coord_msg.data = [0, -1, 0]
            coord_msg.color = 'Nothing'
            self.Coord.publish(coord_msg)
            return 0

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
        detected_image, roi_array, color_count = detect_color(1, removeBG_rgb, 0.3, red = False)
        #cv2.imshow('filted rgb', removeBG_rgb)
        cv2.imshow('Stage2', detected_image)
        cv2.waitKey(1)
        self.ResultImage.publish(CvBridge().cv2_to_imgmsg(detected_image))
        if roi_array.shape[0] == 0: # Nothing detected
            print('Second stage: Nothing detected.')
            coord_msg.data = [0, -1, 0]
            coord_msg.color = 'Nothing'
            self.Coord.publish(coord_msg)
            return 0
        #remember to filt if green or blue are not detected!!!
        
        # self.pos_x = 0
        depth_img_array = crop_depth(roi_array, depth_image)
        coordination = calculate_coordinate(depth_img_array)
        bound_filter = ((coordination > (self.left_bound - self.pos_x)) & (coordination < (self.right_bound - self.pos_x)))[:,0]
        roi_array[np.logical_not(bound_filter), 0] = roi_array[np.logical_not(bound_filter), 2]
        #print(coordination)
        print(bound_filter)
        #print(depth_img_array)
       
        for index, value in enumerate(roi_array):
        	if value[0] == value[2]:
        		depth_img_array[index, 2] = 10000
        index = np.argmin(depth_img_array[:, 2])
        #print(index, depth_img_array[index, 2])
        if depth_img_array[index, 2] == 10000:
            print('Second stage: Out of bound.')
            coord_msg.data = [0, -1, 0]
            coord_msg.color = 'Nothing'
            self.Coord.publish(coord_msg)
            return 0

        coordination = coordination[index, :]
        # sorted_index = np.argsort(depth_img_array[:, 2])
        # closest = depth_img_array[sorted_index[0], :].reshape([1, 3])
        # coordination = calculate_coordinate(closest)
        #print(coordination)





        #publish
        coord_msg = Coordination()
        coord_msg.data = coordination.flatten().tolist()
        coord_msg.color = 'green'
        self.Coord.publish(coord_msg)

    def StageThree(self, rgb_image, depth_image):
        coord_msg = Coordination()
        meter = 0.5
        removeBG_rgb = self.get_filted_image(meter, rgb_image, depth_image, 'rgb')
        removeBG_depth = self.get_filted_image(meter, rgb_image, depth_image, 'depth')
        # if self.stage_index == 30:

        detected_image, roi_array, color_count = detect_color(2, removeBG_rgb, 0.3, red = False, blue=False)
        self.ResultImage.publish(CvBridge().cv2_to_imgmsg(detected_image))
        cv2.imshow('Stage3', detected_image)
        cv2.waitKey(1)
        if color_count[1] == 0: # Green 'E' is not detected
            print('Third stage: Nothing detected.')
            coord_msg.data = [0, -1, 0]
            coord_msg.color = 'Nothing'
            self.Coord.publish(coord_msg)
            return 0
        
        # depth_image_array = crop_depth(roi_array, removeBG_depth)
        depth_image_array = crop_depth(roi_array, depth_image)
        coordination = calculate_coordinate(depth_image_array)

        # self.pos_x = 0
        bound_filter = ((coordination > (self.left_bound - self.pos_x)) & (coordination < (self.right_bound - self.pos_x)))[:,0]
        print(coordination)
        print(bound_filter) 
        roi_array[np.logical_not(bound_filter), 0] = roi_array[np.logical_not(bound_filter), 2]
        
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
        coordination = coordination[max_index]
        #print(coordination)
        #print(max_index)

        if area[max_index] == 0:
            print('Third stage: Out of bound.')
            coord_msg.data = [0, -1, 0]
            coord_msg.color = 'Nothing'
            self.Coord.publish(coord_msg)
            return 0

        #publish
        coord_msg = Coordination()
        coord_msg.data = coordination.flatten().tolist()
        self.Coord.publish(coord_msg)


    def processImage(self):
        process_index = -1
        while(not rospy.is_shutdown()):
            if process_index != self.seq_depth:
                #print(self.seq_depth, self.seq_rgb)
                process_index = self.seq_depth

                rgb_image = self.rgb_image.copy()
                depth_image = self.depth_image.copy()

                rgb_image[:, 0:self.detect_bounding_x1] = [0, 0, 0]
                rgb_image[:, rgb_image.shape[1]-self.detect_bounding_x2:rgb_image.shape[1]] = [0, 0, 0]
                rgb_image[0:self.detect_bounding_y1, :] = [0, 0, 0]
                rgb_image[rgb_image.shape[0]-self.detect_bounding_y2:rgb_image.shape[0], :] = [0, 0, 0]
                self.stage_index = 0
                if self.stage_index == 0:
                    self.StageOne(rgb_image, depth_image) # return the coordination and the color of the largest object
                elif self.stage_index == 1:
                    self.StageTwo(rgb_image, depth_image) # return the closest coordination of target color
                elif self.stage_index == 2:
                    self.StageThree(rgb_image, depth_image) # return the coordination of the largest green object

    def RGB_callback(self, data):
        try:
            # if not self.open_flag:
            #     return
            self.seq_rgb = data.header.seq
            #print('RGB_callback: %d' % (self.seq_rgb))
            self.rgb_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
                # print('seq: rgb/depth', self.seq_rgb, self.seq_depth)
   
        except CvBridgeError as e:
            print(e)
        # cv2.imwrite('b.jpg', rgb_image)
        # cv2.imshow('rgb', rgb_image)
        # cv2.waitKey(1)

        # get detected image and an array of the coordination of the object
        
        # self.t = time.time()        
        
        # print('1', time.time()-self.time)


       
        # return 0

    def Detect_callback(self, data):
        self.roi_info = np.array(data.data)
        #print(self.roi_info)
        self.yolo_detect_finish_flag = True

    def Depth_callback(self, data):
        try:
            self.seq_depth = data.header.seq
            self.depth_image = CvBridge().imgmsg_to_cv2(data, "16UC1")
           
        except CvBridgeError as e:
            print(e)

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
    
    #preprocess.stage_index = 0
    #preprocess.detect_bounding_x1 = 100
    #preprocess.detect_bounding_x2 = 100
    #preprocess.detect_bounding_y1 = 0
    #preprocess.detect_bounding_y2 = 100
    # preprocess.open_flag = 1
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down...")


'''
    def StageOne_Yolo(self, rgb_image):
        print('Publish to yolo')
        msg_rgb_frame = CvBridge().cv2_to_imgmsg(rgb_image)
        self.DetectImage.publish(msg_rgb_frame)
        self.yolo_detect_finish_flag = False

        while self.yolo_detect_finish_flag == False:
            time.sleep(0.1)
        print(self.roi_info, self.roi_info.shape)
        if len(self.roi_info) == 1 : 
            return

        roi_array = np.reshape(self.roi_info, (-1, 6))
        detected_image = rgb_image.copy()
        color_count = np.array([0,0,0])
        roi_array = np.sort(roi_array, axis=0)
        for roi in roi_array:
            calsses = int(roi[0])
            x1 = int(roi[2])
            y1 = int(roi[3])
            x2 = int(roi[4])
            y2 = int(roi[5])
            if calsses == 0:
                color = (0, 0, 255)
                color_string = 'Red'
            elif calsses == 1:
                color = (0, 255, 0)
                color_string = 'Green'
            elif calsses == 2:
                color = (255, 0, 0)
                color_string = 'Blue'
            color_count[calsses] += 1

            cv2.rectangle(detected_image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(detected_image, color_string, (x1, y1+14), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 1, cv2.LINE_AA)
        print(color_count)
        roi_array = roi_array[:, 2:]
        print(roi_array)
        cv2.imshow('Yolo', detected_image)
        cv2.waitKey(1)

        return detected_image, roi_array, color_count
'''
