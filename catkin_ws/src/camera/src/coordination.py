#!/usr/bin/env python

import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image
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
    #result[0]: right, result[1]: down, result[2]: forward
    return result[2], -result[0], -result[1]

path = '../data/realsense/for_test/'
folder = 'points'
img = Image.open(path + folder + '/409_depth.png')
data = np.asarray(img)
#output = np.zeros([720, 1280, 3])
output = []

clipping_distance = 1000

for i in range(720):
    for j in range(1280):
        if  (data[i, j] < clipping_distance) | (data[i, j] <= 0):
          p1, p2, p3 = convert_depth_to_phys_coord_using_realsense(i, j, data[i, j])
          #output[i, j] = [p1, p2, p3]    
          output.append([p1, p2, p3])

output = np.array(output)

print(output.shape)

np.save('coordination', output)

scio.savemat('coordination.mat', {'output': output})
