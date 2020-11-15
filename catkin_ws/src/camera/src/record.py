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
    width = 640
    height = 360
    pipeline = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 15)
    config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, 15)

    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_sensor.set_option(rs.option.visual_preset, 3)  # Set high accuracy for depth sensor
    # depth_scale = depth_sensor.get_depth_scale()

    # clipping_distance_in_meters = 2
    # clipping_distance = clipping_distance_in_meters / depth_scale

    align_to = rs.stream.color
    align = rs.align(align_to)
    
    img_index = 0
    root_path = '/home/dick/SDJL_robot_combat/catkin_ws/src/camera/data/realsense/training_data/'
    color = 'blue/back/'
    print('PATH: ' + root_path + color)
    while(True):
      try:
          frames = pipeline.wait_for_frames()
          # zero_count = 0
          # depth_sum = 0
          #print(frames)
          
          aligned_frames = align.process(frames)
          aligned_depth_frame = aligned_frames.get_depth_frame()
          color_frame = aligned_frames.get_color_frame()
  
          if not aligned_depth_frame or not color_frame:
              raise RuntimeError("Could not acquire depth or color frames.")
  
          depth_image = np.asanyarray(aligned_depth_frame.get_data())
          color_image = np.asanyarray(color_frame.get_data())
          rgb_image = cv2.flip(color_image, -1)
          cv2.imshow('rgb', rgb_image)
          cv2.waitKey(1)
          if not os.path.isdir(root_path+color):
            print('Create path: ' + root_path + color)
            # os.mkdir(root_path+color)
            make_folder(root_path + color)
            print('Success')

          cv2.imwrite(root_path + color + str(img_index) + '.png', rgb_image)
          # cv2.imwrite(str(img_index) + '.png', rgb_image)
          print(root_path + color + str(img_index) + '.png')
          img_index += 1
          time.sleep(1)
          # grey_color = 0
          # depth_image_3d = np.dstack((depth_image, depth_image, depth_image))  # Depth image is 1 channel, color is 3 channels
          
          #print('clipping_distance : ', clipping_distance)
          
          # bg_removed = np.where(
          #     (depth_image_3d > clipping_distance) | (depth_image_3d <= 0),
          #     grey_color,
          #     color_image,
          # )

          
          #print('Max : ', np.max(depth_image))
          #print('Min : ', np.min(depth_image))
          # np.set_printoptions(threshold=np.inf)
          #print(depth_image[:100, :100])

	  #cv2.circle(color_image, (320, 180), 10, (0,0,0), 8)
	  #cv2.circle(color_image, (960, 180), 10, (0,0,0), 8)
	  #cv2.circle(color_image, (320, 540), 10, (0,0,0), 8)
	  #cv2.circle(color_image, (960, 540), 10, (0,0,0), 8)
          #cv2.circle(color_image, (640, 540), 10, (0,0,0), 8)
          # cv2.rectangle(color_image, (width/4, height/4), (width/4*3, height/4*3), (0, 0, 0), 5)
          # depth_array = depth_image[width/4:width/4*3, height/4:height/4*3]
          #print(depth_image.shape)
          #for i in range(depth_array.shape[0]):
          #    for j in range(depth_array.shape[1]):
          #        if depth_array[i][j] == 0:
          #            zero_count += 1
          #        else:
          #            depth_sum += depth_array[i][j]

          # print(depth_sum/depth_array.shape[0]/depth_array.shape[1])
          #if zero_count > depth_array.shape[0]*depth_array.shape[1]*0.2:
          #    print('CAN NOT DETECT!!!')

      	  # cv2.imshow('rgb', cv2.resize(color_image, (640, 360)))
      	  # cv2.imshow('bg_removed', cv2.resize(bg_removed, (640, 360)))
      	  # cv2.waitKey(1)
          
          
          
          # if not os.path.isdir(root_path):
          #   os.mkdir(root_path)
          
          #cv2.imwrite(root_path + str(img_index) +'_' + 'depth.png', depth_image)
          #cv2.imwrite(root_path + str(img_index) +'_' + 'rgb.png', color_image)
          #cv2.imwrite(root_path + str(img_index) +'_' + 'bg_removed.png', bg_removed)
          # img_index += 1
      except OSError as e:
          print(e)
          #time.sleep(0.5)
          #pipeline.stop()
          
    # return color_image, depth_image


if __name__ == "__main__":
    #print('here')
    record_rgbd()
