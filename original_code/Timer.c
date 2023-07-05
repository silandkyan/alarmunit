/******************************************************************************/
/* Timer                                                                      */
/*                                                                            */
/*    Author         Eric Reusser                                             */
/*    Version        1.0                                                      */
/*    Creation date  06/2017                                                  */
/*    Version date   06/2017                                                  */
/*----------------------------------------------------------------------------*/
/* Timer utility: Timer 1, Timer 3, Timer 5 (16 bit timers)                   */
/******************************************************************************/

#include "Timer.h"

/*** Constants ****************************************************************/

const unsigned int MAX_DELAY_1 = 5;      // 5 sec  (Max. value: 60 sec)
const unsigned int MAX_DELAY_3 = 20;     // 20 sec (Max. value: 60 sec)
const unsigned int MAX_DELAY_5 = 10;     // 10 min (Max. value: 60 min)

/*** Local functions **********************************************************/

void Reset_Timer_1();
void Reset_Timer_3();
void Reset_Timer_5();

/*** Variables ****************************************************************/

unsigned int delay_1;
unsigned int delay_3;
unsigned int delay_5;

unsigned int timer1_cnt = 0;
unsigned int timer3_cnt = 0;
unsigned int timer5_cnt = 0;

/*** Timer interrupt routine **************************************************/

void interrupt()
{
     if ( TMR1IF_bit )
     {
          timer1_cnt++;
          Reset_Timer_1();
     }
     if ( TMR3IF_bit )
     {
          timer3_cnt++;
          Reset_Timer_3();
     }
     if ( TMR5IF_bit )
     {
          timer5_cnt++;
          Reset_Timer_5();
     }
}

/*** Timer routines ***********************************************************/

void InitTimers()
{
     T1CON = 0x30;    // Timer 1: Clock = fosc/4, Prescaler = 1:8
     T3CON = 0x30;    // Timer 3: Clock = fosc/4, Prescaler = 1:8
     T5CON = 0x30;    // Timer 5: Clock = fosc/4, Prescaler = 1:8

     TMR1IE_bit = 1;  // Timer 1 interrupt enable
     TMR3IE_bit = 1;  // Timer 3 interrupt enable
     TMR5IE_bit = 1;  // Timer 5 interrupt enable
     INTCON = 0xC0;   // General interrupt enable

     // Reading analog channels, converting to delay times

     delay_1 = MAX_DELAY_1 * ADC_Read( 0 );
     delay_3 = MAX_DELAY_3 * ADC_Read( 1 );
     delay_5 = MAX_DELAY_5 * ADC_Read( 2 );

     Reset_Timer_1();
     Reset_Timer_3();
     Reset_Timer_5();
}

// Timer on/off routines

void Timer_1( short state )
{
     if ( state )
     {
          TMR1ON_bit = 1;
     }
     else
     {
          TMR1ON_bit = 0;
          Reset_Timer_1();
          timer1_cnt = 0;
     }
}

void Timer_3( short state )
{
     if ( state )
     {
          TMR3ON_bit = 1;
     }
     else
     {
          TMR3ON_bit = 0;
          Reset_Timer_3();
          timer3_cnt = 0;
     }
}
void Timer_5( short state )
{
     if ( state )
     {
          TMR5ON_bit = 1;
     }
     else
     {
          TMR5ON_bit = 0;
          Reset_Timer_5();
          timer5_cnt = 0;
     }
}

// Timer check routines

short Check_Timer_1()
{
      if ( timer1_cnt >= delay_1 )
      {
           timer1_cnt = 0;
           return 1;
      }
      return 0;
}

short Check_Timer_3()
{
      if ( timer3_cnt >= delay_3 )
      {
           timer3_cnt = 0;
           return 1;
      }
      return 0;
}

short Check_Timer_5()
{
      if ( timer5_cnt >= delay_5 )
      {
           timer5_cnt = 0;
           return 1;
      }
      return 0;
}

// Timer reset and timing control

// TMR1 = 0xFF05 (65285) -> Tp = 1ms (1kHz)

void Reset_Timer_1()
{
     TMR1IF_bit = 0;
     TMR1H = 0xFF;
     TMR1L = 0x05;
}

// TMR3 = 0xFF05 (65285) -> Tp = 1ms (1kHz)

void Reset_Timer_3()
{
     TMR3IF_bit = 0;
     TMR3H = 0xFF;
     TMR3L = 0x05;
}

// TMR5 = 0xC667 (50535) -> Tp = 60ms (16.7Hz)

void Reset_Timer_5()
{
     TMR5IF_bit = 0;
     TMR5H = 0xC5;
     TMR5L = 0x67;
}