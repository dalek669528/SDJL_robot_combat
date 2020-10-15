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
		self.depth_image = np.zeros((720, 1280))
		# Publications
	   
		# Subscriptions
			
		self.CameraRgbImage     = rospy.Subscriber('CameraRgbImage',   Image, self.CameraRgb_callback,   queue_size=1)
		self.BgRemovedImage     = rospy.Subscriber('BgRemovedImage',   Image, self.BgRemoved_callback,   queue_size=1)
		self.CameraDepthImage   = rospy.Subscriber('CameraDepthImage', Image, self.CameraDepth_callback, queue_size=1)

 	def CameraRgb_callback(self, data):
		try:
		  cv_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
		except CvBridgeError as e:
		  print(e)
		cv2.imwrite('test_rgb.png', cv_image)
		print('Receive rgb!')

	def BgRemoved_callback(self, data):
	  
		try:
		  cv_image = CvBridge().imgmsg_to_cv2(data, "8UC3")
		except CvBridgeError as e:
		  print(e)
		
		cv2.imwrite('test.png', cv_image)
		print('Receive BgR!')
		
		#frame_resize = cv2.resize(cv_image, (640, 360))
		imgs, roi_array = detect_color(cv_image)
		cv2.imwrite('test_process.png', imgs)
		print(roi_array.shape)
		print(roi_array)

		#depth_image    = cv2.imread('test_depth.png')
		depth_img_array = crop_depth(roi_array, self.depth_image)

		print(depth_img_array)

		coordinate_array = calculate_coordinate(depth_img_array) 
		print(coordinate_array)

		cv2.waitKey(0)

    
 	def CameraDepth_callback(self, data):
		try:
			cv_image = CvBridge().imgmsg_to_cv2(data, "16UC1")
			self.depth_image = cv_image.copy()
		except CvBridgeError as e:
			print(e)
		cv2.imwrite('test_depth.png', cv_image)
		print('Receive depth!')
              
if __name__ == '__main__':
	rospy.init_node("processImage",anonymous=False)
	detect_roi = detectROI()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
