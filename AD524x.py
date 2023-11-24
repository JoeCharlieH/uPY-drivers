import utime as time

_SUBADRESS_MASK = const(0x80)
_SUBADRESS_RDAC_1 = const(0x00) #Default for AD5241, access register RDAC1
_SUBADRESS_RDAC_2 = const(0x80) #Access register RDAC2

_RS_MASK = const(0x40)
_RS_NO_MIDSCALE_RS = const(0x00) #After reset, all devices doen't modify their resistance value
_RS_MIDSCALE_RS = const(0x40)   #After reset, all devices go to midscale value

_SD_MASK = const(0x20)
_SD_INACTIVE = const(0x00)  #AD524X is active
_SD_ACTIVE = const(0x20)    #AD524X is inactive (Shutdown)

_OUT_PIN_MASK = const(0X10)
_OUT_HIGH_NONE = const(0x00) # Logic Low for O1 and O2
_OUT_HIGH_1 = const(0X10)    # Logic High only for O1
_OUT_HIGH_2 = const(0X08)    # Logic High only for O2
_OUT_HIGH_1_2 = const(0X18)  # Logic High for O1 and O2

_FS_10K = const(10000)       #10kohm Full Scale
_FS_100k = const(100000)     #100kohm Full Scale
_FS_1M = const(1000000)      #1Mohm Full Scale


_RDAC_REGISTER = ( 
_SUBADRESS_RDAC_1,  
_SUBADRESS_RDAC_2   
)

_MIDSCALE_RS = (
    _RS_NO_MIDSCALE_RS, 
    _RS_MIDSCALE_RS     
)

_SHUTDOWN = (
    _SD_INACTIVE,   
    _SD_ACTIVE      
)

_OUTPUT_PINS = (
    _OUT_HIGH_NONE,
    _OUT_HIGH_1,
    _OUT_HIGH_2,
    _OUT_HIGH_1_2
)

_FULL_SCALE =(
    _FS_10K, 
    _FS_100k,
    _FS_1M
)

class AD5242:
    def __init__(self, i2c, address=0x2C, fs=0, register=0, rs=0, sd=0, out=0):
        self.i2c = i2c
        self.adress = adress
        self.register = register
        self.fs = fs
        self.rs = rs
        self.sd = sd
        self.out = out
        self.temp2 = bytearray(2)

    def _write_register(self, config, raw):
        self.temp2[0] = config
        self.temp2[1] = raw
        self.i2c.writeto(self.address, self.temp2)
        
    def _read_register(self):
        self.i2c.readfrom(self.address,nbytes=1, self.temp2)
        return (self.temp2[0])

    def set_parameters(self, reg=0):
        self.mode = (_RDAC_REGISTER[reg] | _MIDSCALE_RS[self.rs] |
                     _SHUTDOWN[self.sd] | _OUTPUT_PINS[self.out])

    def write_value(self, value):
        self._write_register(self.mode, value)

    def read_value(self):
        res = self._read_register()
        return res
    
    def raw_to_ohms(self, raw):
        f= _FULL_SCALE[self.fs]/256.0
        return raw*f+60
    
        
        