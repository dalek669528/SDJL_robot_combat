#!/usr/bin/env python

import pyrealsense2 as rs
import numpy as np
import cv2
from crop_ROI import *
from detectROI import *
from calculateXY import *

pipeline = rs.pipeline()

config = rs.config()
#config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
#config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 360, rs.format.z16, 15)
config.enable_stream(rs.stream.color, 640, 360, rs.format.bgr8, 15)

profile = pipeline.start(config)

depth_sensor = profile.get_device().first_depth_sensor()
depth_sensor.set_option(rs.option.visual_preset, 3)
depth_scale = depth_sensor.get_depth_scale()

clipping_distance_in_meters = 1
clipping_distance = clipping_distance_in_meters / depth_scale

align_to = rs.stream.color
align = rs.align(align_to)

img_index = 0

while(True):
    try:
        frames = pipeline.wait_for_frames()

        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not aligned_depth_frame or not color_frame:
              raise RuntimeError("Could not acquire depth or color frames.")

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        detected_image, roi_array = detect_color(color_image)
        crop_depth_array = crop_depth(roi_array, depth_image)
        coordinate_array = calculate_coordinate(crop_depth_array)
        
        if coordinate_array.size != 0:
            x_array = coordinate_array[:, 0]
            sorted_array = np.sort(x_array)
            print(coordinate_array)
            print('plus RGB_CAMERA_OFFSET in calculate.py(left to right):')
            print(sorted_array)

        height = color_image.shape[0]
        width = color_image.shape[1]
        #print(color_image.shape[0],color_image.shape[1])
        #print(depth_image.shape[0],depth_image.shape[1])
        #cv2.circle(color_image, (320, 180), 10, (0,0,0), 10)
        #cv2.circle(color_image, (960, 180), 10, (0,0,0), 10)
        #cv2.circle(color_image, (320, 540), 10, (0,0,0), 10)
        #cv2.circle(color_image, (960, 540), 10, (0,0,0), 10)
        #cv2.circle(color_image, (640, 540), 10, (0,0,0), 10)
        cv2.line(detected_image, (width/2, 0), (width/2, height), (0, 0, 0), 5)

        
        cv2.imshow('RGB_imgage', detected_image)
        cv2.waitKey(1)

        img_index += 1

    finally:
        print('keep')
