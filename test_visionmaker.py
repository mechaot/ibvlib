'''
    (c) 2020 Andreas Pösch (andreas.poesch@googlemail.com)
    MIT License

    Make an instance of the visionmaker axis controller and
    issue some commands
'''

# do not be too harsh on test scripts
# pylint: disable=invalid-name, unused-import


from time import sleep
import matplotlib.pyplot as plt

from ibvlib.visionmaker.connector import VisionMaker, ULTIMAKER1_PARAMS
from ibvlib.camera.HttpCamera import HttpCamera

PARAMS = ULTIMAKER1_PARAMS
PARAMS.update({"host": "visionmaker", "port": 7777})

axis = VisionMaker(PARAMS, home_on_connect=False)
cam = HttpCamera("http://visionmaker:5000/cam")

axis.set_neopixel(None, color=(5, 0, 0), apply=True)
axis.set_neopixel2(None, color=(0, 5, 0), apply=True)

sleep(0.1)
for n in range(1, 5):
    axis.set_neopixel(n, color=(255, 0, 0), apply=False)
for n in range(15, 18):
    axis.set_neopixel(n, color=(0, 255, 0), apply=False)

axis.apply_neopixel()

cam.set_parameter(height=2400, width=3200)
img = cam.grab()

plt.imshow(img)
plt.show()

axis.set_neopixel(None, color=(1, 0, 0), apply=True)
axis.set_neopixel2(None, color=(0, 1, 0), apply=True)

axis.finish()
