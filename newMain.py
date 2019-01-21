import cv2
import numpy as np
from transform import transformImage
import sys

live = False;
robotImg = cv2.imread('robot.png')
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

def compositeImages(im1, im2, im3, im4):
	fail

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

	# stitcher = cv2.createStitcher()
	# try:
	# 	(status, stitched) = stitcher.stitch([warp, warp2])
	# except:
	# 	print('Uah Uoh')
	# 	continue
	#
	# print(status)
	# if status == 0:
	# 	cv2.imshow('stitched', stitched)

	# cv2.imshow('Original1', cv2.resize(image, (480, 270)))
	# cv2.imshow('Original2', cv2.resize(image2, (480, 270)))
	cv2.imshow('Transformed', cv2.flip(warp1, 1))
	cv2.imshow('Transformed2', cv2.flip(warp2, 1))
	together = np.concatenate((warp1, warp2), axis=0)
	cv2.imshow('together',cv2.resize(together, (350, 1000)))

	key = cv2.waitKey(10)
	if key == 27:
		sys.exit()
