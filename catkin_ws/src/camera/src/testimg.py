#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from detectROI import detect_color

img = cv2.imread('/home/dick/ros_test/catkin_ws/src/camera/data/realsense/for_test/points/31_rgb.png')
ori = img.copy()
detected_img, roi_array = detect_color(ori, 0.1)
cv2.imshow('ori', img)
cv2.imshow('detected', detected_img)
cv2.imwrite('01-2.png', detected_img)
cv2.waitKey(0)
