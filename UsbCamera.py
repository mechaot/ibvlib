'''
    Simple USB-Camera class
'''

import cv2

class UsbCamera():
    '''
        get images from a webcam or anything with a generic camera driver
    '''
    def __init__(self, cam_no=0):
        '''
            :param cam_no: opencvs camera index
        '''
        self._cam_no = cam_no
        self._capture = cv2.VideoCapture(cam_no)

    def set_parameter(self, **kwargs):
        '''
            dummy function for API compatibility with *real* cameras
        '''
        for key, val in kwargs.items():
            if key.lower() == "height":
                self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, int(val))
            elif key.lower() == "width":
                self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, int(val))


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
        success, img = self._capture.read() 
        if success:
            return img
        else:
            return None
