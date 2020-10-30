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
    def __init__(self, uri, fast_mode=False):
        '''
            :param uri: web address uri
            :param fast_mode: set true when querying images fast 
        '''
        self._uri = uri
        self._fast_mode = fast_mode
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

            in fast_mode we assume two consecutive calls to grab come so fast that
            we can continue reading from the stream even if last frame did gather a
            few bytes on the current frame already. in not fast mode we flush the
            buffer and look for the starting magic byte anew
        '''
        if not self._fast_mode:
            self.data = bytes() # flush buffer
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
                if len(raw) == 0:
                    continue
                img_buffer = np.fromstring(raw, dtype=np.uint8)
                img = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)

                #img = cv2.resize(img,None,fx=1/2, fy=1/2, interpolation = cv2.INTER_CUBIC)
                #img = cv2.resize(img,None,fx=1/2, fy=1/2, interpolation = cv2.INTER_LINEAR)
        
                return img[...,::-1]
