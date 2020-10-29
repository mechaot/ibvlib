'''
    Emulate a camera by loading images from files
    and providing same interface as camera

    (c) 2020 Andreas Pösch (andreas.poesch@googlemail.com)
    MIT License
'''

from os.path import isfile
from glob import glob
from imageio import imread

class FileCamera():
    '''
        read files one after another for grabbing images
    '''
    def __init__(self, file_or_folder, cycle_images=True):
        '''
            :param file_or_folder: (str) a filename (with wildcard support) or name of folder to load
            :param cycle_images: (bool or int) None/False: cycle one time, then end; True: cycle infinitely, (int) cycle this often times
        '''
        self._source = file_or_folder
        self._filenames = []
        self._current_index = 0
        self._cycle = cycle_images

        self.rescan_files()

    def rescan_files(self):
        '''
            look for relevant files in self._source

            can be called manually to rescan, i.e. if
            files have beed added by another process

            :returns: number of files found
        '''
        file_list = []
        if isfile(self._source):
            file_list = [self._source]
        elif isinstance(self._source, str):
            file_list += glob(self._source + "/*.png", recursive=False)
            file_list += glob(self._source + "/*.bmp", recursive=False)
            file_list += glob(self._source + "/*.jpg", recursive=False)
        else:
            raise ValueError("Source not set properly")
        self._filenames = file_list
        if not self._cycle: # when expired, reallow all
            self._current_index = 0
        return len(file_list)

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
        if self._current_index < 0 or self._current_index >= len(self._filenames):
            if isinstance(self._cycle, int) and self._cycle > 0:
                self._cycle -= 1
                self._current_index = 0
            elif self._cycle is True:
                self._current_index = 0
            else:
                return None # cycled out

        if self._filenames:
            active_fn = self._filenames[self._current_index]
            self._current_index += 1
            img = imread(active_fn)
            return img
        else:
            return None
