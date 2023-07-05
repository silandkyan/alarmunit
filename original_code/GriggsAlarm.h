/******************************************************************************/
/* Griggs alarm unit definitions                                              */
/*                                                                            */
/*    Author         Eric Reusser                                             */
/*    Version        1.1                                                      */
/*    Creation date  05/2017                                                  */
/*    Version date   07/2017                                                  */
/******************************************************************************/

/*** Pin assignment ***********************************************************/

// Input pins

sbit LC  at PORTA.B3;     // Load cell                Normally Closed
sbit T   at PORTA.B4;     // Temperature (Eurotherm)  Normally Closed
sbit S1B at PORTA.B5;     // Sigma 1 bottom           Normally Opened
sbit S3  at PORTE.B0;     // Sigma 3                  Normally Opened
sbit S1T at PORTE.B1;     // Sigma 1 top              Normally Opened
sbit NOF at PORTE.B2;     // Emergency OFF (Notaus)   Normally Closed
sbit L   at PORTC.B0;     // Water leakage            Normally Opened
sbit WF  at PORTC.B1;     // Water flow               Normally Closed
sbit AOF at PORTD.B1;     // All alarms off           Normally Opened

// Output pins

sbit THY   at LATC.B7;    // Thyristor enabled
sbit MEN   at LATC.B6;    // Motor enabled
sbit MOK   at LATC.B5;    // Motor OK
sbit WOK   at LATC.B4;    // Water flow enabled
sbit ALR   at LATD.B3;    // Alarm buzzer
sbit LMC   at LATD.B4;    // Microcontroller OK
sbit LPO   at LATD.B5;    // Motor at top end
sbit LNO   at LATD.B6;    // Motor at bottom end

// Alarm indicators

sbit LOF   at LATB.B0;    // Emergency stop
sbit LT    at LATB.B1;    // Temperature
sbit LLC   at LATB.B2;    // Load cell
sbit LWF   at LATB.B3;    // Water flow
sbit LL    at LATB.B4;    // Water leakage
sbit LS1T  at LATB.B5;    // Sigma 1 crash: top
sbit LS1B  at LATB.B6;    // Sigma 1 crash: bottom
sbit LS3   at LATB.B7;    // Sigma 3 crash

/*** Constants ****************************************************************/

const short ON  = 1;
const short OFF = 0;

const short WF_FLAG  = 0x01;
const short L_FLAG   = 0x02;
const short S1T_FLAG = 0x04;
const short S1B_FLAG = 0x08;
const short S3_FLAG  = 0x10;

/*** Function declarations ****************************************************/

void Config();
void Init();
void AllOff( short delay );
void MotorOff();
void WaitReset();
void Alarm( short state );