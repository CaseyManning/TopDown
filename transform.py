import numpy as np
import cv2

maxWidth = 350
maxHeight = 500

p1 = (300, 338)
p2 = (670, 335)
p3 = (0, 530)
p4 = (959, 530)
pts = np.array((p2,p1,p3,p4),dtype=np.float32)

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

def transformImage(image, points=pts):
	return warp_perspective(pts, image)
