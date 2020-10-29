from time import sleep

from visionmaker.connector import VisionMaker, ULTIMAKER1_PARAMS

PARAMS = ULTIMAKER1_PARAMS
PARAMS.update({"host": "visionmaker", "port": 7777})

axis = VisionMaker(PARAMS, home_on_connect=False)


axis.set_neopixel(None, color=(0,0,0), apply=True)
axis.set_neopixel2(None, color=(0,0,0), apply=True)

axis.set_neopixel(None, color=(5,155,155), apply=True)
