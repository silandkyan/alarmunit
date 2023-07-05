/******************************************************************************/
/* Griggs alarm unit                                                          */
/*                                                                            */
/*    Author         Eric Reusser                                             */
/*    Version        1.1                                                      */
/*    Release        3                                                        */
/*    Creation date  05/2017                                                  */
/*    Version date   07/2017                                                  */
/*----------------------------------------------------------------------------*/
/* Griggs_Alarm: PIC C Program                                                */
/******************************************************************************/

#include "GriggsAlarm.h"
#include "Timer.h"

/*** Global variables *********************************************************/

short T3_flag = 0x00;

/*** Main program *************************************************************/

void main()
{
     Config();
     Init();
     InitTimers();
     
     while ( 1 )
     {
          // All alarms OFF
          
          if ( AOF )
          {
               Init();
               T3_flag = 0x00;
               Timer_3( OFF );
               Timer_5( OFF );
               while ( AOF )
               {
                    if ( !NOF ) break;
                    if ( !T )   LT   = ON;
                    else        LT   = OFF;
                    if ( !LC )  LLC  = ON;
                    else        LLC  = OFF;
                    if ( !WF )  LWF  = ON;
                    else        LWF  = OFF;
                    if ( L )    LL   = ON;
                    else        LL   = OFF;
                    if ( S1T )
                    {
                                LS1T = ON;
                                LPO  = ON;
                    }
                    else
                    {
                                LS1T = OFF;
                                LPO  = OFF;
                    }
                    if ( S1B )
                    {
                                LS1B = ON;
                                LNO  = ON;
                    }
                    else
                    {
                                LS1B = OFF;
                                LNO  = OFF;
                    }
                    if ( S3 )   LS3  = ON;
                    else        LS3  = OFF;
               }
               if ( NOF ) Init();
          }

          // Emergency stop or Temperature or Load cell (!NOF, !T, !LC)
          
          if ( !NOF || !T || !LC )
          {
               if ( !NOF ) { LOF = ON; }
               if ( !T )   { LT  = ON; }
               if ( !LC )  { LLC = ON; }
               AllOff( ON );
          }
 
          // Water flow (!WF)
          
          if ( !WF )
          {
               LWF = ON;
               if ( !T3_flag )
               {
                    Timer_3( ON );
                    T3_flag = WF_FLAG;
               }
               if ( T3_flag == WF_FLAG )
               {
                    if ( Check_Timer_3() )
                    {
                         Timer_3( OFF );
                         AllOff( OFF );
                    }
               }
          }
          if ( WF )
          {
               LWF = OFF;
               if ( T3_flag == WF_FLAG )
               {
                    Timer_3( OFF );
                    T3_flag = 0x00;
               }
          }

          // Water leakage
                 
          if ( L )
          {
               LL = ON;
               if ( !T3_flag )
               {
                    Timer_3( ON );
                    T3_flag = L_FLAG;
               }
               if ( T3_flag == L_FLAG )
               {
                    if ( Check_Timer_3() )
                    {
                         Timer_3( OFF );
                         AllOff( OFF );
                    }
               }
          }
          if ( !L )
          {
               LL = OFF;
               if ( T3_flag == L_FLAG )
               {
                    Timer_3( OFF );
                    T3_flag = 0x00;
               }
          }

          // Sigma 1 top
               
          if ( S1T )
          {
               LS1T = ON;
               LPO  = ON;
               if ( !T3_flag )
               {
                    Timer_3( ON );
                    T3_flag = S1T_FLAG;
               }
               if ( T3_flag == S1T_FLAG )
               {
                    if ( Check_Timer_3() )
                    {
                         Timer_3( OFF );
                         AllOff( ON );
                    }
               }
          }
          if ( !S1T )
          {
               LS1T = OFF;
               LPO  = OFF;
               if ( T3_flag == S1T_FLAG )
               {
                    Timer_3( OFF );
                    T3_flag = 0x00;
               }
          }

          // Sigma 1 bottom

          if ( S1B )
          {
               LS1B = ON;
               LNO  = ON;
               if ( !T3_flag )
               {
                    Timer_3( ON );
                    T3_flag = S1B_FLAG;
               }
               if ( T3_flag == S1B_FLAG )
               {
                    if ( Check_Timer_3() )
                    {
                         Timer_3( OFF );
                         AllOff( ON );
                    }
               }
          }
          if ( !S1B )
          {
               LS1B = OFF;
               LNO  = OFF;
               if ( T3_flag == S1B_FLAG )
               {
                    Timer_3( OFF );
                    T3_flag = 0x00;
               }
          }

          // Sigma 3

          if ( S3 )
          {
               LS3 = ON;
               if ( !T3_flag )
               {
                    Timer_3( ON );
                    T3_flag = S3_FLAG;
               }
               if ( T3_flag == S3_FLAG )
               {
                    if ( Check_Timer_3() )
                    {
                         Timer_3( OFF );
                         AllOff( ON );
                    }
               }
          }
          if ( !S3 )
          {
               LS3 = OFF;
               if ( T3_flag == S3_FLAG )
               {
                    Timer_3( OFF );
                    T3_flag = 0x00;
               }
          }
      }
}

void Config()
{
     // Port configuration A[0..2] = analog, all others digital

     ANSELA = 0x07;
     ANSELB = 0x00;
     ANSELC = 0x00;
     ANSELD = 0x00;
     ANSELE = 0x00;

     // Port digital I/O configuration

     TRISA = 0x3F;   // A[0..5] input
     TRISB = 0x00;   // B[0..7] output
     TRISC = 0x0F;   // C[0..3] input, C[4..7] output
     TRISD = 0x03;   // D[0..1] input, D[3..6] output, D[2,7] not used
     TRISE = 0x07;   // E[0..2] input
}

void Init()
{
     // Output ports: initial values

     LATB  = 0x00;   // All alarms off
     LATC  = 0xF0;   // All controls enabled
     LATD  = 0x10;   // All alarms off, Microcontroller OK
}

void AllOff( short delay )
{
     Alarm( ON );
     THY = OFF;
     if ( delay )
     {
          Timer_5( ON );
          MotorOff();
          while( !Check_Timer_5() ) {}
          Timer_5( OFF );
          WOK = OFF;
     }
     else
     {
          WOK = OFF;
          MotorOff();
     }
     WaitReset();
}

void MotorOff()
{
     MOK = OFF;
     Timer_1( ON );
     while ( !Check_Timer_1() ) {}
     MEN = OFF;
     Timer_1( OFF );
}

void WaitReset()
{
     LMC = OFF;
     while( 1 ) {}
}

void Alarm( short state )
{
     if ( state == ON )
     {
          ALR = ON;
          return;
     }
     ALR = OFF;
}