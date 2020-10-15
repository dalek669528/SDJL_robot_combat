#!/usr/bin/env python

import cv2
import rospy
import numpy as np
import pyrealsense2 as rs
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import os
import shutil
import time


def make_folder(path_folder):
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)

def record_rgbd():
    #make_folder("../data/realsense/")

    pipeline = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_sensor.set_option(rs.option.visual_preset, 3)  # Set high accuracy for depth sensor
    depth_scale = depth_sensor.get_depth_scale()

    clipping_distance_in_meters = 1
    clipping_distance = clipping_distance_in_meters / depth_scale

    align_to = rs.stream.color
    align = rs.align(align_to)
    
    img_index = 0
    while(True):
      try:
          frames = pipeline.wait_for_frames()
          
          #print(frames)
          
          aligned_frames = align.process(frames)
          aligned_depth_frame = aligned_frames.get_depth_frame()
          color_frame = aligned_frames.get_color_frame()
  
          if not aligned_depth_frame or not color_frame:
              raise RuntimeError("Could not acquire depth or color frames.")
  
          depth_image = np.asanyarray(aligned_depth_frame.get_data())
          color_image = np.asanyarray(color_frame.get_data())
  
          grey_color = 0
          depth_image_3d = np.dstack((depth_image, depth_image, depth_image))  # Depth image is 1 channel, color is 3 channels
          
          print('clipping_distance : ', clipping_distance)
          
          bg_removed = np.where(
              (depth_image_3d > clipping_distance) | (depth_image_3d < 0),
              grey_color,
              color_image,
          )

          
          print('Max : ', np.max(depth_image))
          print('Min : ', np.min(depth_image))
          np.set_printoptions(threshold=np.inf)
          #print(depth_image[:100, :100])

	  cv2.circle(color_image, (320, 180), 10, (0,0,0), 8)
	  cv2.circle(color_image, (960, 180), 10, (0,0,0), 8)
	  cv2.circle(color_image, (320, 540), 10, (0,0,0), 8)
	  cv2.circle(color_image, (960, 540), 10, (0,0,0), 8)
          cv2.circle(color_image, (640, 540), 10, (0,0,0), 8)

      	  cv2.imshow('rgb', cv2.resize(color_image, (640, 360)))
      	  cv2.imshow('bg_removed', cv2.resize(bg_removed, (640, 360)))
      	  cv2.waitKey(1)
          
          root_path = '/home/dick/ros_test/catkin_ws/src/camera/data/realsense/for_test/points/'
          
          if not os.path.isdir(root_path):
            os.mkdir(root_path)
          
          #cv2.imwrite(root_path + str(img_index) +'_' + 'depth.png', depth_image)
          #cv2.imwrite(root_path + str(img_index) +'_' + 'rgb.png', color_image)
          #cv2.imwrite(root_path + str(img_index) +'_' + 'bg_removed.png', bg_removed)
          img_index += 1
      finally:
          print('keep')
          #time.sleep(0.5)
          #pipeline.stop()
          
    return color_image, depth_image


if __name__ == "__main__":
    print('here')
    record_rgbd()
