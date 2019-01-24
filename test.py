import cv2
import numpy as np
from transform import transformImage
import sys

live = True;
robotImage = cv2.imread('robot.png')
robotHeight, robotWidth, channels = robotImage.shape
n = 0
if live:
	camera1 = cv2.VideoCapture(0)
else:
	image1 = cv2.imread('5.png')

# camera = cv2.VideoCapture(0)
maxWidth = 700
maxHeight = 1000

DIM=(960, 540)
K=np.array([[263.1021173128426, 0.0, 477.98780306608234], [0.0, 261.30612719984185, 300.714230825097], [0.0, 0.0, 1.0]])
D=np.array([[-0.0007727739728155351], [-0.10019345132548932], [0.10790597488851726], [-0.040655761660861996]])

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

while True:
    if live:
    	image1 = getImage(camera1)
    print(len(image1[0]), len(image1))
    try:
    	image = cv2.resize(image1, (960, 540))
    except:
    	print('Null Image')
    	continue
    image = undistort(image)
    warp = cv2.flip(transformImage(image), 1)

    cv2.imshow('Transformed', image)
    cv2.imshow('aaa', warp)

    key = cv2.waitKey(10)
    if key == 27:
    	sys.exit()
    if key == 32:
    	print('saving image')
    	cv2.imwrite(str(n) + 'calib.png',image)
    	n += 1