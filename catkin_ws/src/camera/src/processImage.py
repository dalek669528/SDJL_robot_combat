#!/usr/bin/env python

import cv2
import rospy
import numpy as np
import pyrealsense2 as rs
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import os
import shutil
from detectROI import*
from crop_ROI  import*
from calculateXY import *

class detectROI(object):
 	def __init__(self):
		self.node_name = rospy.get_name()
		rospy.loginfo("[%s] Initializing " %(self.node_name))
		self.depth_image = np.zeros((360, 640))
		# Publications
	   
		# Subscriptions
			
		self.CameraRgbImage     = rospy.Subscriber('CameraRgbImage',   Image, self.CameraRgb_callback,   queue_size=1)
		self.BgRemovedImage     = rospy.Subscriber('BgRemovedImage',   Image, self.BgRemoved_callback,   queue_size=1)
		self.CameraDepthImage   = rospy.Subscriber('CameraDepthImage', Image, self.CameraDepth_callback, queue_size=1)

 	def CameraRgb_callback(self, data):
		try:
		  self.cv_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
		except CvBridgeError as e:
		  print(e)
		
		print('Receive rgb!')

	def BgRemoved_callback(self, data):
	  
		try:
		  raw_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
		except CvBridgeError as e:
		  print(e)
		print('Receive BgR!')
		
                flipped_image = cv2.flip(raw_image, -1)
                
                # detect image
                #imgs, roi_array = detect_color(flipped_image)
                imgs, roi_array = detect_color(self.cv_image)
		print(roi_array.shape)

                cv2.imshow('detect image', imgs)

                # process image
		depth_img_array = crop_depth(roi_array, self.depth_image)
		#print(depth_img_array)
		coordinate_array = calculate_coordinate(depth_img_array) 
		#print(coordinate_array)

		cv2.waitKey(1)

    
 	def CameraDepth_callback(self, data):
		try:
			cv_image = CvBridge().imgmsg_to_cv2(data, "16UC1")
			self.depth_image = cv_image.copy()
		except CvBridgeError as e:
			print(e)
		print('Receive depth!')
              
if __name__ == '__main__':
	rospy.init_node("processImage",anonymous=False)
	detect_roi = detectROI()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
