from machine import Pin
from time import sleep

# Assuming you have the Timer and Check_Timer functions defined elsewhere
# If not, you'll need to implement them in Python
# For now, I'll use sleep as a placeholder

def Timer_3(state):
    global T3_flag
    if state == ON:
        T3_flag = True
    else:
        T3_flag = False

def Timer_5(state):
    sleep(5)

def Check_Timer_3():
    global T3_flag
    return T3_flag

def Check_Timer_5():
    return True

def Timer_1(state):
    sleep(1)

# Global variables
T3_flag = 0x00

# Main program
def main():
    Config()
    Init()
    InitTimers()
    
    while True:
        # All alarms OFF
        if AOF.value() == 1:
            Init()
            T3_flag = 0x00
            Timer_3(OFF)
            Timer_5(OFF)
            while AOF.value() == 1:
                if NOF.value() == 0: break
                if T.value() == 0:   LT.on()
                else:                 LT.off()
                if LC.value() == 0:  LLC.on()
                else:                 LLC.off()
                if WF.value() == 0:  LWF.on()
                else:                 LWF.off()
                if L.value() == 1:   LL.on()
                else:                 LL.off()
                if S1T.value() == 1:
                    LS1T.on()
                    LPO.on()
                else:
                    LS1T.off()
                    LPO.off()
                if S1B.value() == 1:
                    LS1B.on()
                    LNO.on()
                else:
                    LS1B.off()
                    LNO.off()
                if S3.value() == 1:  LS3.on()
                else:                 LS3.off()
            if NOF.value() == 1: Init()

        # Emergency stop or Temperature or Load cell (!NOF, !T, !LC)
        if NOF.value() == 0 or T.value() == 0 or LC.value() == 0:
            if NOF.value() == 0: LOF.on()
            if T.value() == 0:   LT.on()
            if LC.value() == 0:  LLC.on()
            AllOff(ON)

        # Water flow (!WF)
        if WF.value() == 0:
            LWF.on()
            if T3_flag == 0:
                Timer_3(ON)
                T3_flag = WF_FLAG
            if T3_flag == WF_FLAG:
                if Check_Timer_3():
                    Timer_3(OFF)
                    AllOff(OFF)
        if WF.value() == 1:
            LWF.off()
            if T3_flag == WF_FLAG:
                Timer_3(OFF)
                T3_flag = 0x00

        # Water leakage
        if L.value() == 1:
            LL.on()
            if T3_flag == 0:
                Timer_3(ON)
                T3_flag = L_FLAG
            if T3_flag == L_FLAG:
                if Check_Timer_3():
                    Timer_3(OFF)
                    AllOff(OFF)
        if L.value() == 0:
            LL.off()
            if T3_flag == L_FLAG:
                Timer_3(OFF)
                T3_flag = 0x00

        # Sigma 1 top
        if S1T.value() == 1:
            LS1T.on()
            LPO.on()
            if T3_flag == 0:
                Timer_3(ON)
                T3_flag = S1T_FLAG
            if T3_flag == S1T_FLAG:
                if Check_Timer_3():
                    Timer_3(OFF)
                    AllOff(ON)
        if S1T.value() == 0:
            LS1T.off()
            LPO.off()
            if T3_flag == S1T_FLAG:
                Timer_3(OFF)
                T3_flag = 0x00

        # Sigma 1 bottom
        if S1B.value() == 1:
            LS1B.on()
            LNO.on()
            if T3_flag == 0:
                Timer_3(ON)
                T3_flag = S1B_FLAG
            if T3_flag == S1B_FLAG:
                if Check_Timer_3():
                    Timer_3(OFF)
                    AllOff(ON)
        if S1B.value() == 0:
            LS1B.off()
            LNO.off()
            if T3_flag == S1B_FLAG:
                Timer_3(OFF)
                T3_flag = 0x00

        # Sigma 3
        if S3.value() == 1:
            LS3.on()
            if T3_flag == 0:
                Timer_3(ON)
                T3_flag = S3_FLAG
            if T3_flag == S3_FLAG:
                if Check_Timer_3():
                    Timer_3(OFF)
                    AllOff(ON)
        if S3.value() == 0:
            LS3.off()
            if T3_flag == S3_FLAG:
                Timer_3(OFF)
                T3_flag = 0x00

def Config():
    # Port configuration A[0..2] = analog, all others digital
    # In MicroPython, you can set the mode of a pin (analog or digital) when you create it
    # So this function may not be necessary

    # Port digital I/O configuration
    # In MicroPython, you can set the direction of a pin (input or output) when you create it
    # So this function may not be necessary

    pass

def Init():
    # Output ports: initial values
    # In MicroPython, you can set the initial value of a pin when you create it
    # So this function may not be necessary

    pass

def AllOff(delay):
    Alarm(ON)
    THY.off()
    if delay:
        Timer_5(ON)
        MotorOff()
        while not Check_Timer_5(): pass
        Timer_5(OFF)
        WOK.off()
    else:
        WOK.off()
        MotorOff()
    WaitReset()

def MotorOff():
    MOK.off()
    Timer_1(ON)
    while not Check_Timer_1(): pass
    MEN.off()
    Timer_1(OFF)

def WaitReset():
    LMC.off
