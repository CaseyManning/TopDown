import cv2
import numpy as np
import transform
from transform import transformImage
from transform import warp_perspective_new
import sys
import time
import imutils

live = False;
robotImage = cv2.imread('robot.png')
# robotHeight, robotWidth, channels = robotImage.shape
n = 0

cameras = [0, 1, 2]

if live:
	cameras = [cv2.VideoCapture(x) for x in cameras]

# camera = cv2.VideoCapture(0)
maxWidth = 700
maxHeight = 1000

robotImage = cv2.imread('robot.png')

origFisheye = cv2.imread('fisheye.png')

DIM=(960, 540)
DIM2=(960, 540)
K=np.array([[263.1021173128426, 0.0, 477.98780306608234], [0.0, 261.30612719984185, 300.714230825097], [0.0, 0.0, 1.0]])
D=np.array([[-0.0007727739728155351], [-0.10019345132548932], [0.10790597488851726], [-0.040655761660861996]])

lastTime = time.time()

images = [cv2.imread('pinCenter.png'), cv2.imread('pinLeft.png'), cv2.imread('pinRight.png')]

p1 = (401, 400)
p2 = (586, 400)
p3 = (0, 540)
p4 = (960, 540)
uah =  np.array([p1, p2, p3, p4], dtype="float32")


def getImage(cam):
	retval, image = cam.read()
	return image

def undistort(img):
	h,w = img.shape[:2]
	map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
	return cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

def putTogetherImages(images):
	print("images: ", len(images))
	cameraPositions = [(1500, 1000), (1500, 2000), (1000, 1500), (2000, 1500)]
	rotated_images = images[:]
	for i, image in enumerate(images):
		rotated_images[i] = imutils.rotate_bound(image, i*90)
	composite_image = np.zeros((3000,3000,3), np.uint8)

	for pos, image in zip(cameraPositions, rotated_images):
		composite_image[pos[1]:pos[1]+image.shape[0], pos[0]:pos[0]+image.shape[1]] = image

	return composite_image

if live:
	while True:
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
		images = [cv2.resize(x, (960, 540)) for x in images]
		undistorted = [undistort(x) for x in images]
		transformed = [transformImage(x, uah) for x in undistorted]
		for im in undistorted:
			cv2.circle(im, p1, 2, (0,255,0), thickness=3, lineType=8, shift=0)
			cv2.circle(im, p2, 2, (0,255,0), thickness=3, lineType=8, shift=0)
			cv2.circle(im, p3, 2, (0,255,0), thickness=3, lineType=8, shift=0)
			cv2.circle(im, p4, 2, (0,255,0), thickness=3, lineType=8, shift=0)

		for i in range(len(transformed)):
			cv2.imshow('undistorted' + str(i), images[i])
			cv2.imshow('undistored' + str(i), undistorted[i])
			cv2.imshow('transformed' + str(i), transformed[i])

		key = cv2.waitKey(1)
		if key == 27:
			sys.exit()

try:
	images = [cv2.resize(x, (960, 540)) for x in images]
except:
	print('Null Image')

# ct = time.time()
# timePassed = ct - lastTime
# lastTime = ct
# print('FPS: ' + str(1/timePassed))

# cv2.imshow('OriginalA', images[2])
# tri1 = np.float32([[[0,450], [620,337], [620,450]]])
# tri2 = np.float32([[[0,450], [620,337], [620,450]]])
#
# r1 = cv2.boundingRect(tri1)
# r2 = cv2.boundingRect(tri2)

# warpMat = cv2.getAffineTransform( np.float32(tri1), np.float32(tri2))
# images[2] = cv2.warpAffine(images[2], warpMat, (r2[2], r2[3]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
# for i in range(len(images)):
# 	cv2.imshow('Original1' + str(i), images[i])

undistorted = undistort(origFisheye)

warped = warp_perspective_new(uah, undistorted)

cv2.circle(undistorted, p1, 2, (255,255,0), thickness=3, lineType=8, shift=0)
cv2.circle(undistorted, p2, 2, (0,0,255), thickness=3, lineType=8, shift=0)
cv2.circle(undistorted, p3, 2, (255,0,0), thickness=3, lineType=8, shift=0)
cv2.circle(undistorted, p4, 2, (0,255,0), thickness=3, lineType=8, shift=0)


cv2.imshow('1riginal', origFisheye)
cv2.imshow('2riginal', undistorted)
cv2.imshow('3riginal', warped)
# cv2.imshow('Top Down 2', warpedBad)


while True:
	key = cv2.waitKey(10000)
	if key == 27:
		sys.exit()
	if key == 32:
		print('saving images')
		for i in range(len(images)):
			cv2.imwrite(str(i) + 'testFisheye.png', images[i])
