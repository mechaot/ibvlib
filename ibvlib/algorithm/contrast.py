'''
  contrast measure functions
'''

import numpy as np
import cv2


def sobel_contrast(img) -> float:
    '''
      contrast function by sobel

      img -- numpy image

      calculates a float contrast measure from an image; can be used for camera focussing
    '''
    #also works with 3channel sobel, each color separately
    img_x = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
    img_y = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)
    
    #contrast strength
    # note the "squared magnitude", this is intentional
    #   -> emphasize steep gradients over large-step gradients
    # do not take the sqrt!
    grad = img_x * img_x + img_y * img_y

    #image mean contrast strength
    # we can take the sqrt now for the final scalar -> in fact, any monotoneous function is appropriate here
    mean_input = img.mean()
    contrast = np.sqrt(np.mean(grad)) / mean_input
    return contrast
