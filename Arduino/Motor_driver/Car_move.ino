void Car::PWM_Calculate(){
  
  A.speed_renew(timer);
  B.speed_renew(timer);
  C.speed_renew(timer);
  D.speed_renew(timer);
  
  Vx = (-A.v + B.v - C.v + D.v)/4;
  Vy = (A.v + B.v + C.v + D.v)/4;
  w = (A.v + B.v - C.v - D.v)/(4*(W+L)) * 180 / PI;
  X += (-A.delta_x + B.delta_x - C.delta_x + D.delta_x)/4;
  Y += (A.delta_x + B.delta_x + C.delta_x + D.delta_x)/4;
  theta += ((A.delta_x + B.delta_x - C.delta_x - D.delta_x)/(4*(W+L))) * 180 / PI;
  if(theta>=360)
    theta -= 360;
  else if(theta < 0){
    theta += 360;
  }

  if(control_type >= 4){
    position_PID();
  }
  if(control_type >= 3){
    A.desire_V = - desire_Vx + desire_Vy + desire_w*(W+L);
    B.desire_V =   desire_Vx + desire_Vy + desire_w*(W+L);
    C.desire_V = - desire_Vx + desire_Vy - desire_w*(W+L);
    D.desire_V =   desire_Vx + desire_Vy - desire_w*(W+L);
  }
  if(control_type > 1){
    A.pwm_calculate();
    B.pwm_calculate();
    C.pwm_calculate();
    D.pwm_calculate();
  }
}

void Car::position_PID()
{
  pos_err[0] = desire_X - X;
  pos_err[1] = desire_Y - Y;

  pos_err_sum[0] += pos_err[0];
  pos_err_sum[1] += pos_err[1];
 
  desire_Vx = pos_err[0]*p_Kp + pos_err_sum[0]*p_Ki + (pos_err[0] - pos_err_past[0])*p_Kd;
  desire_Vy = pos_err[1]*p_Kp + pos_err_sum[1]*p_Ki + (pos_err[0] - pos_err_past[0])*p_Kd;

  pos_err_past[0] = pos_err[0];
  pos_err_past[1] = pos_err[1];


  if(abs(pos_err[0]) < 1 && abs(pos_err[1]) < 1){
    pos_err[2] = desire_theta - theta;
    if(pos_err[2]>180)
      pos_err[2] = 360 - pos_err[2];
    else if(pos_err[2] <= -180){
      pos_err[2] = 360 + pos_err[2];
    }
    pos_err_sum[2] += pos_err[2];
    desire_w  = (pos_err[2]*p_Kp + pos_err_sum[2]*p_Ki + (pos_err[0] - pos_err_past[0])*p_Kd) * PI / 180.0;
    pos_err_past[2] = pos_err[2];
  }
  else{
    desire_w = 0;
  }
  
}

void Car::Car_Control(){
  if(A.pwm < 0) { //反转
    analogWrite(MotorA1, 0); //MotorA1置0时电机反转
    analogWrite(MotorA2, (-A.pwm) > MAX_PWM ? MAX_PWM : (-A.pwm));
  }
  else { //正转
    analogWrite(MotorA1, A.pwm > MAX_PWM ? MAX_PWM : A.pwm);
    analogWrite(MotorA2, 0); //MotorA2置0时电机正转
  }
  
  if(B.pwm < 0) { //反转
    analogWrite(MotorB1, 0); //MotorB1置0时电机反转
    analogWrite(MotorB2, (-B.pwm) > MAX_PWM ? MAX_PWM : (-B.pwm));
  }
  else { //正转
    analogWrite(MotorB1, B.pwm > MAX_PWM ? MAX_PWM : B.pwm);
    analogWrite(MotorB2, 0); //MotorB2置0时电机正转
  }
  
  const int half_pwm = 128; 
  analogWrite(MotorC2, half_pwm); //MotorC1置0时电机反转
  if(C.pwm < 0) { //反转
    analogWrite(MotorC1, (half_pwm- ( (-C.pwm) > MAX_PWM ? MAX_PWM : (-C.pwm)) ) );
  }
  else { //正转
    analogWrite(MotorC1, C.pwm>MAX_PWM ? (MAX_PWM + half_pwm) : (C.pwm + half_pwm ));
  }

  if(D.pwm < 0) { //反转
    analogWrite(MotorD1, (half_pwm- ( (-D.pwm) > MAX_PWM ? MAX_PWM : (-D.pwm)) ) );
    analogWrite(MotorD2, (half_pwm- ( (-D.pwm) > MAX_PWM ? MAX_PWM : (-D.pwm)) ) );

  }
  else { //正转
    analogWrite(MotorD1, D.pwm>MAX_PWM ? (MAX_PWM + half_pwm) : (D.pwm + half_pwm ));
    analogWrite(MotorD2, D.pwm>MAX_PWM ? (MAX_PWM + half_pwm) : (D.pwm + half_pwm ));
  }
}
