# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:36:37 2010

@author: Andreas
"""
__author__ = "Andreas Poesch"
__email__ =  "andreas.poesch@googlemail.com"

import numpy as np                              #numeric arrays

#DIRTY magic to make it faster (need to have LLVM compiler and numba package installed)
#from numba import jit, autojit
#@jit(cache=True) #store compiled version in cache (for 2nd execution of script)
#@autojit

def convolve(image, kernel):
    '''
        implement a basic grayscale image convolution filter

        image -- 2d-numpy array: the grayscale image to which the kernel is applied
        kernel -- 2d-numpy array: the filter kernel matrix

        returns: filtered image 2d numpy array 
        
        note: for border exceptions/handling assume the image
        is enlarged with a band of zeros
    '''
    if image.ndim != 2:
        raise ValueError("Not a grayscale image")
    if kernel.ndim != 2:
        raise ValueError("Not a 2d kernel")
    
    
    # get image shape: height and width
    h,w = image.shape
    # get the shape of the kernel
    kh, kw = kernel.shape # the shape of the kernel
    cy, cx = kh//2, kw//2 # center position index at half the shape. // is for integer division  5//2 = 2


    if not (kh % 2 == 1 and kw % 2 == 1):
        raise ValueError("Kernel is not odd times odd, has no center")

    # create result array forced to be of floating point type
    result = np.zeros( image.shape, dtype=np.float )

    for y in range(h):          #Don't use the filter on the border!
        for x in range(w):            
            value = 0.0
            for ky in range(kh):
                for kx in range(kw):
                    bildY = y - ky + cy
                    bildX = x - kx + cx
                    if (0 <= bildX < w) and (0 <= bildY < h):
                       value += image[bildY,bildX] * kernel[ky,kx]
                    #else:
                    #    value += 0.0 * kernel[ky,kx]
            result[y,x] = value

    return result
