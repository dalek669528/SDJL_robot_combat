void Serial_rw(){
  if (Serial.available() > 0) {
    String str = Serial.readStringUntil('\n');
    if(str != ""){
      char* c_str = str.c_str();
      int msg_type = atoi( strtok(c_str, " ") );
      String substr = strtok(NULL, "");
      switch (msg_type){
        case 0:
          arm.workType = 112;
          car.control_type = -2;
          car.car_reset();
          slide.reset();
        case 1: //Control pose
          car.Serial_r(substr);
          break;
        case 2: //Control arm
          arm.Serial_r(substr);
          break;
        case 3: //Control slide
          slide.Serial_r(substr);
          break;
        case 4:
          printInfo();
          break;
        case 5:
          car.print_info = !car.print_info;
          break;
        case 6:
          if(substr != "")
            arm.printInfo(substr.toInt());
          else
            arm.printInfo(-1);
          break;
        case 7:
          slide.print_info = !slide.print_info;
        default:
          car.past_control_type = car.control_type = -2;
          car.car_stop();
          break;
      }
    }
  }
}

void printInfo(){
    double V = analogRead(AD);
    Serial.print(timer);
    Serial.print(" ");
    Serial.print(V/18.21);
    Serial.print(" ");
    Serial.print(car.X);
    Serial.print(" ");
    Serial.print(car.Y);
    Serial.print(" ");
    Serial.print(car.theta);
    Serial.print(" ");
    Serial.print(arm.servo[0].now_angle);
    Serial.print(" ");
    Serial.print(arm.servo[1].now_angle);
    Serial.print(" ");
    Serial.print(arm.servo[2].now_angle);
    Serial.print(" ");
    Serial.print(arm.servo[3].now_angle);
    Serial.print(" ");
    Serial.print(slide.encoder);
    Serial.print("\n");
    
}
