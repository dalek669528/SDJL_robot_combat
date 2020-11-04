void PWM_Calculate()
{
  
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



  if(control_type == 4){
    Position_PID();
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
