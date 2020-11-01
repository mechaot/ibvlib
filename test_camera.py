"""
    (c) 2020 Andreas Pösch (andreas.poesch@googlemail.com)
    MIT License

    Make instances of one of the camera classes and grab images until pressing Esc or Space
    Pressing "s" will save current image frame
"""
# do not be too harsh on test scripts
# pylint: disable=invalid-name, unused-import

from time import sleep, time
from imageio import imwrite
import cv2

# from ibvlib.camera.FileCamera import FileCamera
from ibvlib.camera.UsbCamera import UsbCamera
# from ibvlib.camera.HttpStreamCamera import HttpStreamCamera
# from ibvlib.camera.HttpCamera import HttpCamera

# cam = FileCamera("./data", cycle_images=100)
cam = UsbCamera(0)
# cam = HttpStreamCamera("http://192.168.10.130:8080/video?.mjpeg", fast_mode=False)
# # This works for the Android App "IP Webcam" https://play.google.com/store/apps/details?id=com.pas.webcam
# cam = HttpCamera("http://visionmaker:5000/cam")

while True:
    img = cam.grab() # F12
    if img is None:
        print("Got no image")
        break

    if img.ndim == 3: # color images dimensions=(height, width, channels) need conversion
        cv2.imshow('frame', img)  # just display image
        # cv2.imshow('frame', img[:, :, ::-1])  # RGB -> BGR for opencv imshow; reverse order in 3rd matrix dimension
    else: # gray images dimensions=(height, width) are non-problematic
        cv2.imshow('frame', img)

    # read keyboard input, required to make the image buffer show
    key = cv2.waitKey(1)
    if key & 0xff in (ord("x"), ord("q"), 0x1b):   # 0x1b = ESC
        print("Aborting")
        break
    elif key % 0xff == ord("s"):
        filename = "image_{}.png".format(time())
        imwrite(filename, img)
        print("Saved {}".format(filename))

cv2.destroyAllWindows()
print("finished.")
