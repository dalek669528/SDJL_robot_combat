import cv2
import numpy as np

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

def detect_color(img):
	canvas = img.copy()
	#print(canvas.shape)
	dim = canvas.shape

	red_mask   = getRed(canvas)
	contours_red, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	green_mask = getGreen(canvas)
	contours_green, hierarchy = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	roi_list = []
	for cnt in contours_red:
		x, y, w, h = cv2.boundingRect(cnt)
		if((w * h) > 500*4):
			cv2.rectangle(canvas, (x - 10, y - 10), (x + w + 10, y + h + 10), (0, 255, 0), 2)
			x1 = x - 10 if (x - 10) > 0 else 0
			y1 = y - 10 if (y - 10) > 0 else 0
			x2 = x+w+10 if (x+w+10) < dim[1] else dim[1]-1
			y2 = y+h+10 if (y+h+10) < dim[0] else dim[0]-1

			roi_list.append((x1, y1, x2, y2))
			cv2.putText(canvas, 'Red', (x - 10, y - 14), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

	for cnt in contours_green:
		x, y, w, h = cv2.boundingRect(cnt)
		if((w * h) > 500*4):
			cv2.rectangle(canvas, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 0, 0), 2)
			x1 = x - 10 if (x - 10) > 0 else 0
			y1 = y - 10 if (y - 10) > 0 else 0
			x2 = x+w+10 if (x+w+10) < dim[1] else dim[1]-1
			y2 = y+h+10 if (y+h+10) < dim[0] else dim[0]-1

			roi_list.append((x1, y1, x2, y2))
			cv2.putText(canvas, 'Green', (x - 10, y - 14), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

	return canvas, np.array(roi_list)
