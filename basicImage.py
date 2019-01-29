import cv2
import numpy as np
import transform
from transform import transformImage
import sys

live = True;
robotImage = cv2.imread('robot.png')
robotHeight, robotWidth, channels = robotImage.shape
n = 0
if live:
	# camera1 = cv2.VideoCapture(4)
	camera1 = cv2.VideoCapture(0)
	camera2 = cv2.VideoCapture(1)
	camera3 = cv2.VideoCapture(2)
	camera4 = cv2.VideoCapture(3)
else:
	image1 = cv2.imread('5.png')

def getImage(cam):
	retval, image = cam.read()
	return image


while True:
	if live:
		image1 = getImage(camera1)
		image2 = getImage(camera2)
		image3 = getImage(camera3)
		image4 = getImage(camera4)
	try:
		image1 = cv2.resize(image1, (960, 540))
		image2 = cv2.resize(image2, (960, 540))
		image3 = cv2.resize(image3, (960, 540))
		image4 = cv2.resize(image4, (960, 540))
	except:
		print('Null Image')
		continue

	cv2.imshow('Original1', image1)
	cv2.imshow('Original2', image2)
	cv2.imshow('Original3', image3)
	cv2.imshow('Original4', image4)
	# cv2.imshow('Unfisheyed', image1)

	key = cv2.waitKey(10)
	if key == 27:
		sys.exit()
