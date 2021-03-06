#!/usr/bin/env python

import cv2
import rospy
import numpy as np
import time
import pyrealsense2 as rs
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import os
import shutil

class Camera(object):
  def __init__(self):
    self.node_name = rospy.get_name()
    rospy.loginfo("[%s] Initializing " %(self.node_name))
    self.image_width  = 640
    self.image_height = 360
    self.fps = 15
    self.pipeline     = rs.pipeline()
    
    self.config = rs.config()
    self.config.enable_stream(rs.stream.depth, self.image_width, self.image_height, rs.format.z16, self.fps)
    self.config.enable_stream(rs.stream.color, self.image_width, self.image_height, rs.format.bgr8, self.fps)
    
    self.profile =  self.pipeline.start(self.config)
    
    self.depth_sensor = self.profile.get_device().first_depth_sensor()
    self.depth_sensor.set_option(rs.option.visual_preset, 3)  # Set high accuracy for depth sensor
    #self.depth_scale = self.depth_sensor.get_depth_scale()
    
    self.align_to = rs.stream.color
    self.align = rs.align(self.align_to)
    
    # Publications
    self.CameraRgbImage = rospy.Publisher('RawRGB', Image, queue_size=1)
    self.CameraDepthImage = rospy.Publisher('RawDepth', Image, queue_size=1)
    
    # Subscriptions
    
    self.publishImage()
   
  def publishImage(self):
    time_count = 1
    # path = '/home/dick/SDJL_robot_combat/catkin_ws/src/camera/data/realsense/videos_frames/'
    # folder = 'stage1-4/'
    # frame_index = 0
    # if not os.path.exists(path+folder):
    #     os.makedirs(path+folder)
    # file_name = '00'
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # output = cv2.VideoWriter(path+folder+file_name+'.avi', fourcc, 3.0, (self.image_width, self.image_height))
    while(not rospy.is_shutdown()):
      try:
        frames =  self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        
        if not aligned_depth_frame or not color_frame:
          raise RuntimeError("Could not acquire depth or color frames.")

        if time_count%5 == 0:
            time_count = 1
        else:
            time_count += 1
            continue
        
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        flipped_rgb = cv2.flip(color_image, -1)
        flipped_depth = cv2.flip(depth_image, -1)

        # output.write(flipped_rgb)
        # # record the video(by save image)
        # cv2.imwrite(path + folder + str(frame_index) + '.png', flipped_rgb)
        # frame_index += 1
        # cv2.imshow('rgb', flipped_rgb)
        # cv2.waitKey(1)

        rospy.loginfo('Publish image.')
        msg_rgb_frame          = CvBridge().cv2_to_imgmsg(flipped_rgb)
        msg_depth_frame        = CvBridge().cv2_to_imgmsg(flipped_depth)        

        self.CameraRgbImage.publish(msg_rgb_frame)
        self.CameraDepthImage.publish(msg_depth_frame)

        #removeBG_rgb = self.get_filted_image(0.5, flipped_rgb, flipped_depth, 'rgb')
        #cv2.imshow('removeBG_rgb', removeBG_rgb)
        #cv2.waitKey(1)
        print('RGB seq: %d' % (msg_rgb_frame.header.seq))
        print('Depth seq: %d' % (msg_depth_frame.header.seq))
        
      except KeyboardInterrupt:
        # output.release()
        time.sleep(1)
        print("Shutting Down...")
    # output.release()

  def get_filted_image(self, meter, rgb_image, depth_image, image_type): # get distance-filted image type:rgb, depth
    clipping_distance = meter / 0.0010000000474974513
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



if __name__ == '__main__':
  rospy.init_node("CameraImagePublisher", anonymous=False)
  camera = Camera()