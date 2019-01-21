import numpy as np
import cv2
import sys

n = 0
# camera = cv2.VideoCapture(0)
maxWidth = 700
maxHeight = 1000

camera = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(1)

def getImage():
	retval, image = camera.read()
	return image

def getImage2():
	retval, image = camera2.read()
	return image

def warp_perspective(rect, grid):
	(tl, tr, br, bl) = rect
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

	# ...and now for the height of our new image
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

	# map the screen to a top-down, "birds eye" view
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype="float32")

	# the perspective to grab the screen
	M = cv2.getPerspectiveTransform(rect, dst)
	warp = cv2.warpPerspective(grid, M, (maxWidth, maxHeight))
	return warp
	# return self.make_it_square(warp)

while True:
	image = getImage()
	image2 = getImage2()
	# print(len(image[0]), len(image))
	try:
		image = cv2.resize(image, (960, 540))
		image2 = cv2.resize(image2, (960, 540))
	except:
		print('Null Image')
		continue
	p1 = (300, 338)
	p2 = (670, 335)
	p3 = (0, 530)
	p4 = (959, 530)
	pts = np.array((p2,p1,p3,p4),dtype=np.float32)

	warp = warp_perspective(pts, image)
	warp2 = warp_perspective(pts, image2)

	stitcher = cv2.createStitcher()
	try:
		(status, stitched) = stitcher.stitch([warp, warp2])
	except:
		print('Uah Uoh')
	cv2.circle(image, p1, 3, (255,0,0), 3)
	cv2.circle(image, p2, 3, (255,0,0), 3)
	cv2.circle(image, p3, 3, (255,0,0), 3)
	cv2.circle(image, p4, 3, (255,0,0), 3)

	print(status)
	if status == 0:
		cv2.imshow('stitched', stitched)
	else:
		cv2.imshow('Original1', cv2.resize(image, (480, 270)))
		cv2.imshow('Original2', cv2.resize(image, (480, 270)))
		cv2.imshow('Transformed', cv2.flip(warp, 1))
		cv2.imshow('Transformed2', cv2.flip(warp2, 1))

	key = cv2.waitKey(10)
	if key == 32:
		print('saving image')
		cv2.imwrite(str(n) + '0stitching.png',image)
		cv2.imwrite(str(n) + '1stitching.png',image2)
		cv2.imwrite(str(n) + '2stitching.png',warp)
		cv2.imwrite(str(n) + '3stitching.png',warp2)
		n += 1
	if key == 27:
		sys.exit()
