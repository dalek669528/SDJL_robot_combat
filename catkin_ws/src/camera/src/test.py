#!/usr/bin/env python

import cv2
import sys
import rospy
import numpy as np
import pyrealsense2 as rs
import time
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Int32, Float32MultiArray
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
        self.yolo_detect_finish_flag = False
        self.roi_info = []
        # Subscribers
        
        self.DetectResult = rospy.Subscriber('DetectResult', Float32MultiArray, self.Detect_callback, queue_size=1)
       
        # Publishers
        # self.Color = rospy.Publisher('Color', Int32, queue_size=1) # publish max detected color
        self.DetectImage = rospy.Publisher('DetectImage', Image, queue_size=1)
        time.sleep(1)
        self.StageOne_Yolo()

    def StageOne_Yolo(self):
        while(1):
            print('Publish to yolo')
            rgb_image = cv2.imread('43.png')
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

            temp = raw_input('INPUT (\'q\' to quit):')
            if(temp == "q"):
                break

        return detected_image, roi_array, color_count





    def Detect_callback(self, data):
        self.roi_info = np.array(data.data)
        print(self.roi_info)
        self.yolo_detect_finish_flag = True

   

if __name__ == '__main__':
    rospy.init_node("Test",anonymous=False)
    preprocess = Preprocess()
    
    preprocess.stage_index = 0
    #preprocess.detect_bounding_x1 = 100
    #preprocess.detect_bounding_x2 = 100
    #preprocess.detect_bounding_y1 = 0
    #preprocess.detect_bounding_y2 = 100
    preprocess.open_flag = 1