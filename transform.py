import numpy as np
import cv2

topDownRes = (960, 540)

p1 = (300, 338)
p2 = (670, 335)
p3 = (0, 530)
p4 = (959, 530)
pts = np.array((p2,p1,p3,p4),dtype=np.float32)

def warp_perspective(rect, grid):
	(tl, tr, br, bl) = rect
	# map the screen to a top-down, "birds eye" view
	dst = np.array([
		[0, 0],
		[topDownRes[0] - 1, 0],
		[topDownRes[0] - 1, topDownRes[1] - 1],
		[0, topDownRes[1] - 1]], dtype="float32")

	# the perspective to grab the screen
	M = cv2.getPerspectiveTransform(rect, dst)
	warp = cv2.warpPerspective(grid, M, (topDownRes[0], topDownRes[1]))
	return warp

def transformImage(image, points=pts):
	return warp_perspective(pts, image)

def getTransformPoints(callibration_image, checkerboard_dims):
	return cv2.findChessboardCorners(callibration_image, checkerboard_dims)
