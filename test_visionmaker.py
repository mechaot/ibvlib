'''
    (c) 2020 Andreas Pösch (andreas.poesch@googlemail.com)
    MIT License

    Make an instance of the visionmaker axis controller and
    issue some commands
'''

# do not be too harsh on test scripts
# pylint: disable=invalid-name, unused-import

from time import sleep

from visionmaker.connector import VisionMaker, ULTIMAKER1_PARAMS

PARAMS = ULTIMAKER1_PARAMS
PARAMS.update({"host": "visionmaker", "port": 7777})

axis = VisionMaker(PARAMS, home_on_connect=False)


axis.set_neopixel(None, color=(0, 0, 0), apply=True)
axis.set_neopixel2(None, color=(0, 0, 0), apply=True)

sleep(0.5)

axis.set_neopixel(None, color=(5, 155, 155), apply=True)
