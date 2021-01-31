from time import sleep
import matplotlib.pyplot as plt
import sys, os
import cv2
from scipy.optimize import curve_fit
import numpy as np
from imageio import imwrite
import json
from glob import iglob, glob

from ibvlib.visionmaker.connector import VisionMaker, ULTIMAKER1_PARAMS
from ibvlib.camera.HttpCamera import HttpCamera
from ibvlib.algorithm.contrast import sobel_contrast

PARAMS = ULTIMAKER1_PARAMS
PARAMS.update({"host": "visionmaker", "port": 7777})

axis = VisionMaker(PARAMS, home_on_connect=True)
print("home")
cam = HttpCamera("http://visionmaker:5000/cam")

pos = (115, 85, 20)
zrange = np.arange(5, 40, 0.5)
resolution = (1600,1200)
roi = [300, -500, -300, 500]   # trbl

def get_image_at(cam, pos, resolution=(2000,2400), show=True):
    h ,w = resolution
    cam.set_parameter(width=w, height=h)

    x,y,z = pos
    axis.move_to(x=x, y=y, z=z, speed=100)
    img = cam.grab()

    fn = "zfocus_x{:.2f}_y{:.2f}_z{:.2f}.png".format(*pos)
    imwrite(fn, img)
    return img

def gaus(x,a,x0,sigma):
    return a * np.exp(-(x - x0)** 2 / (2 * sigma ** 2))
    
def find_maximum(x, y):
  assert len(x) == len(y)

  max_idx = np.argmax(y)

  if max_idx == 0 or max_idx == (len(x) - 1):
    raise ValueError("Max at border of range, cannot interpolate")

  print("max_idx", max_idx, y[max_idx])

  n = len(x)                          #the number of data
  mean = sum(x*y)/n                   #note this correction
  sigma = sum(y*(x-mean)**2)/n        #note this correction
  popt, pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma], method='lm')
  print(popt)
  a, fit_mean, fit_sigma = popt
  print("optimum at z=", fit_mean)
  return fit_mean

contrasts = []

for z in zrange:
    coords = (pos[0], pos[1], z)
    img = get_image_at(cam, coords, resolution)

    t,r,b,l = roi
    img_roi = img[l:r, t:b, ...]
    img_contrast = sobel_contrast(img_roi)
    print("  C=", img_contrast)
    contrasts.append(img_contrast)

fit_mean = find_maximum(zrange, contrasts)

coords = (pos[0], pos[1], fit_mean)
img = get_image_at(cam, coords, resolution)
imwrite("zfocus_sharp.png", img)

plt.subplot(121)
plt.plot(zrange, contrasts)
plt.grid()
plt.title("Best focus at z={}".format(fit_mean))

plt.subplot(122)
plt.imshow(img)
plt.title("Sharpest position")
plt.show()
