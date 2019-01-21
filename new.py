import numpy as np
import cv2
import sys

# https://programtalk.com/vs2/python/10364/SnapSudoku/scripts/helpers.py/

n = 0
# camera = cv2.VideoCapture(0)
maxWidth = 700
maxHeight = 1000

camera = cv2.VideoCapture(0)

def getImage():
	retval, image = camera.read()
	return image

def warp_perspective(rect, grid):
	(tl, tr, br, bl) = rect
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

	# ...and now for the height of our new image
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

	# take the maximum of the width and height values to reach
	# our final dimensions
	# maxWidth = max(int(widthA), int(widthB))
	# maxHeight = max(int(heightA), int(heightB))

	# construct our destination points which will be used to
	# map the screen to a top-down, "birds eye" view
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype="float32")

	# calculate the perspective transform matrix and warp
	# the perspective to grab the screen
	M = cv2.getPerspectiveTransform(rect, dst)
	warp = cv2.warpPerspective(grid, M, (maxWidth, maxHeight))
	return warp
	# return self.make_it_square(warp)

while True:
	image = getImage()
	# print(len(image[0]), len(image))
	image = cv2.resize(image, (960, 540))
	p1 = (300, 338)
	p2 = (670, 335)
	p3 = (0, 530)
	p4 = (959, 530)
	pts = np.array((p2,p1,p3,p4),dtype=np.float32)

	warp = warp_perspective(pts, image)

	cv2.circle(image, p1, 3, (255,0,0), 3)
	cv2.circle(image, p2, 3, (255,0,0), 3)
	cv2.circle(image, p3, 3, (255,0,0), 3)
	cv2.circle(image, p4, 3, (255,0,0), 3)

	cv2.imshow('Original1', image)
	cv2.imshow('Transformed', cv2.flip(warp, 1))

	key = cv2.waitKey(10)
	if key == 32:
		print('saving image')
		cv2.imwrite(str(n) + '0stitching.png',image)
		cv2.imwrite(str(n) + '2stitching.png',warp)
		n += 1
	if key == 27:
		sys.exit()
