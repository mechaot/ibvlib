'''
    (c) 2020 Andreas Pösch (andreas.poesch@googlemail.com)
    MIT License
'''
# do not be too harsh on test scripts
# pylint: disable=invalid-name, unused-import

from time import sleep
import cv2

from FileCamera import FileCamera
from UsbCamera import UsbCamera
from HttpStreamCamera import HttpStreamCamera
from HttpCamera import HttpCamera

# cam = FileCamera("./data", cycle_images=100)
# cam = UsbCamera(0)
# cam = HttpStreamCamera("http://192.168.10.182:8080/video?.mjpeg")
cam = HttpCamera("http://visionmaker:5000/cam")

while True:
    img = cam.grab()
    if img is None:
        print("Got no image")
        break

    cv2.imshow('frame', img)

    # read keyboard input, required to make the image buffer show
    key = cv2.waitKey(1)
    if key & 0xff in (ord("x"), ord("q"), 0x1b):   # 0x1b = ESC
        print("Aborting")
        break

cv2.destroyAllWindows()
print("finished.")
