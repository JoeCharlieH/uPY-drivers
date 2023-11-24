import utime as time

_UPDATE_MASK = const(0x30)
_UPDATE_TEMP_REGISTER = const(0x00)           #Updates the temporary register with incoming bus data
_UPDATE_TEMP_AND_DAC_REGISTER = const(0x10)   #Updates the temporary an DAC register from incoming bus data
_UPDATE_DAC_FROM_TEMP_REGISTER = const(0x20)  #Updates the DAC register with the temporary register's data
_UPDATE_ALL_DEVICES = const(0x30)             #Broadcast to all DAC devices in the bus to update the DAC register (update data depends from bit C<2>) 

_UPDATE_MASK = const(0x04)
_UPDATE_ALL_FROM_TEMP = const(0x00) #Update all DACs registers from their individual temporary registers 
_UPDATE_ALL_FROM_BUS = const(0x04)  #Update all DACs registers with incoming bus data


_WRITE_MODE_MASK = const(0x01)
_NORMAL_DAC_OP = const(0x00)    #Regular Write to temporary Register 
_POWER_DOWN_FLAG = const(0x01)  #Write to Power Mode Configuration Register


_POWER_SET_MASK = const(0xC0)
_LOW_POWER = const(0x00)        #DEFAULT
_FAST_SET = const(0x20)         #Fast Settling Time Mode
_PWD_1K_TO_GND = const(0x40)    #Power down with output connected to an internal 1k resistor to GND
_PWD_100K_TO_GND = const(0x80)  #Power down with output connected to an internal 100k resistor to GND
_PWD_HI_Z = const(0xC0)         #Power down with High Impedance Output

_UPDATE_SINGLE = (
    _UPDATE_TEMP_REGISTER, 
    _UPDATE_TEMP_AND_DAC_REGISTER, 
    _UPDATE_DAC_FROM_TEMP_REGISTER
)

_UPDATE_ALL = (
    _UPDATE_ALL_FROM_TEMP,
    _UPDATE_ALL_FROM_BUS
)

_PW_MODE = (
    _LOW_POWER,      
    _FAST_SET, 
    _PWD_1K_TO_GND, 
    _PWD_100K_TO_GND, 
    _PWD_HI_Z 
)

_OP_MODE =(
    _NORMAL_DAC_OP,
    _POWER_DOWN_FLAG
)

class DAC8571:
    def __init__(self, i2c, address=0x4C, update=1):
        self.i2c = i2c
        self.address = address
        self.upd = update
        self.temp3 =  bytearray(3)

    def _write_to(self, control, value):
        self.temp3[0] = control
        self.temp3[1] = value >> 8
        self.temp3[2] = value & 0xFF
        self.i2c.writeto(self.address, self.temp3)

    def _read_from(self):
        self.i2c.readfrom(self.address, self.temp3)
        return (self.temp3[0]<<8) | self.temp3[1]

    def set_powerdown(self, mode=0,pwrs=0):
        self.mode = (_UPDATE_SINGLE[self.upd]|_OP_MODE[mode])
        self.pwrs = (_PW_MODE[pwrs])

    def write(self, value):
        self._write_to((_UPDATE_SINGLE[self.upd]|_NORMAL_DAC_OP),value)

    def write_powerdown(self):
        temp_buff=bytearray(2)
        temp_buff[0]=self.pwrs
        temp_buff[1]=0x00
        self._write_to(self.mode,temp_buff.hex())

    def read(self):
        res=self._read_from()
        return res