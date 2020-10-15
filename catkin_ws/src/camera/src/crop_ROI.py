#!/usr/bin/env python

import pyrealsense2 as rs
import numpy as np
import cv2


#return center point of the rectangle and its depth
def crop_depth(points, depth):
    #print(np.max(depth))
    #cv2.imwrite('crop_depth.png', depth)
    n = points.shape[0]
    output = np.zeros((n,3))
    for i in range(n):
        p = points[i]
        output[i][0] = int((p[2]+p[0])/2)
        output[i][1] = int((p[3]+p[1])/2)
        width = p[2] - p[0]
        height = p[3] - p[1]

        count = 0
        for j in range(p[1], p[3]+1):
            for k in range(p[0], p[2]+1):
                count += depth[j][k]
        #print(count, (width*height))
        output[i][2] = int(count/(width*height))
	#output[i][2] = depth[int(output[i][1])][int(output[i][0])]
    

    return output #n*3 array
