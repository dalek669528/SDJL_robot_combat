import cv2
import time
import numpy as np
from boundingbox_suppression import non_max_suppression_slow

def getRed(img):
	lower_bound_0 = np.array([0, 120, 50]) 
	upper_bound_0 = np.array([20, 255, 255])
	lower_bound_1 = np.array([160, 120, 50]) 
	upper_bound_1 = np.array([180, 255, 255])
	hsv_img   = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask_0 = cv2.inRange(hsv_img, lower_bound_0, upper_bound_0)
	mask_1 = cv2.inRange(hsv_img, lower_bound_1, upper_bound_1)
	mask  = cv2.bitwise_or(mask_0, mask_1)
	# cv2.imshow('red', img[:, :, 2])
	# cv2.waitKey(1)
	return mask

def getRed_rgb(img):
	(B,G,R) = cv2.split(img)
	ratio_GtoRB = (R/3.0)/((R/3.0)+(G/3.0)+(B/3.0)+1)
	mask = cv2.threshold(ratio_GtoRB, 0.4, 255, cv2.THRESH_BINARY)[1]
	return mask

def getGreen(img):
	lower_bound_0 = np.array([65,60,80]) 
	upper_bound_0 = np.array([90,255,255])
	hsv_img   = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv_img, lower_bound_0, upper_bound_0)
	# cv2.imshow('green', img[:, :, 1])
	# cv2.waitKey(1)
	return mask

def getGreen_rgb(img):
	(B,G,R) = cv2.split(img)
	ratio_GtoRB = (G/3.0)/((R/3.0)+(G/3.0)+(B/3.0)+1)
	mask = cv2.threshold(ratio_GtoRB, 0.4, 255, cv2.THRESH_BINARY)[1]
	return mask

def getBlue(img):
	lower_bound_0 = np.array([90,60,20]) 
	upper_bound_0 = np.array([140,255,255])
	hsv_img   = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv_img, lower_bound_0, upper_bound_0)
	# cv2.imshow('blue', mask)
	# cv2.waitKey(1)

	return mask

def getBlue_box(img):
	lower_bound_0 = np.array([70,60,20]) 
	upper_bound_0 = np.array([160,255,255])
	hsv_img   = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv_img, lower_bound_0, upper_bound_0)
	# cv2.imshow('blue1', mask)
	# cv2.waitKey(1)

	return mask

def getBlue_rgb(img):
	(B,G,R) = cv2.split(img)
	ratio_GtoRB = (B/3.0)/((R/3.0)+(G/3.0)+(B/3.0)+1)
	mask = cv2.threshold(ratio_GtoRB, 0.4, 255, cv2.THRESH_BINARY)[1]
	return mask

def process_contours(color_string, contours, threshold, canvas, roi_list):
	if color_string == 'Red':
		color = (0, 0, 255)
	elif color_string == 'Green':
		color = (0, 255, 0)
	elif color_string == 'Blue':
		color = (255, 0, 0)

	boxes = []
	count = 0
	dim = canvas.shape
	for ind, cnt in enumerate(contours):
		x, y, w, h = cv2.boundingRect(cnt)
		if(((w * h) > 500*2) & ((w * h) < 60000)):
			boxes.append([x, y, x+w, y+h])
	boxes = np.array(boxes)
	picks = non_max_suppression_slow(boxes, threshold) if len(boxes) > 1 else boxes
	for (startX, startY, endX, endY) in picks:
		w = int(endX-startX)
		h = int(endY-startY)
		x = int(startX)
		y = int(startY)

		if(((w * h) > 500*2) & ((w * h) < 60000)):
			count += 1
			x1 = x - 10 if (x - 10) > 0 else 0
			y1 = y - 10 if (y - 10) > 0 else 0
			x2 = x+w+10 if (x+w+10) < dim[1] else dim[1]-1
			y2 = y+h+10 if (y+h+10) < dim[0] else dim[0]-1
			cv2.rectangle(canvas, (x1, y1), (x2, y2), color, 2)
			roi_list.append((x1, y1, x2, y2))
			cv2.putText(canvas, color_string, (x1, y1+14), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 1, cv2.LINE_AA)

	return canvas, roi_list, count

