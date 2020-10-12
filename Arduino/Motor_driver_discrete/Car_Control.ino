void Car_Control(){
  int pwm_temp;
  if(A.pwm < 0) { //反转
    pwm_temp = -A.pwm;
    analogWrite(MotorA2, 0); //MotorA1置0时电机反转
    analogWrite(MotorA1, pwm_temp>MAX_PWM? MAX_PWM:pwm_temp);
  }
  else { //正转
    analogWrite(MotorA2, A.pwm>MAX_PWM? MAX_PWM:A.pwm);
    analogWrite(MotorA1, 0); //MotorA2置0时电机正转
  }
  
  if(B.pwm < 0) { //反转
    pwm_temp = -B.pwm;
    analogWrite(MotorB1, 0); //MotorB1置0时电机反转
    analogWrite(MotorB2, pwm_temp>MAX_PWM? MAX_PWM:pwm_temp);
  }
  else { //正转
    analogWrite(MotorB1, B.pwm>MAX_PWM? MAX_PWM:B.pwm);
    analogWrite(MotorB2, 0); //MotorB2置0时电机正转
  }
  
  if(C.pwm < 0) { //反转
    pwm_temp = -C.pwm;
    analogWrite(MotorC2, 0); //MotorC1置0时电机反转
    analogWrite(MotorC1, pwm_temp>MAX_PWM? MAX_PWM:pwm_temp);
  }
  else { //正转
    analogWrite(MotorC2, C.pwm>MAX_PWM? MAX_PWM:C.pwm);
    analogWrite(MotorC1, 0); //MotorC2置0时电机正转
  }
  
  if(D.pwm < 0) { //反转
    pwm_temp = -D.pwm;
    analogWrite(MotorD1, 0); //MotorD1置0时电机反转
    analogWrite(MotorD2, pwm_temp>MAX_PWM? MAX_PWM:pwm_temp);
  }
  else { //正转
    analogWrite(MotorD1, D.pwm>MAX_PWM? MAX_PWM:D.pwm);
    analogWrite(MotorD2, 0); //MotorD2置0时电机正转
  }
}
