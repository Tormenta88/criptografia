import numpy as np
import cv2 as cv

img = cv.imread('sample_inputs/101_1.tif')
gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)

sift = cv.SIFT_create()
kp = sift.detect(gray,None)

img=cv.drawKeypoints(gray,kp,img)

cv.imwrite('sift_keypoints.jpg',img)


'''SIFT xfeatures2d
detect and compute
FlamBasedMatcher'''