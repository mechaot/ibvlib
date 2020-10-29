'''
    Simple USB-Camera class
'''

from urllib.parse import quote
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
        query_string = "&".join([quote(f"{k}={v}") for k, v in self._options.items()])
        url = self._uri + "?" + query_string

        res = requests.get(url)
        if res.status_code == 200:
            img = imread(res.content)
            return img
        else:
            print(res.status_code, res.text)
            return None
