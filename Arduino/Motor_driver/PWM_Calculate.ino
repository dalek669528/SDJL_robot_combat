void PWM_Calculate()
{
  A.speed_cal();
  B.speed_cal();
  C.speed_cal();
  D.speed_cal();



  
//  double deg_L = (encoderPosL - encoderL_past) / CPR * PI * 2 * TIRE_RADIUS;
//  double deg_R = (encoderPosR - encoderR_past) / CPR * PI * 2 * TIRE_RADIUS;
//  Speed_L = (encoderPosL - encoderL_past)/CPR*PI*2*TIRE_RADIUS/(millis()-SpeedTimer)*1000; //cm/sec
//  Speed_R = (encoderPosR - encoderR_past)/CPR*PI*2*TIRE_RADIUS/(millis()-SpeedTimer)*1000; //cm/sec
//  SpeedTimer = millis();
//  encoderR_past = encoderPosR;
//  encoderL_past = encoderPosL;
  
  double deg_LR = (deg_L + deg_R) * 0.5;
  Speed_LR = (Speed_L + Speed_R) * 0.5;
//    
  Speed_Diff = Speed_L - Speed_R;
  Speed_Diff_ALL += Speed_Diff;
//
  double temp;
  double Pt = 0, It = 0, Dt = 0;
  double Pt_p = 0, It_p = 0, Dt_p = 0;
//  
//  car_position += Speed_LR * (micros() - angle_dt) * 0.000001;
//  //手機 速度控制 加速度設上限
//  if(Speed_Need - Speed_LR > 0) {
//    Position_Temp = (Speed_Need - Speed_LR)/40;
//  }
//  else if(Speed_Need - Speed_LR < -40) {
//    Position_Temp = (Speed_Need - Speed_LR)/20;
//  }
//  
//  while (Last_Turn_Need - Turn_Need > 180) {
//    Turn_Need -= 360;
//  }
//  while (Last_Turn_Need - Turn_Need < -180) {
//    Turn_Need += 360;
//  }
// 
//  //直線 
//  double encoderError = (encoderPosL - encoderPosR);
//  
//  // 位置控制
//  // Car Position
//  Pt_p = KP_P * (Position_Temp);
//  It_p = KP_I * car_position_int;
//  Dt_p = KP_D * Speed_LR;
//  car_position_int += (car_position)*(micros()-angle_dt)*0.000001;
//  
//  // 角度控制
//  Pt = -KA_P * (Pt_p - Angle_Car + ANG_OFFSET);
//  It = -KA_I * (Et_total + It_p);
//  Dt = KA_D * (Gyro_Car - Dt_p);
//  Et_total += (Pt_p - Angle_Car + ANG_OFFSET) * (micros() - angle_dt) * 0.000001; // 單位換算:micros --> sec
//  if (Et_total > 1.3)
//    Et_total = 1.3;
//  else if (Et_total < -1.3)
//    Et_total = -1.3;
//    
//  double P_wheel = 0, I_wheel = 0;
//  Et_wheel += encoderError*(micros()-angle_dt)*0.000001;
//  P_wheel = 3*encoderError;
//  I_wheel = 1.5*Et_wheel;
//  
//  angle_dt = micros();
//  
//  temp = int(P_wheel + I_wheel);
//  
//  pwm = int(Pt+It+Dt);
//  
//  turn = (45-abs(Turn_Need))*0.012;
//
//  if(turn<0.1&&turn>-0.1){
//    pwm_r = (pwm+temp);
//    pwm_l = (pwm-temp);
//  }
//  else{
//    pwm_r = (pwm)*(1-turn);
//    pwm_l = (pwm)*(1+turn);
//    Et_wheel = 0;
//    encoderError = 0;
//    encoderPosL = 0;
//    encoderPosR = 0;
//  }
//    
//    //Serial.println(pwm);
//    //Speed_Need  //Turn_Need
//
}
