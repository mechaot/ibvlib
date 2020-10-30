# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on Sun Sep 28 19:15:18 2014

Robust serial terminal

@author: mechaot
"""

import serial
import serial.tools.list_ports as list_ports
from threading import Thread, Lock
from time import time, sleep
import re
import traceback

TERMCHAR = '\r\n'
DEBUG = False

def printTraceback(ex, *args):
#    log.error ("Exception: %s"%(str(ex)))
    #if args:
    #    log.error ("Data:" + str( args))
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("*** print_tb:")
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    print("*** print_exception:")
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=5, file=sys.stdout)

    s = traceback.format_exception(exc_type, exc_value, exc_traceback, limit=5)
    #log.critical("Exception: %s"%s)
    
def findSerialPorts():
    '''
        find a string list of possible ports
    '''
#    import platform
#    if platform.system().lower() in ["win32", "windows", "win64"]:
#            ports = ["COM%i" for i in range(32)]
#    else:
#        import glob
#        ports = glob.glob("/dev/ttyACM*") + glob.glob("/dev/ttyUSB*")
#    return ports
    return [port.device for port in list_ports.comports()]

class SerialTerminal(Thread):
    def __init__(self, port=None, baudrate=None, suppress_arduino_reboot=False):
        ''' initialize serial port class
        
            port:   port descriptor e.g. "COM1" or "/dev/ttyUSB0"
            baudrate:   bits per second

            if "port" is of format "(str):(int)" then we assume host:port and connect
            via tcp
        '''
        Thread.__init__(self)
        self.serial = None
        self.port = port
        self.baudrate = baudrate

        self.callback = None
        self.inLines = []
        self._termReq = False                
                
        if self.port != None and self.baudrate != None:
            self.connect(suppress_arduino_reboot=suppress_arduino_reboot)
            self.start()
        
    def connect(self, port=None, baudrate=None, suppress_arduino_reboot=False):
        ''' connect to port, maybe with overwriting settings
            suppress_arduino_reboot: set RTS and DTS such that arduino nano/uno does not reboot
            
            starts terminal thread right away
        '''
        if port != None:
            self.port = port
        if not isinstance(self.port, str):
            raise ValueError("Port specification must be a string")
        if baudrate is not None:
            self.baudrate = baudrate
        if self.port == None or self.baudrate == None:
            raise ValueError("Incomplete configuration")
        if self.serial != None:
            print("Warning: Serial already connected. Disconnecting first")
            self.disconnect()
                        
        self.serial = serial.Serial()            
        self.serial.port = self.port
        self.serial.baudrate = self.baudrate
        self.serial.timeout = 1
        if suppress_arduino_reboot:
            self.serial.setRTS(False)
            self.serial.setDTR(False)
        self._termReq = False
        
        self.serial.open()
        if not self.serial.isOpen():
            raise IOError("Error opening serial port")
        
    def close(self):
        self.terminate()
        sleep(2)
        self.disconnect()

        
    def disconnect(self):
        if self.serial != None:
            print(("Warning: Disconnecting serial port %s"%self.port))            
            self.serial.close()
            self.serial = None            
        else:
            print("Warning: Already disconnected")            
            
    def write(self, line, end=TERMCHAR):
        line = str(line)
        if not line.endswith(end):
            line += end
        if DEBUG:
            print(">", line)
        self.serial.write(bytes(line, encoding='ascii')) #let the lib raise esceptions
        # self.serial.flush()

    def request(self, rq, timeout = 1.0, pre_flush=True):
        ''' send one line and return the reply
            
            on timeout "None" is returned
        ''' 
        if pre_flush:
            self.flush()
        self.write(rq)
        tic = time()
        while (tic + timeout) < time():
            if len(self.inLines):
                return self.getLine()
            else:
                sleep(0.1)
        return None    #request timed out
                        
    def getLine(self):
        if len(self.inLines) > 0:
            return self.inLines.pop(0)
        else:
            return None                

    def flush(self):
        if DEBUG:
            print("FLUSH")

        self.inLines = []
        
        
    def terminate(self):
        self._termReq = True
        

    def _lineRecieved(self, line):
        line = line.decode("ascii", errors='ignore')
        if DEBUG:
            print("<", line)
        
        self.inLines.append(line)
        if self.callback is not None:
            self.callback(line)

            
    def run(self):
        self._termReq = False        
        buffer = bytearray()            
        while not self._termReq:
            ch = self.serial.read(1)
            buffer += ch
            idx = buffer.find(bytes('\n', 'ascii'))
            if idx >= 0:
                line = buffer[:idx]   #omit the newline char
                buffer = buffer[idx+1:]
                self._lineRecieved(line)
        print("Serial Thread ended")
        self.disconnect()
            


    