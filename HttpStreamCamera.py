'''
    Grab images from HTTP video stream

    (c) 2020 Andreas Pösch (andreas.poesch@googlemail.com)
    MIT License
'''

import cv2

import urllib
from urllib.request import urlopen
import numpy as np

class HttpStreamCamera():
    '''
        get images from http stream, such as from an android device running a streaming app
    '''
    def __init__(self, uri):
        '''
            :param uri: web address uri
        '''
        self._uri = uri
        self.stream = urlopen(uri)
        self.data = bytes()

    def set_parameter(self, **kwargs):
        '''
            dummy function for API compatibility with *real* cameras
        '''
        return None

    def get_parameter(self, **kwargs):
        '''
            dummy function for compatibility
        '''
        return None

    def grab(self):
        '''
            get next image

            :returns: next image in stack or None if no image available
        '''
        while True:
            self.data += self.stream.read(4096) #read a junk of data
            # 0xff 0xd8 is the starting of the jpeg frame
            a = self.data.find(b'\xff\xd8')
            # 0xff 0xd9 is the end of the jpeg frame
            b = self.data.find(b'\xff\xd9')
            # Taking the jpeg image as byte stream
            if a!=-1 and b!=-1:
                # exctract between two magic bytes
                raw = self.data[a:b+2]
                # cut stream
                self.data= self.data[b+2:]
                # Decoding the byte stream to cv2 readable matrix format
                print("data:", len(raw), type(raw))
                img_buffer = np.fromstring(raw, dtype=np.uint8)
                img = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)

                #img = cv2.resize(img,None,fx=1/2, fy=1/2, interpolation = cv2.INTER_CUBIC)
                #img = cv2.resize(img,None,fx=1/2, fy=1/2, interpolation = cv2.INTER_LINEAR)
        
                return img