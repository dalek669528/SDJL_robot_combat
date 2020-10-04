//////////////////TBN四路驱动引脚接线///////////////////////////
//电机-------------TBN四路驱动丝印标识----------ArduinoUNO主板引脚
//电机-------------DATA_ABC牛角座-----------ArduinoUNO主板引脚
//                     EN(使能)------------10
//                     5V-----------------5V
//                     AD-----------------A0
//                     G------------------GND
//                     A1-----------------6
//                     A2-----------------7
//                     B1-----------------9
//                     B2-----------------8
//直流电机A-------------MotorA
//直流电机B-------------MotorB
//电机-------------TBN四路驱动丝印标识----------ArduinoUNO主板引脚

#include "wheel.h"

//定义引脚名称 
#define EN      13  //使能输出引脚，该引脚时高电平才允许控制直流电机，低电平时电机停止
#define AD      A0  //PWM输入引脚，读取电池电压
#define MotorA1 12  //PWM输出引脚，控制直流电机A
#define MotorA2 11  //Dig输出引脚，控制直流电机A
#define MotorB1 10  //PWM输出引脚，控制直流电机B
#define MotorB2 9   //Dig输出引脚，控制直流电机B
#define MotorC1 8   //PWM输出引脚，控制直流电机C
#define MotorC2 7   //Dig输出引脚，控制直流电机C
#define MotorD1 6   //PWM输出引脚，控制直流电机D
#define MotorD2 5   //Dig输出引脚，控制直流电机D

#define SPD_INT_A1 3
#define SPD_INT_A2 4
#define SPD_INT_B1 2
#define SPD_INT_B2 14
#define SPD_INT_C1 18
#define SPD_INT_C2 17
#define SPD_INT_D1 19
#define SPD_INT_D2 20

#define CPR = 390 //count per round
#define TIRE_RADIUS = 3 //3cm

Wheel A(50), B(50), C(50), D(50);

//double ANG_OFFSET;
//double Et_total;
//double Dt_total;

//uint32_t timer;
//uint32_t angle_dt;
uint32_t SendTimer;
//uint32_t ReceiveTimer;
//uint32_t SendToPCTimer;
//uint32_t SpeedTimer;
//uint32_t StopTimer;

void setup() {
//  timer = micros();
//  angle_dt = micros();
//  SendTimer = millis();
//  ReceiveTimer = millis();
//  SendToPCTimer = millis();
//  SpeedTimer = millis();
//  StopTimer = millis();
  Pin_init();
  Serial.begin(115200);
  while (!Serial) {}  // wait for serial port to connect.
}

void loop() {
  Serial_rw();
  PWM_Calculate();
  Car_Control();
}
