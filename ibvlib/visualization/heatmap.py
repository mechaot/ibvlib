# -*- coding: utf-8 -*-
"""
Created on Tue Jan 06 17:14:41 2015

@author: poesch
"""

import matplotlib.pyplot as plt
import numpy as np

def heatmap(data, gridcolor='face', cmap=None, colorbar=False):
    ''' from (small matrices) make annotated plot
        if colorbar then add one
        
        data -- 2d numpy array to display as heatmap
    '''
    if not data.ndim == 2:
        raise ValueError("Only supporting 2d arrays")
    heatmap = plt.pcolormesh(data, edgecolors=gridcolor, cmap=cmap)#, axes='tight')
    m,M = np.min(data), np.max(data)
    b = m + (M-m) * 0.2
    B = m + (M-m) * 0.8
    
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            plt.text(x + 0.5, y + 0.5, '%.0f' % data[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     color='black' if b < data[y,x] else 'white' ,
                     #bbox=dict(facecolor='white', alpha=0.5)   #hintergrundfarbe
                     )
    
    if colorbar:
        plt.colorbar(heatmap)
        


        
        
if __name__ == '__main__':
    data = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    plt.subplot(121)
    heatmap(data, gridcolor='#00004f')
    
    #plt.grid(1)
    plt.show()            