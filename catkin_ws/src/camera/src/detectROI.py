import cv2
import numpy as np
from boundingbox_suppression import non_max_suppression_slow

def getRed(img):
	lower_bound_0 = np.array([0, 100, 230]) 
	upper_bound_0 = np.array([10, 255, 255])
	lower_bound_1 = np.array([170, 100, 50]) 
	upper_bound_1 = np.array([180, 255, 255])
	hsv_img   = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask_0 = cv2.inRange(hsv_img, lower_bound_0, upper_bound_0)
	mask_1 = cv2.inRange(hsv_img, lower_bound_1, upper_bound_1)
	mask  = cv2.bitwise_or(mask_0, mask_1)
	return mask

def getGreen(img):
	lower_bound_0 = np.array([65,60,60]) 
	upper_bound_0 = np.array([85,255,255])
	hsv_img   = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv_img, lower_bound_0, upper_bound_0)
	return mask

def getBlue(img):
	lower_bound_0 = np.array([70,60,20]) 
	upper_bound_0 = np.array([140,255,255])
	hsv_img   = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv_img, lower_bound_0, upper_bound_0)
	return mask


def detect_color(img, threshold):
	canvas = img.copy()
	#print(canvas.shape)
	dim = canvas.shape

	red_mask   = getRed(canvas)
	contours_red, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	green_mask = getGreen(canvas)
	contours_green, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        blue_mask = getBlue(canvas)
	contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	roi_list = []
        red_boxes = np.zeros([np.size(contours_red), 4])
        blue_boxes = np.zeros([np.size(contours_blue), 4])
        green_boxes = np.zeros([np.size(contours_green), 4])
        red_count = 0
        green_count = 0
        blue_count = 0

	for ind, cnt in enumerate(contours_red):
	        x, y, w, h = cv2.boundingRect(cnt)
                if(((w * h) > 500*4) & ((w * h) < 57600)):
                    red_boxes[ind, :] = [x, y, x+w, y+h]
        
        red_picks = non_max_suppression_slow(red_boxes, threshold)
        for (startX, startY, endX, endY) in red_picks:
                w = int(endX-startX)
                h = int(endY-startY)
                x = int(startX)
                y = int(startY)

		if(((w * h) > 500*4) & ((w * h) < 57600)):
		#if((w * h) > 500*4):
                        red_count += 1
			x1 = x - 10 if (x - 10) > 0 else 0
			y1 = y - 10 if (y - 10) > 0 else 0
			x2 = x+w+10 if (x+w+10) < dim[1] else dim[1]-1
			y2 = y+h+10 if (y+h+10) < dim[0] else dim[0]-1
                        cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 0, 255), 2)
			roi_list.append((x1, y1, x2, y2))
			cv2.putText(canvas, 'Red', (x1, y1+14), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

	for ind, cnt in enumerate(contours_green):
		x, y, w, h = cv2.boundingRect(cnt)
                green_boxes[ind, :] = [x, y, x+w, y+h]

        green_picks = non_max_suppression_slow(green_boxes, threshold)
        for (startX, startY, endX, endY) in green_picks:
                w = int(endX-startX)
                h = int(endY-startY)
                x = int(startX)
                y = int(startY)

                if(((w * h) > 500*4) & ((w * h) < 57600)):
		#if((w * h) > 500*4):
                        green_count += 1
			x1 = x - 10 if (x - 10) > 0 else 0
			y1 = y - 10 if (y - 10) > 0 else 0
			x2 = x+w+10 if (x+w+10) < dim[1] else dim[1]-1
			y2 = y+h+10 if (y+h+10) < dim[0] else dim[0]-1
			cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 255, 0), 2)
			roi_list.append((x1, y1, x2, y2))
			cv2.putText(canvas, 'Green', (x1, y1+14), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        for ind, cnt in enumerate(contours_blue):
		x, y, w, h = cv2.boundingRect(cnt)
                blue_boxes[ind, :] = [x, y, x+w, y+h]

        blue_picks = non_max_suppression_slow(blue_boxes, threshold)
        for (startX, startY, endX, endY) in blue_picks:
                w = int(endX-startX)
                h = int(endY-startY)
                x = int(startX)
                y = int(startY)

                if(((w * h) > 500*4) & ((w * h) < 57600)):
                        blue_count += 1
			x1 = x - 10 if (x - 10) > 0 else 0
			y1 = y - 10 if (y - 10) > 0 else 0
			x2 = x+w+10 if (x+w+10) < dim[1] else dim[1]-1
			y2 = y+h+10 if (y+h+10) < dim[0] else dim[0]-1
                        cv2.rectangle(canvas, (x1, y1), (x2, y2), (255, 0, 0), 2)
			roi_list.append((x1, y1, x2, y2))
			cv2.putText(canvas, 'Blue', (x1, y1+14), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

	return canvas, np.array(roi_list), np.array([red_count, green_count, blue_count])
