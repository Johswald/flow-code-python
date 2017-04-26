#   write flow file

#   According to the matlab code of Deqing Sun and c++ source code of Daniel Scharstein  
#   Contact: dqsun@cs.brown.edu
#   Contact: schar@middlebury.edu

#   Author: Johannes Oswald, Technical University Munich
#   Contact: johannes.oswald@tum.de
#   Date: 26/04/2017

#	For more information, check http://vision.middlebury.edu/flow/ 

import numpy as np
import os

TAG_STRING = 'PIEH'

def write(flow, filename):

	assert type(filename) is str, "file is not str %r" % str(filename)
	assert filename[-4:] == '.flo', "file ending is not .flo %r" % file[-4:]

	height, width, nBands = flow.shape
	assert nBands == 2, "Number of bands = %r != 2" % nBands
	u = flow[: , : , 0]
	v = flow[: , : , 1]	
	assert u.shape == v.shape, "Invalid flow shape"
	height, width = u.shape

	f = open(filename,'wb')
	f.write(TAG_STRING)
	np.array(width).astype(np.int32).tofile(f)
	np.array(height).astype(np.int32).tofile(f)
	tmp = np.zeros((height, width*nBands))
	tmp[:,np.arange(width)*2] = u
	tmp[:,np.arange(width)*2 + 1] = v
	tmp.astype(np.float32).tofile(f)

	f.close()