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

  pinMode(Motor_S1, OUTPUT);
  pinMode(Motor_S2, OUTPUT);
  pinMode(INT_S1, INPUT_PULLUP);
  pinMode(INT_S2, INPUT);
  
  pinMode(SERVO1_PIN, OUTPUT);
  pinMode(SERVO2_PIN, OUTPUT);
  pinMode(SERVO3_PIN, OUTPUT);
  pinMode(SERVO4_PIN, OUTPUT);

  pinMode(button, INPUT);
  pinMode(Gnd, OUTPUT);
  pinMode(Vcc, OUTPUT);
  digitalWrite(Vcc, HIGH);
  digitalWrite(Gnd, LOW);

  
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

  analogWrite(Motor_S1, 0);
  analogWrite(Motor_S2, 0);
  attachInterrupt(digitalPinToInterrupt(INT_S1), Encoder_S1, RISING);
//  attachInterrupt(digitalPinToInterrupt(INT_S2), Encoder_S2, RISING);
}
