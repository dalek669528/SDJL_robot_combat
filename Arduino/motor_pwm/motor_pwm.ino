#include <stdlib.h>
#include <string.h>


#define EN      2  //使能输出引脚，该引脚时高电平才允许控制直流电机，低电平时电机停止
#define MotorA1 3  //PWM输出引脚，控制直流电机A
#define AD      A0 //PWM输入引脚，读取电池电压
#define MotorA2 5  //PWM输出引脚，控制直流电机A
#define MotorB1 6  //PWM输出引脚，控制直流电机B
#define MotorB2 9  //PWM输出引脚，控制直流电机B 
#define MotorC1 10 //PWM输出引脚，控制直流电机C
#define MotorC2 11 //PWM输出引脚，控制直流电机C
#define MotorD1 12 //数字输出引脚，由于ArduinoUNO主板上的PWM输出引脚有限，
#define MotorD2 13 //故只能使用数字输出引脚通过手动设置占空比控制直流电机D，缺点是控制效果较差


void setup() {

  Serial.begin(9600);  //設定通訊速率

  //引脚功能初始化
  pinMode(EN, OUTPUT);
  pinMode(MotorA1, OUTPUT);
  pinMode(MotorA2, OUTPUT);
  pinMode(MotorB1, OUTPUT);
  pinMode(MotorB2, OUTPUT);
  pinMode(MotorC1, OUTPUT);
  pinMode(MotorC2, OUTPUT);
  pinMode(MotorD1, OUTPUT);
  pinMode(MotorD2, OUTPUT);
  pinMode(AD, INPUT);

  //初始化TBN单/双路驱动
  digitalWrite(EN, 1); 
  analogWrite(MotorA1, 0);
  analogWrite(MotorA2, 0);
  analogWrite(MotorB1, 0);
  analogWrite(MotorB2, 0);
  analogWrite(MotorC1, 0);
  analogWrite(MotorC2, 0);
  digitalWrite(MotorD1, 0);
  digitalWrite(MotorD2, 0);
  
}

void SetPowerA(int direction, int power)
{
  int pwm=255*power/100; //输出到模拟引脚的PWM信号范围为0~255
  if(direction==1) //正转
  {
   analogWrite(MotorA1, 0); //MotorA1置0时电机正转
   analogWrite(MotorA2, pwm); 
  }
  else if(direction==0) //反转
  {
   analogWrite(MotorA1, pwm);
   analogWrite(MotorA2, 0); //MotorA2置0时电机反转
  }
}

void SetPowerB(int direction, int power)
{
  int pwm=255*power/100; //输出到模拟引脚的PWM信号范围为0~255
  if(direction==1) //正转
  {
   analogWrite(MotorB1, 0); //MotorB1置0时电机正转
   analogWrite(MotorB2, pwm);
  }
  else if(direction==0) //反转
  {
   analogWrite(MotorB1, pwm);
   analogWrite(MotorB2, 0); //MotorB2置0时电机反转
  }
}

void SetPowerC(int direction, int power)
{
  int pwm=255*power/100; //输出到模拟引脚的PWM信号范围为0~255
  if(direction==1) //正转
  {
   analogWrite(MotorC1, 0); //MotorC1置0时电机正转
   analogWrite(MotorC2, pwm);
  }
  else if(direction==0) //反转
  {
   analogWrite(MotorC1, pwm);
   analogWrite(MotorC2, 0); //MotorC2置0时电机反转
  }
}

void SetPowerD(int direction, int power)
{
  if(direction==1) //正转
  {
    for(int i=0;i<1000;i++)
    {
     digitalWrite(MotorD1, 0); //MotorD1置0时电机正转
     digitalWrite(MotorD2, 1);
     delayMicroseconds(power*100); //保持高电平power*100微秒
     digitalWrite(MotorD2, 0);
     delayMicroseconds(10000-power*100); //保持低电平电平（10000-power*100）微秒
    }
  }
  else if(direction==0) //反转
  {
    for(int i=0;i<1000;i++)
    {
     digitalWrite(MotorD2, 0); //MotorD2置0时电机正转
     digitalWrite(MotorD1, 1);
     delayMicroseconds(power); //保持高电平power*100微秒
     digitalWrite(MotorD1, 0);
     delayMicroseconds(100-power); //保持低电平电平（10000-power*100）微秒
    }
  }
}

void loop() {

while (!Serial.available()) {}   //直到暫存器出現訊號才跳出迴圈

//Serial.write(Serial.read());  //傳輸讀取的訊號

  while (Serial.available()>0) {   //如果暫存器有訊號則不斷讀取直到沒有
  
  String s=Serial.readString();
  char* s_c = s.c_str();
  int error[4];
  int error_past[4];
  int counter=0;
  
  if(s!=""){
  
    char *substr = NULL;
    
    substr = strtok(s_c," ");
          
    do{
      
      int x=atoi(substr);
      error[counter]=x;
      
      Serial.println(x);
      
      substr = strtok(NULL," ");

      counter++;
    }while(substr);

   }
  for(int i=0;i<4;i++){
    error_past[i]=error[i];
    Serial.println(error_past[i]);  
  }
  }

  SetPowerA(1, 50); //ABCD电机50%功率正转
  SetPowerB(1, 50);
  SetPowerC(1, 50);
  SetPowerD(1, 50);
  delay(100); //直流电机正转3s


}
