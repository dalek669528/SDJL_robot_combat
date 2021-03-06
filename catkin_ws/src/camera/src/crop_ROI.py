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

        temp = depth[p[1]:p[3]+1, p[0]:p[2]+1].copy()
        exist = (temp != 0)
        #num = temp.sum()
        den = exist.sum()
        #np.set_printoptions(threshold=np.nan)
        #print(temp)
        sort_array = np.sort(temp.flatten())
        caculate_array = sort_array[np.sum(sort_array==0) : np.sum(sort_array==0)+100]
        

        if den > 0:
            #output[i][2] = int(num/den)
            output[i][2] = caculate_array.mean()
        else:
            output[i][2] = 0
            
    return output #n*3 array
    
'''

  temp = depth[p[1]:p[3]+1, p[0]:p[2]+1].copy()
        exist = (temp != 0)
        num = temp.sum()
        den = exist.sum()
        
        if den > 0:
            output[i][2] = int(num/den)
        else:
            output[i][2] = 0


        count = 0
        depth_sum = 0
        for j in range(p[1], p[3]+1):
            for k in range(p[0], p[2]+1):
                if depth[j][k] != 0:
                    depth_sum += depth[j][k]
                    count += 1
        #print(count, (width*height))
        if count > 0:
            output[i][2] = int(depth_sum/count)
        else:
            output[i][2] = 0
	#output[i][2] = depth[int(output[i][1])][int(output[i][0])]
'''
