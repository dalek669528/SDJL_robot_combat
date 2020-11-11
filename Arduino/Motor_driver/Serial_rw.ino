void Serial_rw(){
  if (Serial.available() > 0) {
    String str = Serial.readStringUntil('\n');
    if(str != ""){
      char* c_str = str.c_str();
      int msg_type = atoi( strtok(c_str, " ") );
      String substr = strtok(NULL, "");
      switch (msg_type){
        case 1:
          car.Serial_r(substr);
          break;
        case 2:
          arm.Serial_r(substr);
          break;
        case 3:
          car.printInfo();
          break;
        case 4:
          car.printInfo();
          break;
        default:
          car.past_control_type = car.control_type = -2;
          car.car_stop();
          break;
      }
    }
  }
}
void Car::Serial_r(String str){
  reset_err();
  
  if(str.indexOf(' ') != -1){
    control_type = 0;
    control_type = (str.substring(0,str.indexOf(' '))).toInt();
    str = str.substring(str.indexOf(' ')+1);
    switch(control_type){
      case 1:
        A.pwm = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        B.pwm = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        C.pwm = (str.substring(0,str.indexOf(' '))).toInt();
        D.pwm = (str.substring(str.indexOf(' ')+1)).toInt();
        break;
      case 2:
        A.desire_V = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        B.desire_V = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        C.desire_V = (str.substring(0,str.indexOf(' '))).toInt();
        D.desire_V = (str.substring(str.indexOf(' ')+1)).toInt();
        break;
      case 3:
        desire_Vx = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        desire_Vy = (str.substring(0,str.indexOf(' '))).toInt();
        desire_w = (str.substring(str.indexOf(' ')+1)).toInt() * PI / 180.0;
        break;
      case 4:
        desire_X = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        desire_Y = (str.substring(0,str.indexOf(' '))).toInt();
        desire_theta = (str.substring(str.indexOf(' ')+1)).toInt();
        break;
      case 5:
        desire_X += (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        desire_Y += (str.substring(0,str.indexOf(' '))).toInt();
        desire_theta += (str.substring(str.indexOf(' ')+1)).toInt();  
        if(desire_theta>=360)
          desire_theta -= 360;
        else if(desire_theta < 0)
          desire_theta += 360;
        break;
      case -1:
        int changePID, p, i, d; 
        changePID = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        p = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        i = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        d = (str.substring(str.indexOf(' ')+1)).toInt();
        switch(changePID){
          case 0:
            A.set_PID(p, i, d);
            break;
          case 1:
            B.set_PID(p, i, d);
            break;
          case 2:
            C.set_PID(p, i, d);
            break;
          case 3:
            D.set_PID(p, i, d);
            break;
          case 4:
            p_Kp = p;
            p_Ki = i;
            p_Kd = d;
            break;
        }
        control_type = past_control_type;
      default:
        control_type = -2;
        car_reset();
    }
    past_control_type = control_type;
  }
  else{
    past_control_type = control_type = -2;
    car_stop();
  }
}
  
void Car::printInfo(){
  double V = analogRead(AD);
  Serial.print(timer);
  Serial.print(" ");
  Serial.print(V/18.21);
  Serial.print("V ");
  Serial.print(control_type);
  Serial.print(" ");

  Serial.print(X);
  Serial.print(" ");
  Serial.print(Y);
  Serial.print(" ");
  Serial.print(theta);
  Serial.print(" cm ");
//  Serial.print(Vx);
//  Serial.print(" ");
//  Serial.print(Vy);
//  Serial.print(" ");
//  Serial.print(w);
//  Serial.print(" cm/s ");
  Serial.print(A.v);
  Serial.print(" ");
//  Serial.print(A.desire_V);
//  Serial.print(" ");
  Serial.print(B.v);
  Serial.print(" ");
//  Serial.print(B.desire_V);
//  Serial.print(" ");
  Serial.print(C.v);
  Serial.print(" ");
//  Serial.print(C.desire_V);
//  Serial.print(" ");
  Serial.print(D.v);
  Serial.print(" ");
//  Serial.print(D.desire_V);
  Serial.print(" cm/s ");
//  Serial.print(A.encoder);
//  Serial.print(" ");
//  Serial.print(B.encoder);
//  Serial.print(" ");
//  Serial.print(C.encoder);
//  Serial.print(" ");
//  Serial.print(D.encoder);
  Serial.print("\n");
}