def detect_color(stage, img, threshold, red=True, green=True, blue=True):
	canvas = img.copy()
	red_count = 0
	green_count = 0
	blue_count = 0
	roi_list = []
	#print(time.time())
	# t = time.time()
	# red_mask   = getRed(canvas)
	#print(red_mask.shape)
	#resize_ratio = 0.5
	#resize_red_mask = cv2.resize(red_mask, (int(red_mask.shape[1]*resize_ratio), int(red_mask.shape[0]*resize_ratio)))
	#cv2.imshow('temp', resize_red_mask)
	#cv2.waitKey(1)
	
	if red:
		red_mask   = getRed(canvas)
		contours_red, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		canvas, roi_list, red_count = process_contours('Red', contours_red, threshold, canvas, roi_list)
	if green:
		green_mask = getGreen_rgb(canvas).astype(np.uint8)
		contours_green, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		canvas, roi_list, green_count = process_contours('Green', contours_green, threshold, canvas, roi_list)
	if blue:
		if stage == 1:
			blue_mask = getBlue_box(canvas)
		else:
			blue_mask = getBlue(canvas)
		contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		canvas, roi_list, blue_count = process_contours('Blue', contours_blue, threshold, canvas, roi_list)

	return canvas, np.array(roi_list), np.array([red_count, green_count, blue_count])

	# for ind, cnt in enumerate(contours_red):
	# 	x, y, w, h = cv2.boundingRect(cnt)
	# 	if(((w * h) > 500*4) & ((w * h) < 57600)):
	# 		#red_boxes[ind, :] = [x, y, x+w, y+h]
	# 		red_boxes.append([x, y, x+w, y+h])
	# red_boxes = np.array(red_boxes)


	# # print('r10', time.time()-t)
	# # t = time.time()


	# red_picks = non_max_suppression_slow(red_boxes, threshold) if len(red_boxes) > 1 else red_boxes
	# # print('r11', time.time()-t)
	# # t = time.time()
	# for (startX, startY, endX, endY) in red_picks:
	# 	w = int(endX-startX)
	# 	h = int(endY-startY)
	# 	x = int(startX)
	# 	y = int(startY)

	# 	if(((w * h) > 500*4) & ((w * h) < 57600)):
	# 	#if((w * h) > 500*4):
	# 		red_count += 1
	# 		x1 = x - 10 if (x - 10) > 0 else 0
	# 		y1 = y - 10 if (y - 10) > 0 else 0
	# 		x2 = x+w+10 if (x+w+10) < dim[1] else dim[1]-1
	# 		y2 = y+h+10 if (y+h+10) < dim[0] else dim[0]-1
	# 		cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 0, 255), 2)
	# 		roi_list.append((x1, y1, x2, y2))
	# 		cv2.putText(canvas, 'Red', (x1, y1+14), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

	# # print('r12', time.time()-t)
	# # t = time.time()


	# for ind, cnt in enumerate(contours_green):
	# 	x, y, w, h = cv2.boundingRect(cnt)
	# 	if(((w * h) > 500*4) & ((w * h) < 57600)):
	# 		#green_boxes[ind, :] = [x, y, x+w, y+h]
	# 		green_boxes.append([x, y, x+w, y+h])
	# green_boxes = np.array(green_boxes)
	# # print('g10', time.time()-t)
	# # t = time.time()

	# green_picks = non_max_suppression_slow(green_boxes, threshold) if len(green_boxes) > 1 else green_boxes

	# # print('g11', time.time()-t)
	# # t = time.time()

	# for (startX, startY, endX, endY) in green_picks:
	# 	w = int(endX-startX)
	# 	h = int(endY-startY)
	# 	x = int(startX)
	# 	y = int(startY)

	# 	if(((w * h) > 500*4) & ((w * h) < 57600)):
	# 	#if((w * h) > 500*4):
	# 		green_count += 1
	# 		x1 = x - 10 if (x - 10) > 0 else 0
	# 		y1 = y - 10 if (y - 10) > 0 else 0
	# 		x2 = x+w+10 if (x+w+10) < dim[1] else dim[1]-1
	# 		y2 = y+h+10 if (y+h+10) < dim[0] else dim[0]-1
	# 		cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 255, 0), 2)
	# 		roi_list.append((x1, y1, x2, y2))
	# 		cv2.putText(canvas, 'Green', (x1, y1+14), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)


	# # print('g12', time.time()-t)
	# # t = time.time()


	# for ind, cnt in enumerate(contours_blue):
	# 	x, y, w, h = cv2.boundingRect(cnt)
	# 	if(((w * h) > 500*4) & ((w * h) < 57600)):
	# 		#blue_boxes[ind, :] = [x, y, x+w, y+h]
	# 		blue_boxes.append([x, y, x+w, y+h])
	# blue_boxes = np.array(blue_boxes)

	# # print('b10', time.time()-t)
	# # t = time.time()

	# blue_picks = non_max_suppression_slow(blue_boxes, threshold) if len(blue_boxes) > 1 else blue_boxes
	# # print('b11', time.time()-t)
	# # t = time.time()

	# for (startX, startY, endX, endY) in blue_picks:
	# 	w = int(endX-startX)
	# 	h = int(endY-startY)
	# 	x = int(startX)
	# 	y = int(startY)

	# 	if(((w * h) > 500*4) & ((w * h) < 57600)):
	# 		blue_count += 1
	# 		x1 = x - 10 if (x - 10) > 0 else 0
	# 		y1 = y - 10 if (y - 10) > 0 else 0
	# 		x2 = x+w+10 if (x+w+10) < dim[1] else dim[1]-1
	# 		y2 = y+h+10 if (y+h+10) < dim[0] else dim[0]-1
	# 		cv2.rectangle(canvas, (x1, y1), (x2, y2), (255, 0, 0), 2)
	# 		roi_list.append((x1, y1, x2, y2))
	# 		cv2.putText(canvas, 'Blue', (x1, y1+14), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
	# print('b12', time.time()-t)
	# t = time.time()

	#print('11', time.time()-t)