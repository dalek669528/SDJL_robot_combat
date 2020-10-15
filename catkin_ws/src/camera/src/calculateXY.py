#!/usr/bin/env python

import pyrealsense2 as rs
import numpy as np
import rospy
import cv2
import scipy.io as scio

def convert_depth_to_phys_coord_using_realsense(x, y, depth):
    _intrinsics = rs.intrinsics()
    _intrinsics.width = 1920           #cameraInfo.width
    _intrinsics.height = 1080          #cameraInfo.height
    _intrinsics.ppx = 654.888000488281 #cameraInfo.K[2]
    _intrinsics.ppy = 368.117980957031 #cameraInfo.K[5]
    _intrinsics.fx = 912.651000976562  #cameraInfo.K[0]
    _intrinsics.fy = 911.876037597656  #cameraInfo.K[4]
    #_intrinsics.model = cameraInfo.distortion_model
    _intrinsics.model  = rs.distortion.inverse_brown_conrady
    _intrinsics.coeffs = [0, 0, 0, 0, 0] #[i for i in cameraInfo.D]
    result = rs.rs2_deproject_pixel_to_point(_intrinsics, [x, y], depth)
    #result[0]: up and down, result[1]: left and right, result[2]: forward and back
    #return result[2], -result[0], -result[1]
    return -result[1], -result[0], result[2]


def calculate_coordinate(depth_img_list):
	CAMERAS_OFFSET    = -35
	RGB_CAMERA_OFFSET = 148	
	output_list = []
	for i in range(len(depth_img_list)):
		#input argument : y(h), x(w), depth
		w, h, depth = convert_depth_to_phys_coord_using_realsense(depth_img_list[i][1], depth_img_list[i][0], depth_img_list[i][2])  
		x = w + CAMERAS_OFFSET + RGB_CAMERA_OFFSET
		output_list.append([x, depth, h])
	return np.array(output_list)
