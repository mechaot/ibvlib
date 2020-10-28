# -*- coding: utf-8 -*-
import numpy as np

__author__ = "Andreas Poesch"
    
def otsuthreshold(mat, bins=256):
    """ calculate otsu-method based threshold of image matrix
    
        :param mat: input grayscale image matrix
        :param bins: number of different values to brute-force for otsu threshold
        :returns: threshold value
        
        calculation is perfomed based on a 0...255 histogram
        we do the moving variance, which is numerically very unstable,
        for speed over precision (as otsu is some predictive guessing anyway)
    """
    # get min and max image values
    m = np.min(mat)
    M = np.max(mat)    
    
    # otsu cannot work on monochromatic image
    if m >= (M-1):
        raise ValueError("Image has not enough contrast, so cannot binarize")
    
    # calculate histogram bins in brute-force rance
    histi, edges = np.histogram(mat.ravel(), bins=bins, range=(m,M))    
    #numpy.histogram is WAY faster then the scipy one
    hist = histi.astype(np.float)
    
    #initialize threshold and cost function 
    thres = 0
    quotient = 0.0    
 
    #cumulated histogram, this saves us summing up in the loop -> faster processing
    cumhist = np.cumsum(hist)
    #the "energy" or value-weighted counts
    histsum = np.cumsum([i * hist[i]  for i in range(bins)])         #sum

    #the last item in cumulated histogram should be count of all pixels
    _count = cumhist[-1]
    #energy
    _sum = histsum[-1]    
    
    #check minimum constrast
    if _sum == 0:
        print (mat)
        print('Error: no contrast wihin image: no otsu')
        print('Gray Value Range: ', m,M)
        return 0
        
    #total image mean value
    _mean = np.sum( histsum ) / _sum
    
    #we iterate over all bins 
    for t in range(bins):
        # calc mean on the lower part until t (the darker pixels)
        sum0 =   histsum[t] 
        count0 = cumhist[t]
        if (count0 <= 1):
            continue
        mean0 = sum0 / count0
        
        #calc mean on upper half (the brighter pixelss)
        sum1 = _sum - sum0 #np.sum( [i * hist[i] for i in range(t,256)] )
        count1 = _count - count0 # np.sum(hist[t:])
        if (count1 <= 1):
            continue
        mean1 = sum1 / count1

        # inner class variances, normalized to count of pixels in class
        var0 = np.sum( [(((mean0 - a) ** 2) * hist[a]) for a in range(t)] )
        var1 = np.sum( [(((mean1 - a) ** 2) * hist[a]) for a in range(t,256)] )
        varl = var0 + var1

        # inter-class variance w.r.t. global mean value
        varz = count0 * (mean0 - _mean)**2 + count1 * (mean1 - _mean)**2
        
        # the score function is the quotient
        q = varz / varl
        
        # if score is better than any previous score, then save as new score and also remember associated threshold t
        if (q > quotient):
            quotient = q
            thres = t        
 
    # make sure we have an int (depending on min/max and bin count this is not enforced)
    t = np.round(thres)
    # honestly, we got our t as the best otsu-index in bins -> need to grab the real pixel value from bin edges
    threshold_value = edges[t]
    # return the value
    return threshold_value
            
