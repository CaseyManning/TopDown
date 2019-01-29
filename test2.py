import cv2
import numpy as np
import transform
from transform import transformImage
import sys
import time

live = False;
robotImage = cv2.imread('robot.png')
robotHeight, robotWidth, channels = robotImage.shape
n = 0

cameras = [0, 1, 2, 3, 4]

if live:
	cameras = [cv2.VideoCapture(x) for x in cameras]

# camera = cv2.VideoCapture(0)
maxWidth = 700
maxHeight = 1000

robotImage = cv2.imread('robot.png')

#350, 344), (609, 336), (960, 503), (0, 503)
p1 = (290, 335)
p2 = (670, 335)
p3 = (0, 540)
p4 = (959, 540)

DIM=(960, 540)
K=np.array([[263.1021173128426, 0.0, 477.98780306608234], [0.0, 261.30612719984185, 300.714230825097], [0.0, 0.0, 1.0]])
D=np.array([[-0.0007727739728155351], [-0.10019345132548932], [0.10790597488851726], [-0.040655761660861996]])

lastTime = time.time()

images = [cv2.imread('0testFisheye.png'), cv2.imread('1testFisheye.png'), cv2.imread('2testFisheye.png')]

def getImage(cam):
	retval, image = cam.read()
	return image

def putTogetherImages(i1, i2, i3, i4):
	p1 = np.concatenate((i1, robotImage), axis=0)
	return np.concatenate((p1, i2), axis=0)

def undistort(img):
	h,w = img.shape[:2]
	map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
	return cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

def putTogetherImages(i1, i2, i3, i4):
	p1 = np.concatenate((i1, robotImage), axis=0)
	return np.concatenate((p1, i2), axis=0)

while True:
	if live:
		images = [getImage(x) for x in cameras]
		nulls = []
		for i in range(len(images)):
			if images[i] is None:
				print('Error reading image ' + str(i))
				noneImages = True
				nulls.append(i)
		nulls.reverse()
		for i in nulls:
			images.pop(i)
	if True:
		try:
			images = [cv2.resize(x, (960, 540)) for x in images]
		except:
			print('Null Image')
			continue

		ct = time.time()
		timePassed = ct - lastTime
		lastTime = ct
		print('FPS: ' + str(1/timePassed))

		undistorted = [undistort(x) for x in images]

		# calibrationImage = cv2.resize(image, (960, 540))
		# cv2.imshow("calibration", calibrationImage);
		# calibrationPoints = transform.getTransformPoints(calibrationImage, (9, 6))
		# print(calibrationPoints)
		for img in undistorted:
			cv2.circle(img, p1, 2, (0,255,0), thickness=3, lineType=8, shift=0)
			cv2.circle(img, p2, 2, (0,255,0), thickness=3, lineType=8, shift=0)
			cv2.circle(img, p3, 2, (0,255,0), thickness=3, lineType=8, shift=0)
			cv2.circle(img, p4, 2, (0,255,0), thickness=3, lineType=8, shift=0)

		for i in range(len(images)):
			cv2.imshow('Original1' + str(i), images[i])

		warped = [cv2.flip(transformImage(x), 1) for x in undistorted]

		for i in range(len(warped)):
			cv2.imshow('undistorted' + str(i), undistorted[i])

		topDown = putTogetherImages(warped[0], warped[1], warped[2], robotImage)
		cv2.imshow('allTogether' + str(i), undistorted[i])

		key = cv2.waitKey(1)
		if key == 27:
			sys.exit()
		if key == 32:
			print('saving images')
			for i in range(len(images)):
				cv2.imwrite(str(i) + 'testFisheye.png', images[i])
