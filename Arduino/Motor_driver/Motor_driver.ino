#include "Wheel.h"
#include "Arm.h"

//定义引脚名称 
#define EN      A1  //使能输出引脚，该引脚时高电平才允许控制直流电机，低电平时电机停止
#define AD      A0  //PWM输入引脚，读取电池电压
#define MotorA1 8   //PWM输出引脚，控制直流电机A
#define MotorA2 13  //Dig输出引脚，控制直流电机A
#define MotorB1 9   //PWM输出引脚，控制直流电机B
#define MotorB2 12  //Dig输出引脚，控制直流电机B
#define MotorC1 10  //PWM输出引脚，控制直流电机C
#define MotorC2 11  //Dig输出引脚，控制直流电机C
#define MotorD1 6   //PWM输出引脚，控制直流电机D
#define MotorD2 7   //Dig输出引脚，控制直流电机D

#define SPD_INT_A1 18
#define SPD_INT_A2 14
#define SPD_INT_B1 19
#define SPD_INT_B2 15
#define SPD_INT_C1 20
#define SPD_INT_C2 16
#define SPD_INT_D1 21
#define SPD_INT_D2 17

#define SERVO1_PIN A2
#define SERVO2_PIN A3
#define SERVO3_PIN A4
#define SERVO4_PIN A5

#define INT_S1 2
#define INT_S2 3
#define Motor_S1 4
#define Motor_S2 5


Car car;
Arm arm;

int period = 50;
uint32_t timer;
uint32_t timer2;

void setup(){
  timer = millis();
  Pin_init();
  Serial.begin(115200);
  while (!Serial) {}  // wait for serial port to connect.
}

void loop() {
  timer2 = millis();
  if(timer2 >= timer + period){
    timer = (timer2/(period))*(period);
    Serial_rw();
    car.PWM_Calculate();
    arm.Routine();
    arm.Arm_Control();
  }
  car.Car_Control();
}
