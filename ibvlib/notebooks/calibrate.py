from time import sleep
import matplotlib.pyplot as plt
import sys, os
import cv2
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

for fn in iglob("./calibration*.png"):
    os.remove(fn)

def get_image_at(cam, pos, resolution=(2000,2400), show=True):
    h ,w = resolution
    cam.set_parameter(width=w, height=h)

    x,y,z = pos
    axis.move_to(x=x, y=y, z=z, speed=100)
    img = cam.grab()

    fn = "calibration_x{:.2f}_y{:.2f}_z{:.2f}.png".format(*pos)
    imwrite(fn, img)

    if show:
        plt.imshow(img)
    return img


#setup chessboard
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
chessboard = (12,12) #count of inner corners
fieldsize = 2.5 #in mm
# resolution = (1200, 1600)
resolution = (2000, 2400)

positions = [
    (115,85,20),  # dead center

    (115-50,85-50,20),
    (115-50,85,20),
    (115-50,85+50,20),
    (115   ,85-50,20),
    (115   ,85+50,20),
    (115+50,85-50,20),
    (115+50,85,20),
    (115+50,85+50,20),

    (115,85,22),
    (115,85,24),
    (115,85,26),
    (115,85,28),
    (115, 85, 30),
    
    (115-5 ,85,20),
    (115 + 5, 85, 20),
    (115-10 ,85,20),
    (115+10 ,85,20),    
    (115 ,85-5,20),
    (115 ,85+5,20)
]


def findChessboard(img):
    '''
        take camera image, try to find chessboard and return 
        qdebug image if successfull
        
        img: input image (color)
        returns (dbgimg, success)
            dbgimg: debug image with chessboard
            success: boolean true if cb found, false else
    '''
    imgpoints = []
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard, None)

    # If found, add object points, image points (after refining them)
    print("found chessboard:", ret)
    if ret == True:
        imgpoints = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)        
        #dbgimg = cv2.drawChessboardCorners(img.copy(), chessboard, corners2, ret)
    return imgpoints



objp = np.zeros((np.prod(chessboard),3), np.float32)
objp[:,:2] = np.mgrid[0:chessboard[0],0:chessboard[1]].T.reshape(-1,2) * fieldsize

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

axis.set_neopixel(None, color=(250, 250, 250), apply=True)

for pos in positions:
    print("Get image at", pos)
    img = get_image_at(cam, pos, resolution)

    cbimg = cv2.blur(img, (5,5))
    imgpts = findChessboard(cbimg)

    if len(imgpts):
        imgpoints.append(imgpts)
        objpoints.append(objp)
        print("Found cb points", len(imgpts), pos)
    
    else:
        print("No cb points", pos)
        
print("images captured.")

h, w = resolution
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (w,h),None,None)

print("results:", ret)
print("K:\n", mtx)
print("dist:", dist)


alpha = 0
K = mtx
Knew, roi=cv2.getOptimalNewCameraMatrix(K,dist,(w,h),alpha,(w,h))

data = {"K": [row.tolist() for row in K],
        "Knew": [row.tolist() for row in K],
        "roi": roi,
        "alpha": alpha,
        "width": w,
        "height": h,
        "chessboard": chessboard,
        "chesssize": fieldsize,
        "dist": dist.tolist()
}

filename = "calibration.json"
f = open(filename, "w")
json.dump(data, f, indent=4)
f.close()

print("saved calibration data:", filename)