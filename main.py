import numpy as np
import cv2
import sys

n = 0
camera = cv2.VideoCapture(0)

groundDist = 1

DIM=(1280, 960)
K=np.array([[802.396025426153, 0.0, 746.5423655130637], [0.0, 802.8910112346373, 422.33390924614145], [0.0, 0.0, 1.0]])
D=np.array([[-0.04604657032144514], [0.059120469125113276], [-0.7955394607318061], [0.9293220346274716]])

def getImage():
	retval, image = camera.read()
	return image


def undistort(img):
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    return cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

def findPoints():
    return((0,0), (0,0), (0,0), (0,0))

def order_points(pts):

	rect = np.zeros((4, 2), dtype = "float32")


	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect

	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	return warped

while True:
    image = getImage()

    # retval, K, D, rvecs, tvecs	=	cv.fisheye.calibrate(objectPoints, imagePoints, image_size, K, D[, rvecs[, tvecs[, flags[, criteria]]]]	)

    # # use Knew to scale the output
    # Knew = K.copy()
    # Knew[(0,1), (0,1)] = 0.4 * Knew[(0,1), (0,1)]
    img_undistorted = undistort(image)

    transformed = four_point_transform(img_undistorted, np.array([(0, 600), (1000, 600), (1000, 800), (0, 800)]))

    cv2.imshow('Fisheye', transformed)
    cv2.imshow('Top Down', img_undistorted)

    key = cv2.waitKey(10)
    if key == 32:
        print('saving image')
        cv2.imwrite(str(n) + '.png',image)
        n += 1
    if key == 27:
    	sys.exit()
