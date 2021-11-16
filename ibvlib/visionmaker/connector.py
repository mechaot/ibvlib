# corexy class 


from .serialterm import SerialTerminal, findSerialPorts
from .tcpterm import TcpTerminal
from time import sleep, time

def output(txt):
    print("<", txt)

ULTIMAKER1_PARAMS = \
    {
        "port": None,
        "baudrate": 115200,
        "x_min": 1,  # >0 to ever trigger homing
        "y_min": 1,
        "z_min": 1,
        "x_max": 290,
        "y_max": 205,
        "z_max": 150,
    }

class VisionMaker():
    '''
        marlin based axis system with special modifications for vision maker
    '''
    DEBUG = True

    def __init__(self, params=None, home_on_connect=True):
        self._params = params
        if "host" in params:
            self._serial = TcpTerminal(host=params["host"], port=params["port"])
        else:
            if params.get("port") is None:
                params["port"] = findSerialPorts()[0]  # let it raise if we have no serial
            self._serial = SerialTerminal(port=params["port"], baudrate=params["baudrate"], suppress_arduino_reboot=True)
        #self._serial.callback = output
        if self.DEBUG:
            print("connected")
    
        if home_on_connect:
            self.home()
                        
            
    def finish(self):
        if self._serial:
            self._serial.close()
    
    def cmd(self, line):
        self._serial.write(line, end="\r\r")
        self._serial.flush()

    def is_moving(self):
        self.cmd("M49")  # custom code
        r = None
        while r is None:
            r = self._serial.getLine()
            if r == "BUSY":  # ignore ack to the ? command
                sleep(0.15)
                return True
            elif r == "IDLE":
                return False
            if r == "ok":
                r = None

    def home(self, timeout=60):
        '''
            home all axis


        '''
        if self.DEBUG:
            print("homing...", flush=True, end="")
        tic = time()
        self.cmd("G28")
        if timeout is None:
            return True

        while True:
            if (tic + timeout) < time():
                if self.DEBUG:
                    print("Timeout homing")
                return False

            if self.is_moving() is False:
                return True
                
        if self.DEBUG:
            print("Error homing")
        return False
    
    def wait_done(self, timeout=5.0):
        ''' block until no movement in planner

            :returns: True if idle, False on timeout
        '''
        tic = time()
        started_motion = False
        while True:
            if (tic + timeout) < time():
                return False
            if self.is_moving() == False:
                return True
            sleep(0.05)
       
            
    def move_to(self, x=None, y=None, z=None, speed=None, timeout=15.0):
        '''
            move table to x,y position
            
            :param x: x position, None to keep position
            :param y: y position, None to keep position
            :param z: z position, None to keep position
            :param speed: speed of movement mm/sec, None to use "fast" G0
            :param timeout: seconds to block at max until finished, 0 to immediately return
            :returns: seconds the motion took, None of not there
        '''        
        rq = "G0"
        if x is not None:
            if not self._params["x_min"] <= x <= self._params["x_max"]:
                raise ValueError(f"X-Axis requested out of range {x} [{self._params['x_min']}, {self._params['x_max']}])")
            rq += f" X{x}"
        if y is not None:
            if not self._params["y_min"] <= y <= self._params["y_max"]:
                raise ValueError(f"X-Axis requested out of range {y} [{self._params['y_min']}, {self._params['y_max']}])")
            rq += f" Y{y}"
        if z is not None:
            if not self._params["z_min"] <= z <= self._params["z_max"]:
                raise ValueError(f"Z-Axis requested out of range {z} [{self._params['z_min']}, {self._params['z_max']}])")
            rq += f" Z{z}"
        if speed is not None:
            f = speed * 60.0 # hardware expects mm/min
            rq +=  f" F{f:.3f}"
        if self.DEBUG:
            print(rq)
        self.cmd(rq)
        if timeout is not None:
            return self.wait_done(timeout)
        else:
            return None
 
    
    def set_neopixel(self, index, r=None, g=None, b=None, color=None, apply=False):
        '''
            :param index: (int) which led to set, "None" for "all"
            :param r,g,b: set this color component only, None to leave
            :param color: if set, 3-tuple r,g,b 0...255 each
            :param apply: if set, then immediately apply
        '''
        if index is None:
            index = -1
            apply = True
        if isinstance(index, int):
            cmd = f"M61 p{index}"
            if color is None:
                if r is not None:
                    cmd += f" r{r}"
                if g is not None:
                    cmd += f" g{g}"
                if b is not None:
                    cmd += f" b{b}"
            else:
                cmd += " r{0} g{1} b{2} ".format(*color)
            if apply:
                cmd += " a1"
            self.cmd(cmd)
        elif hasattr(index, '__iter__'):
            for i, idx in enumerate(index):
                self.set_neopixel(idx, r, g, b, color, apply=False)
                sleep(0.005) # give comm time enough
                if apply:
                    self.apply_neopixel()
        else:
            raise TypeError("Index neither int nor list of int")

    def apply_neopixel(self):
        '''
            after setting some neopixels without apply, send the apply cmd
        '''
        self.cmd("M62")

    def set_neopixel2(self, index, r=None, g=None, b=None, color=None, apply=False):
        '''
            :param index: (int) which led to set, "None" for "all"
            :param r,g,b: set this color component only, None to leave
            :param color: if set, 3-tuple r,g,b 0...255 each
            :param apply: if set, then immediately apply
        '''
        if index is None:
            index = -1
            apply = True
        if isinstance(index, int):
            cmd = f"M63 p{index}"
            if color is None:
                if r is not None:
                    cmd += f" r{r}"
                if g is not None:
                    cmd += f" g{g}"
                if b is not None:
                    cmd += f" b{b}"
            else:
                cmd += " r{0} g{1} b{2} ".format(*color)
            if apply:
                cmd += " a1"
            self.cmd(cmd)
        elif hasattr(index, '__iter__'):
            for i, idx in enumerate(index):
                self.set_neopixel2(idx, r, g, b, color, apply=False)
                sleep(0.005) # give comm time enough
                if apply:
                    self.apply_neopixel2()
        else:
            raise TypeError("Index neither int nor list of int")


    def apply_neopixel2(self):
        '''
            after setting some neopixels without apply, send the apply cmd
        '''
        self.cmd("M64")


    def set_pwm(self, r=None, g=None, b=None):
        '''
            set pwm output

            :param r: value for red channel 0...255, None to leave unchanged
            :param g: value for green channel 0...255, None to leave unchanged
            :param b: value for blue channel 0...255, None to leave unchanged
        '''
        cmd = "M50"
        if r is not None:
            cmd += f" r{r}"
        if g is not None:
            cmd += f" g{g}"
        if b is not None:
            cmd += f" b{b}"
        self.cmd(cmd)

    def set_pwm2(self, b=None):
        '''
            set lower singel channel pwm output

            :param b: value for brightness channel 0...255, None to leave unchanged
        '''
        cmd = "M51"
        if b is not None:
            cmd += f" b{b}"
        self.cmd(cmd)
