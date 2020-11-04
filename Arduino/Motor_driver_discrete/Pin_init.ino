void Pin_init(){
  //引脚功能初始化;
  pinMode(AD, INPUT);
  pinMode(EN, OUTPUT);
  pinMode(MotorA1, OUTPUT);
  pinMode(MotorA2, OUTPUT);
  pinMode(MotorB1, OUTPUT);
  pinMode(MotorB2, OUTPUT);
  pinMode(MotorC1, OUTPUT);
  pinMode(MotorC2, OUTPUT);
  pinMode(MotorD1, OUTPUT);
  pinMode(MotorD2, OUTPUT);

  pinMode(SPD_INT_A1, INPUT_PULLUP);
  pinMode(SPD_INT_A2, INPUT);
  pinMode(SPD_INT_B1, INPUT_PULLUP);
  pinMode(SPD_INT_B2, INPUT);
  pinMode(SPD_INT_C1, INPUT_PULLUP);
  pinMode(SPD_INT_C2, INPUT);
  pinMode(SPD_INT_D1, INPUT_PULLUP);
  pinMode(SPD_INT_D2, INPUT);
  
  
  //初始化TBN单/双路驱动
  digitalWrite(EN, 1);
  analogWrite(MotorA1, 0);
  analogWrite(MotorA2, 0);
  analogWrite(MotorB1, 0);
  analogWrite(MotorB2, 0);
  analogWrite(MotorC1, 0);
  analogWrite(MotorC2, 0);
  analogWrite(MotorD1, 0);
  analogWrite(MotorD2, 0);
  attachInterrupt(digitalPinToInterrupt(SPD_INT_A1), Encoder_A, RISING);
  attachInterrupt(digitalPinToInterrupt(SPD_INT_B1), Encoder_B, RISING);
  attachInterrupt(digitalPinToInterrupt(SPD_INT_C1), Encoder_C, RISING);
  attachInterrupt(digitalPinToInterrupt(SPD_INT_D1), Encoder_D, RISING);
}
