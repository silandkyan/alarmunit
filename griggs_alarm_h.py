from machine import Pin

# Input pins
LC  = Pin(3, Pin.IN)  # Load cell                Normally Closed
T   = Pin(4, Pin.IN)  # Temperature (Eurotherm)  Normally Closed
S1B = Pin(5, Pin.IN)  # Sigma 1 bottom           Normally Opened
S3  = Pin(0, Pin.IN)  # Sigma 3                  Normally Opened
S1T = Pin(1, Pin.IN)  # Sigma 1 top              Normally Opened
NOF = Pin(2, Pin.IN)  # Emergency OFF (Notaus)   Normally Closed
L   = Pin(0, Pin.IN)  # Water leakage            Normally Opened
WF  = Pin(1, Pin.IN)  # Water flow               Normally Closed
AOF = Pin(1, Pin.IN)  # All alarms off           Normally Opened

# Output pins
THY   = Pin(7, Pin.OUT)  # Thyristor enabled
MEN   = Pin(6, Pin.OUT)  # Motor enabled
MOK   = Pin(5, Pin.OUT)  # Motor OK
WOK   = Pin(4, Pin.OUT)  # Water flow enabled
ALR   = Pin(3, Pin.OUT)  # Alarm buzzer
LMC   = Pin(4, Pin.OUT)  # Microcontroller OK
LPO   = Pin(5, Pin.OUT)  # Motor at top end
LNO   = Pin(6, Pin.OUT)  # Motor at bottom end

# Alarm indicators
LOF   = Pin(0, Pin.OUT)  # Emergency stop
LT    = Pin(1, Pin.OUT)  # Temperature
LLC   = Pin(2, Pin.OUT)  # Load cell
LWF   = Pin(3, Pin.OUT)  # Water flow
LL    = Pin(4, Pin.OUT)  # Water leakage
LS1T  = Pin(5, Pin.OUT)  # Sigma 1 crash: top
LS1B  = Pin(6, Pin.OUT)  # Sigma 1 crash: bottom
LS3   = Pin(7, Pin.OUT)  # Sigma 3 crash

# Constants
ON  = 1
OFF = 0

WF_FLAG  = 0x01
L_FLAG   = 0x02
S1T_FLAG = 0x04
S1B_FLAG = 0x08
S3_FLAG  = 0x10

# Function declarations
# In Python, you don't need to declare functions in advance, so these are not needed.
# Just define your functions in your Python script.
