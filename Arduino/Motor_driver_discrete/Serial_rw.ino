void Serial_rw(){
  if (Serial.available() > 0) {
    String str = Serial.readStringUntil('\n');
    
    A.reset_error();
    B.reset_error();
    C.reset_error();
    D.reset_error();
    pos_err[0] = pos_err[1] = pos_err[2] = 0;
    pos_err_past[0] = pos_err_past[1] = pos_err_past[2] = 0;
    pos_err_sum[0] = pos_err_sum[1] = pos_err_sum[2] = 0;
    
    if(str.indexOf(' ') != -1){
      control_type = 0;
      control_type = (str.substring(0,str.indexOf(' '))).toInt();
      str = str.substring(str.indexOf(' ')+1);
      
      if(control_type == 1){
        A.pwm = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        B.pwm = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        C.pwm = (str.substring(0,str.indexOf(' '))).toInt();
        D.pwm = (str.substring(str.indexOf(' ')+1)).toInt();
      }
      else if (control_type == 2){
        A.desire_V = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        B.desire_V = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        C.desire_V = (str.substring(0,str.indexOf(' '))).toInt();
        D.desire_V = (str.substring(str.indexOf(' ')+1)).toInt();
      }
      else if (control_type == 3){
        desire_Vx = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        desire_Vy = (str.substring(0,str.indexOf(' '))).toInt();
        desire_w = (str.substring(str.indexOf(' ')+1)).toInt();
      }
      else if (control_type == 4){
        desire_X = (str.substring(0,str.indexOf(' '))).toInt();
        str = str.substring(str.indexOf(' ')+1);
        desire_Y = (str.substring(0,str.indexOf(' '))).toInt();
        desire_theta = (str.substring(str.indexOf(' ')+1)).toInt();
        desire_theta = desire_theta * PI / 180.0;
      }
      else{
        control_type = -1;
        A.desire_V = B.desire_V = C.desire_V = D.desire_V = 0;
        X = Y = theta = 0;
      }
    }
    else{
      control_type = -1;
      A.desire_V = B.desire_V = C.desire_V = D.desire_V = 0;
    }
  }




  double V=analogRead(AD);
//  Serial.print(timer);
  Serial.print(millis());
  Serial.print(" ");
  Serial.print(V/18.21);
  Serial.print("V ");


  if(control_type == 1){
    Serial.print(A.encoder);
    Serial.print(" ");
    Serial.print(B.encoder);
    Serial.print(" ");
    Serial.print(C.encoder);
    Serial.print(" ");
    Serial.print(D.encoder);
    Serial.print("\n");
  }
  else if(control_type == 2){
    Serial.print(A.v);
    Serial.print(" ");
    Serial.print(B.v);
    Serial.print(" ");
    Serial.print(C.v);
    Serial.print(" ");
    Serial.print(D.v);
    Serial.print("  cm/s\n");    
  }
    else if(control_type == 3){
    Serial.print(Vx);
    Serial.print(" ");
    Serial.print(Vy);
    Serial.print(" ");
    Serial.print(w);
    Serial.print("  cm/s\n");    
  }
  else{
    Serial.print(X);
    Serial.print(" ");
    Serial.print(Y);
    Serial.print(" ");
    Serial.print(theta *180.0 / PI);
    Serial.print(" cm\n");
  }


  
}
