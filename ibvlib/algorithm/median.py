# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:36:37 2010

@author: Andreas
"""

__author__ = "Andreas Poesch"
__email__ =  "andreas.poesch@googlemail.com"
                      
import numpy as np                              #numeric arrays

def median(image, size):
    '''
        implement a median rank filter for grayscale images

        :param image: the image to which the kernel is applied
        :param size: [height, width] of the median filter
        :returns: numpy array of same size as imgage

        note: for border exceptions/handling respect a dynamic size of 
        the sortable list and do not "hallucinate" out-of-bounds values
    '''
    # get image shape: height and width
    h,w = image.shape
    # get the shape of the kernel
    kh, kw = size# the shape of the kernel
    cy, cx = kh//2, kw//2 # center position index at half the shape. // is for integer division  5//2 = 2

    # create result array forced to be of floating point type
    result = np.zeros_like(image)   # equals: result = np.zeros( image.shape, dtype=image.dtype )

    for y in range(h):          #Don't use the filter on the border!
        for x in range(w):
            values = []
            for ky in range(kh):
                for kx in range(kw):
                    bildY = y - ky + cy
                    bildX = x - kx + cx
                    if (0 <= bildX < w) and (0 <= bildY < h):
                       values.append(image[bildY, bildX])
                       
            values.sort()
            result[y,x] = values[len(values)//2]

    return result

