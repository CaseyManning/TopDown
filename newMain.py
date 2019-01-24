import cv2
import numpy as np
from transform import transformImage
import sys

live = True;
robotImage = cv2.imread('robot.png')
robotHeight, robotWidth, channels = robotImage.shape

if live:
	camera1 = cv2.VideoCapture(0)
	camera2 = cv2.VideoCapture(1)
	camera3 = cv2.VideoCapture(2)
	camera4 = cv2.VideoCapture(3)
else:
	image1 = cv2.imread('5.png')
	image2 = cv2.imread('5.png')
	image3 = cv2.imread('5.png')
	image4 = cv2.imread('5.png')

# camera = cv2.VideoCapture(0)
maxWidth = 700
maxHeight = 1000

def getImage(cam):
	retval, image = cam.read()
	return image

def putTogetherImages(i1, i2, i3, i4):
	p1 = np.concatenate((i1, robotImage), axis=0)
	return np.concatenate((p1, i2), axis=0)

while True:
	if live:
		image1 = getImage(camera1)
		image2 = getImage(camera2)
		image3 = getImage(camera3)
		image4 = getImage(camera4)
	# print(len(image[0]), len(image))
	try:
		image = cv2.resize(image1, (960, 540))
		image2 = cv2.resize(image2, (960, 540))
	except:
		print('Null Image')
		continue

	warp1 = cv2.flip(transformImage(image1), 1)
	warp2 = cv2.flip(cv2.flip(transformImage(image2), 1), 0)
	cv2.imshow('Transformed', cv2.flip(warp1, 1))
	cv2.imshow('Transformed2', cv2.flip(warp2, 1))

	cv2.imshow('Transformed', cv2.flip(warp1, 1))
	cv2.imshow('Transformed2', cv2.flip(warp2, 1))

	together = putTogetherImages(warp1, warp2, image3, image4)

	cv2.imshow('together',cv2.resize(together, (350, 800)))

	key = cv2.waitKey(10)
	if key == 27:
		sys.exit()
