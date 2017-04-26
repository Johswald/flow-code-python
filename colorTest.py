#   creates a test image showing the color encoding scheme

#   According to the matlab code of Deqing Sun and c++ source code of Daniel Scharstein  
#   Contact: dqsun@cs.brown.edu
#   Contact: schar@middlebury.edu

#   Author: Johannes Oswald, Technical University Munich
#   Contact: johannes.oswald@tum.de
#   Date: 26/04/2017

#	For more information, check http://vision.middlebury.edu/flow/ 

import numpy as np
import cv2
import math

import computeColor
import writeFlowFile
import readFlowFile

truerange = 1
height = 151
width  = 151
range_f = truerange * 1.04

s2 = int(round(height/2))
x, y = np.meshgrid(np.arange(1, height + 1, 1), np.arange(1, width + 1, 1))

u = x*range_f/s2 - range_f
v = y*range_f/s2 - range_f

img = computeColor.computeColor(u/truerange, v/truerange)

img[s2,:,:] = 0
img[:,s2,:] = 0

cv2.imshow('test color pattern',img)
k = cv2.waitKey()

F = np.stack((u, v), axis = 2)
writeFlowFile.write(F, 'colorTest.flo')

flow = readFlowFile.read('colorTest.flo')

u = flow[: , : , 0]
v = flow[: , : , 1]		

img = computeColor.computeColor(u/truerange, v/truerange)

img[s2,:,:] = 0
img[:,s2,:] = 0

cv2.imshow('saved and reloaded test color pattern',img)
k = cv2.waitKey()

# color encoding scheme for optical flow
img = computeColor.computeColor(u/range_f/math.sqrt(2), v/range_f/math.sqrt(2));

cv2.imshow('optical flow color encoding scheme',img)
cv2.imwrite('colorTest.png', img)
k = cv2.waitKey()


