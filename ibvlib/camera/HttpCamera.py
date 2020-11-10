'''
    Simple USB-Camera class
'''

from urllib.parse import urlencode
import requests
from imageio import imread

class HttpCamera():
    '''
        get images from a webcam or anything with a generic camera driver
    '''
    def __init__(self, uri, ssl_verify=True):
        '''
            :param cam_no: opencvs camera index
        '''
        self._uri = uri
        self._verify = ssl_verify
        self._options = {"width": 800, "height": 600}

    def set_parameter(self, **kwargs):
        '''
            dummy function for API compatibility with *real* cameras
        '''
        self._options.update(kwargs)

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
        url = self._uri + "?" + urlencode(self._options)

        res = requests.get(url, verify=self._verify)
        if res.status_code == 200:
            img = imread(res.content)
            return img
        else:
            print(res.status_code, res.text)
            return None

    def __iter__(self):
        '''
            for image in cam...
        '''
        while True:
            img = self.grab()
            if img is None:
                return
            else:
                yield img