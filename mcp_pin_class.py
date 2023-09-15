
class mcp_pin:
    state = bytearray([0]) # classvariable to memorize all states of output pins in current iteration
    '''class for adapting i2c syntax of MCP23017 device to micropython,
       to provide compatibility with machine functions. 
       taken arguments:
           i2c: type = hex; takes chosen i2c-bus
           device_addr: type = hex; hardware configuration for i2c device address
           string[0]:
               bank: type = str; 'a' or 'b' for bank-A or B of MCP23017
           string[1]:
               pin: type = str; decimal number for GPIO-A or B register (takes values from 0 to 7)
               (Note: bank-A counts pins from right to left, bank-B from left to right!
               ->see MCP-datasheet)
           io: type = str; takes 'OUT' for output and 'IN' for input on corresponding bank
           (Note: the given string sets ALL pins on one bank to in- or output)'''
    def __init__(self, i2c, device_addr, string, io):
        self.i2c = i2c
        self.device_addr = device_addr
        self.bank = string[0]
        self.pin = int(string[1])
        self.io = io
        self.setup()
        
    def setup(self):
        '''defining GPIOA or GPIOB as output address for functions
        from IODIRA and IODIRB register.'''
        if self.bank == 'a':
            self.bank = 0x00
            self.regist_addr = 0x12
        elif self.bank == 'b':
            self.bank = 0x01
            self.regist_addr = 0x13
        '''init for I/O configuration on bank-A or B of device.
        instance.io sets specified bank to in- or output.'''
        if self.io == 'OUT':
            self.io = 0x00
        elif self.io == 'IN':
            self.io = 0xff
        else:
            print('invalid:',self.io,'for in/output configuration!')
        self.i2c.writeto_mem(self.device_addr, self.bank, bytearray([self.io]))

    def on(self):
        '''everytime on() or off() get called, byte which is sent to instance.regist_addr
        of device with instance.device_addr refreshes pin state of all 8 pins on chosen port.
        state-byte is realized by class.state, which gets manipulated according to instance.pin.'''
        try:
            mask = 1 << self.pin # mask shifts value 1 in 0x01 byte to digit given by instance.pin 
            mcp_pin.state[0] |= mask # mask gets applied to the first byte in the bytearray class.state,
                                     # bitwise-OR-operator; only converts 0 to 1 at desired digit
            #print(mcp_pin.state)
            self.i2c.writeto_mem(self.device_addr, self.regist_addr, mcp_pin.state) # new state gets transfered to given register
        except OSError as e:
            print(f"Error: I/O-access in on(): {e}") # in case of trouble of communication between mcp and pico

    def off(self):
        '''off() just inverts corresponding bit for instance.pin, others remain untouched.'''
        try:
            mask = 1 << self.pin # mask shifts value 1 in 0x01 byte to digit given by instance.pin
            mcp_pin.state[0] &= ~mask # inverted mask gets applied, bitwise-AND-operator; only converts 1 to 0 at desired digit
            #print(mcp_pin.state)
            self.i2c.writeto_mem(self.device_addr, self.regist_addr, mcp_pin.state) # new state gets transfered to given register
        except OSError as e:
            print(f"Error: I/O-access in in off(): {e}") # in case of trouble of communication between mcp and pico
        
    def value(self):
        '''compares mask-byte via bitwise-AND with byte at register-address of bank-A or B depending on which is set to 'IN'.'''
        try:
            val = self.i2c.readfrom_mem(self.device_addr, self.regist_addr, 1) # acquire first byte from register
            mask = 1 << self.pin 
            if val[0] & mask: # check if for one pair of bits from value[0] and mask the AND-condition is true 
                return 1
            else:
                return 0
        except OSError as e:
            print(f"Error: I/O-access in in value(): {e}") # in case of trouble of communication between mcp and pico
    
