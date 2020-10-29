# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2020-07-26

Robust tcp/ip mediated serial terminal

@author: mechaot
"""

import sys
from threading import Thread, Lock
import socket
from time import time, sleep
import re
import traceback

TERMCHAR = '\r\n'
DEBUG = False


def printTraceback(ex, *args):
    #    log.error ("Exception: %s"%(str(ex)))
    # if args:
    #    log.error ("Data:" + str( args))
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("*** print_tb:")
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    print("*** print_exception:")
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=5, file=sys.stdout)

    s = traceback.format_exception(exc_type, exc_value, exc_traceback, limit=5)
    #log.critical("Exception: %s"%s)


class TcpTerminal(Thread):
    def __init__(self, host, port, **kwargs):
        ''' initialize serial port class

            host: hostname
            port: portnumber
            kwargs: ignore for compatibility

            we're using non-encrypted unauthenticated tcp/ip serial bridge code
        '''
        Thread.__init__(self)
        self.host = host
        self.port = port

        self.sock = None

        self.callback = None
        self.inLines = []
        self._termReq = False

        if self.host and self.port:
            self.connect()
            self.start()

    def connect(self, host=None, port=None):
        ''' connect to port, maybe with overwriting settings
            suppress_arduino_reboot: set RTS and DTS such that arduino nano/uno does not reboot

            starts terminal thread right away
        '''
        if self.sock is not None:
            print(
                f"Warning, already connected to {self.host}:{self.port}, disconnecting first")
            self.close()
        if not isinstance(self.host, str):
            raise ValueError("Hostname must be a string")
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def close(self):
        '''
            end communication
        '''
        self.terminate()
        sleep(2)
        self.disconnect()

    def disconnect(self):
        if self.sock is not None:
            print(f"Warning: Disconnecting from {self.host}")
            self.sock.close()
            self.sock = None
        else:
            print("Warning: Already disconnected")

    def write(self, line, end=TERMCHAR):
        '''
            send one line/command to the server
        '''
        line = str(line)
        if not line.endswith(end):
            line += end
        if DEBUG:
            print(">", line)
        # let the lib raise esceptions
        self.sock.send(bytes(line, encoding='ascii'))
        # self.sock.flush()

    def request(self, rq, timeout=1.0, pre_flush=True):
        ''' send one line and return the reply

            on timeout "None" is returned
        '''
        if pre_flush:
            self.flush()
        self.sock.send(rq)
        tic = time()
        while (tic + timeout) < time():
            if len(self.inLines):
                return self.getLine()
            else:
                sleep(0.1)
        return None  # request timed out

    def getLine(self):
        '''
            get next line in receiving buffer
        '''
        if len(self.inLines) > 0:
            return self.inLines.pop(0)
        else:
            return None

    def flush(self):
        '''
            flush recv buffer
        '''
        if DEBUG:
            print("FLUSH")

        self.inLines = []

    def terminate(self):
        '''
            set flag to terminate worker thread
        '''
        self._termReq = True

    def _lineRecieved(self, line):
        '''
            internal: a full line has been received, push to line buffer
        '''
        line = line.decode("ascii", errors='ignore')
        if DEBUG:
            print("<", line)

        self.inLines.append(line)
        if self.callback is not None:
            self.callback(line)         # pylint: disable=not-callable

    def run(self):
        '''
            main loop, runs asynchronously in own thread
        '''
        self._termReq = False
        buffer = bytearray()
        while not self._termReq:
            try:
                ch = self.sock.recv(1)
            except ConnectionAbortedError: # will raise on finishing connection cleanly
                break
            buffer += ch
            idx = buffer.find(bytes('\n', 'ascii'))
            if idx >= 0:
                line = buffer[:idx]  # omit the newline char
                buffer = buffer[idx+1:]
                self._lineRecieved(line)
        print("Serial Thread ended")
        self.disconnect()
