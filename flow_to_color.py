#   computeColor color codes flow field U, V

#   According to the matlab code of Deqing Sun 
#   Contact: dqsun@cs.brown.edu

#   Author: Johannes Oswald, Technical University Munich
#   Contact: johannes.oswald@tum.de
#   $Date: 2017-04-26 (Wed, 04 April 2017) $

# Copyright 2017, Johannes Oswald.
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose other than its incorporation into a
# commercial product is hereby granted without fee, provided that the
# above copyright notice appear in all copies and that both that
# copyright notice and this permission notice appear in supporting
# documentation, and that the name of the author and Technical University Munich not be used in
# advertising or publicity pertaining to distribution of the software
# without specific, written prior permission.

# THE AUTHOR AND TECHNICAL UNIVERSITY MUNICH DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY
# PARTICULAR PURPOSE.  IN NO EVENT SHALL THE AUTHOR OR TECHNICAL UNIVERSITY MUNICH BE LIABLE FOR
# ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE. 


import glob
import cv2
import sys
import math
import numpy as np

def makeColorwheel():

	#  color encoding scheme

	#   adapted from the color circle idea described at
	#   http://members.shaw.ca/quadibloc/other/colint.htm

	RY = 15
	YG = 6
	GC = 4
	CB = 11
	BM = 13
	MR = 6

	ncols = RY + YG + GC + CB + BM + MR

	colorwheel = np.zeros([ncols, 3]) # r g b

	col = 0
	#RY
	colorwheel[0:RY, 0] = 255
	colorwheel[0:RY, 1] = np.floor(255*np.asarray([i for i in range(RY)])/RY)
	col = col+RY

	#YG
	colorwheel[col:YG+col, 0]= 255 - np.floor(255*np.asarray([i for i in range(YG)])/YG)
	colorwheel[col:YG+col, 1] = 255;
	col = col+YG;

	#GC
	colorwheel[col:GC+col, 1]= 255 
	colorwheel[col:GC+col, 2] = np.floor(255*np.asarray([i for i in range(GC)])/GC)
	col = col+GC;

	#CB
	colorwheel[col:CB+col, 1]= 255 -np.floor(255*np.asarray([i for i in range(CB)])/CB)
	colorwheel[col:CB+col, 2] = 255
	col = col+CB;

	#BM
	colorwheel[col:BM+col, 2]= 255 
	colorwheel[col:BM+col, 0] = np.floor(255*np.asarray([i for i in range(BM)])/BM)
	col = col+BM;

	#MR
	colorwheel[col:MR+col, 2]= 255 -np.floor(255*np.asarray([i for i in range(MR)])/MR)
	colorwheel[col:MR+col, 0] = 255
	
	return 	colorwheel

def computeColor(u, v):

	colorwheel = makeColorwheel();
	
	nan_u = np.isnan(u)
	nan_v = np.isnan(v)
	nanIdx = np.isnan(u+v)
	nan_u = np.where(nan_u)
	nan_v = np.where(nan_v) 
	u[nan_u] = 0
	u[nan_v] = 0
	v[nan_u] = 0 
	v[nan_v] = 0
	ncols = colorwheel.shape[0]
	rad = np.sqrt(np.multiply(u,u)+np.multiply(v,v)) 
	a = np.arctan2(-v, -u)/math.pi
	fk = (a+1) /2 * (ncols-1) + 1
	k0 = np.floor(fk)
	k1 = k0+1;
	print(colorwheel)
	for index, x in np.ndenumerate(k1):
		if x == ncols:
			k1[index] = 1
	f = fk - k0
	img = np.empty([k1.shape[0], k1.shape[1],3])
	for i in range(colorwheel.shape[1]):
		tmp = colorwheel[:,i]
		col0 = np.zeros([k1.shape[0], k1.shape[1]])
		col1 = np.zeros([k1.shape[0], k1.shape[1]])
		for index, x in np.ndenumerate(k0):
			col0[index] = tmp[int(x) - 1]/255.0
		for index2, y in np.ndenumerate(k1):
			col1[index2] = tmp[int(y) -1]/255.0
		
		on = np.ones([k1.shape[0], k1.shape[1]])
		col = np.multiply(on-f,col0) + np.multiply(f,col1)

		idx = np.where(rad <= 1)
		for index, x in np.ndenumerate(rad):
			if x <= 1:
				col[index] = 1 - rad[index]*(1-col[index])
			elif x > 1:
				col[index] = col[index]*0.75
			else:
				print("Error")
		print("COL", col[0, :])
		print(np.floor(255*np.multiply(col, 1-nanIdx))[150, :])
		img[:,:, i] = np.floor(255*np.multiply(col, 1-nanIdx))
	return img


def showhsv(flow):

	eps = sys.float_info.epsilon
	UNKNOWN_FLOW_THRESH = 1e9
	UNKNOWN_FLOW = 1e10

	u = flow[: , : , 0]
	v = flow[: , : , 1]

	maxu = -999
	maxv = -999

	minu = 999
	minv = 999

	maxrad = -1
	#fix unknown flow
	greater_u = np.where(u > UNKNOWN_FLOW_THRESH)
	greater_v = np.where(v > UNKNOWN_FLOW_THRESH)
	u[greater_u] = 0
	u[greater_v] = 0
	v[greater_u] = 0 
	v[greater_v] = 0

	maxu = max([maxu, np.amax(u)])
	minu = min([minu, np.amin(u)])

	maxv = max([maxv, np.amax(v)])
	minv = min([minv, np.amin(v)])
	rad = np.sqrt(np.multiply(u,u)+np.multiply(v,v)) 
	maxrad = max([maxrad, np.amax(rad)])
	print('max flow: %.4f flow range: u = %.3f .. %.3f; v = %.3f .. %.3f\n' % (maxrad, minu, maxu, minv, maxv))

	u = u/(maxrad+eps)
	v = v/(maxrad+eps)
	img = computeColor(u, v)

	return img

def main():
	truerange = 1
	height = 151
	width  = 151
	range_x = truerange * 1.04

	with open('colorTest.flo', "rb") as f:
		magic = np.fromfile(f, np.float32, count=1)
		if 202021.25 != magic:
			print 'Magic number incorrect. Invalid .flo file'
			exit()
		else:
			w = np.fromfile(f, np.int32, count=1)
			h = np.fromfile(f, np.int32, count=1)
			data = np.fromfile(f, np.float32, count=2*w*h)
			# Reshape data into 3D array (columns, rows, bands)
			flow = np.resize(data, (int(h), int(w), 2))


	#cv2.imshow('img_0',img_0)
	#cv2.imshow('img_1',img_1)

	a = flow[: , : , 0]
	b = flow[: , : , 1]
	mag, ang = cv2.cartToPolar(a, b)
	#ang = np.transpose(ang)
	#http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html
	hsv = np.zeros((int(h), int(w), 3), np.uint8)
	hsv[:, :, 0] = ang * 180 / np.pi / 2
	hsv[:, :, 1] = 255
	hsv[:, :, 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
	hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

	cv2.imshow('img_1',hsv)

	k = cv2.waitKey()
	u = flow[: , : , 0]
	v = flow[: , : , 1]

	img = showhsv(flow)
	hsv = img.astype(np.uint8)
	cv2.imshow('img_f',hsv)
	k = cv2.waitKey()