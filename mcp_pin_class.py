
class mcp_pin:
    devices = [] # classvariable for listing all devices connected to the i2c-bus  
    states = [] # classvariable for to save states of banks on each device 
    '''class for adapting i2c syntax of MCP23017 device to micropython,
       to provide compatibility with machine functions. Use of multiple MCP-devices is supported.
       taken arguments:
           i2c: type = hex; takes chosen i2c-bus
           device_addr: type = hex; hardware configuration for i2c device address
           string[0]:
               bank: type = str; 'a' or 'b' for bank-A/B of MCP23017
           string[1]:
               pin: type = str; decimal number for GPIO-A/B register (takes values from 0 to 7)
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
        
    @classmethod
    def scan_devices(cls, i2c):
        '''scan for devices on i2c-bus, make list of cls.devices in increasing order,
        create cls.state-list for each device with two bytes in bytearray representing bank-A/B.
        Used to check if your instances take the right device-addresses as arguments'''
        cls.devices = i2c.scan()
        print(len(cls.devices), 'devices found:')
        for device in cls.devices:
            print(hex(device))
            cls.states.append(bytearray([0, 0]))
        
    def setup(self):
        '''for each instance, get self.index so each device is
        accessing the right memory-element in cls.states.'''
        i = 0 
        for device in mcp_pin.devices: 
            if self.device_addr == device:
                self.index = i
            i += 1
        '''defining GPIOA or GPIOB as output address for functions
        from IODIRA and IODIRB register.'''
        if self.bank == 'a':
            self.bank = 0x00
            self.regist_addr = 0x12
        elif self.bank == 'b':
            self.bank = 0x01
            self.regist_addr = 0x13
        '''init for I/O configuration on bank-A/B of device.
        self.io sets specified bank to in- or output.'''
        if self.io == 'OUT':
            self.io = 0x00
        elif self.io == 'IN':
            self.io = 0xff
        else:
            print('invalid:',self.io,'for in/output configuration!')
        self.i2c.writeto_mem(self.device_addr, self.bank, bytearray([self.io]))

    def on(self):
        '''everytime on() or off() get called, byte which is sent to self.regist_addr
        of device with self.device_addr refreshes pin state of all 8 pins on chosen port.
        State-byte is realized by bitwise-OR-operation: only converts 0 to 1 at desired digit.'''
        try:
            mask = 1 << self.pin # mask shifts value 1 in 0x01 byte to digit given by self.pin
            if self.bank == 0x00: 
                mcp_pin.states[self.index][0] |= mask # choose right device: [self.index], and choose right bank: [0/1]
                new_state = mcp_pin.states[self.index][0]
            elif self.bank == 0x01:
                mcp_pin.states[self.index][1]|= mask
                new_state = mcp_pin.states[self.index][1]                      
            #print(mcp_pin.states) # for debugging
            self.i2c.writeto_mem(self.device_addr, self.regist_addr, bytearray([new_state])) # new state gets transfered to given register
            #print('regist_addr:', self.regist_addr,'information byte:', self.i2c.readfrom_mem(self.device_addr, self.regist_addr, 1)) # for debugging
        except OSError as e:
            print(f"Error: I/O-access in on(): {e}") # in case of trouble with communication between mcp and pico

    def off(self):
        '''off() just inverts corresponding bit for self.pin, others remain untouched.
        State-byte is realized by bitwise-AND-operation: only converts 1 to 0 at desired digit.'''
        try:
            mask = 1 << self.pin # mask shifts value 1 in 0x01 byte to digit given by self.pin
            if self.bank == 0x00: 
                mcp_pin.states[self.index][0] &= ~mask # choose right device: [self.index], and choose right bank: [0/1]
                new_state = mcp_pin.states[self.index][0]
            elif self.bank == 0x01:
                mcp_pin.states[self.index][1] &= ~mask
                new_state = mcp_pin.states[self.index][1]
            #print(mcp_pin.states) # for debugging
            self.i2c.writeto_mem(self.device_addr, self.regist_addr, bytearray([new_state])) # new state gets transfered to given register
            #print('regist_addr:', self.regist_addr,'information byte:', self.i2c.readfrom_mem(self.device_addr, self.regist_addr, 1)) # for debugging
        except OSError as e:
            print(f"Error: I/O-access in in off(): {e}") # in case of trouble with communication between mcp and pico
        
    def value(self):
        '''compares mask-byte via bitwise-AND with byte at register-address of bank-A/B depending on which is set to 'IN'.'''
        try:
            val = self.i2c.readfrom_mem(self.device_addr, self.regist_addr, 1) # acquire first byte from register
            mask = 1 << self.pin
            if val[0] & mask: # check if for one pair of bits from value[0] and mask the AND-condition is true 
                return 1
            else:
                return 0
        except OSError as e:
            print(f"Error: I/O-access in in value(): {e}") # in case of trouble with communication between mcp and pico
    
