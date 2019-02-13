import numpy as np
import cv2

topDownRes = (600, 600)

p1 = (478, 600)
p2 = (800, 600)
p3 = (0, 391)
p4 = (1260, 391)
pts2 = np.array((p2,p1,p3,p4),dtype=np.float32)

def warp_perspective(rect, grid):
	(tl, tr, br, bl) = rect
	# map the screen to a top-down, "birds eye" view
	dst = np.array([
		[0, 0],
		[topDownRes[0] - 1, 0],
		[topDownRes[0] - 1, topDownRes[1] - 1],
		[0, topDownRes[1] - 1]], dtype="float32")

	M = cv2.getPerspectiveTransform(rect, dst)
	warp = cv2.warpPerspective(grid, M, (topDownRes[0], topDownRes[1]))
	return warp

def warp_perspective_new(rect, image):

	dst = np.array([(300,300), (700, 300), (300, 700), (700, 700)], dtype="float32")
	h, mask = cv2.findHomography(rect, dst)
	warpedImage = cv2.warpPerspective(image, h, (1000, 1000))
	return warpedImage


def transformImage(image, points=pts2):
	return warp_perspective(points, image)

def getTransformPoints(callibration_image, checkerboard_dims):
	return cv2.findChessboardCorners(callibration_image, checkerboard_dims, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
