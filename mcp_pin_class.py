
class mcp_pin:
    state = bytearray([0])
    '''class for adapting i2c syntax of MCP23017 device to micropython,
       to provide compatibility with machine functions. 
       taken arguments:
           i2c: takes chosen i2c-bus
           device_addr: hardware configuration for i2c device address,
           bank: bank-A or B of MCP23017
           pin: decimal number for GPIO-A or B register (takes values from 0 to 7)
           (Note: bank-A counts pins from right to left, bank-B from left to right!
           ->see MCP-datasheet)
           io: takes 0 for output and 1 for input on corresponding bank
           (Note: the given number sets ALL pins on one bank to in- or output)'''
    def __init__(self, i2c, device_addr, bank, pin, io):
        self.i2c = i2c
        self.device_addr = device_addr
        self.pin = pin
        self.io = io
        self.bank = bank
        self.setup()
        
    def setup(self):
        '''defining GPIOA or GPIOB as output address for on() and off()
        from IODIRA and IODIRB register'''
        if self.bank == 0x00:
            self.regist_addr = 0x12
        elif self.bank == 0x01:
            self.regist_addr = 0x13
        '''init for I/O configuration on bank-A or B of device.
        instance.io sets specified bank to in- or output:
        0 means output / 1 means input.'''
        if self.io == 0:
            self.io == 0x00
        elif self.io == 1:
            self.io = 0xff
        else:
            print('invalid value:',self.io,'for in/output configuration!')
        self.i2c.writeto_mem(self.device_addr, self.bank, bytearray([self.io]))

    def on(self):
        '''everytime on() or off() get called, byte which is sent to self.regist_addr
        of device with self.device_addr refreshes pin state of all 8 pins on chosen port.
        state-byte is realized by classvariable state, which gets overwritten according to instance.pin'''
        mask = 1 << self.pin
        mcp_pin.state[0] |= mask
        self.i2c.writeto_mem(self.device_addr, self.regist_addr, mcp_pin.state)
        

    def off(self):
        '''off() just inverts corresponding bit for instance.pin, others remain untouched.'''
        mask = 1 << self.pin
        mcp_pin.state[0] &= ~mask
        self.i2c.writeto_mem(self.device_addr, self.regist_addr, mcp_pin.state)
        
    def value(self):
        '''takes value of bit according to instance.pin from GPIO-A or B register byte'''
        value = self.i2c.readfrom_mem(self.device_addr, self.regist_addr, 1)
        mask = 1 << self.pin
        if value[0] & mask:
            return 1
        else:
            return 0
        
    
