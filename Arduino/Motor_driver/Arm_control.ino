void Arm::Serial_r(String str) {
  char* intput_string_c = str.c_str();
  int idx = 0;
  SERVO_SPEED = 20;
  if (str != "") {
    workType = atoi( strtok(intput_string_c, " ") );
    switch(workType){
      case 121:
        for(int i=0; i<4; i++)
          serial_Angle_array[i] = atof(strtok(NULL, " "));
        break;
      case 122:
        for(int i=0; i<4; i++)
          serial_Angle_array[i] = servo[i].now_angle;
        idx = atoi(strtok(NULL, " "));
        if(idx != -1){
          SERVO_SPEED = SERVO_SPEED * atof(strtok(NULL, " "));
          serial_Angle_array[idx] = ( (atoi(strtok(NULL, " "))?180:0  ) - SERVO_OFFSET[idx]) * SERVO_POSITIVE[idx]; 
        }
        break;
        
      case 221:
        for(int i=0; i<2; i++)
          pointYZ[i]=atof(strtok(NULL," "));
        if(pointYZ[0] > ARM_PICK_LOWER_BOUND && pointYZ[0] < ARM_PICK_UPPER_BOUND){
          float YZ_angle[4];
          movetoPoint(0, 30, pointYZ, YZ_angle);
          reset_motion();
          for(int i = 0 ; i < 4 ; i++){
             motion_array[0][i] = YZ_angle[i];
          }
          motion_array[0][4] = 1;
          for(int i = 0 ; i < 3 ; i++){
             motion_array[1][i] = YZ_angle[i];
          }
          motion_array[1][3] = 60;
          motion_array[1][4] = -1;
          
          for(int i = 0 ; i < 4 ; i++){
             motion_array[2][i] = SERVO_PICKUP_STATE[i];
          }
          motion_array[2][4] = 0;
        }
        break;
      case 222:
        for(int i=0; i<2; i++)
          pointYZ[i]=atof(strtok(NULL," "));    
        if(pointYZ[0] > ARM_PICK_LOWER_BOUND && pointYZ[0] < ARM_PICK_UPPER_BOUND){
          float YZ_angle[4];
          movetoPoint(60, 60, pointYZ, YZ_angle);
          reset_motion();
          for(int i = 0 ; i < 4 ; i++){
             motion_array[0][i] = YZ_angle[i];
          }
          motion_array[0][4] = 1;
          for(int i = 0 ; i < 3 ; i++){
             motion_array[1][i] = YZ_angle[i];
          }
          motion_array[1][3] = 30;
          motion_array[1][4] = -1;
          for(int i = 0 ; i < 4 ; i++){
             motion_array[2][i] = SERVO_READY_STATE[i];
          }
          motion_array[2][4] = 0;
        }
        break;
    }
  }
}


void Arm::printInfo(int servo_index) {
  int start_idx = 0, end_idx = 4;
  if(servo_index != -1){
    start_idx = servo_index;
    servo_index = start_idx + 1;
  }    
  for(servo_index = start_idx ; servo_index < end_idx ; servo_index++){
    Serial.print("Motor ");
    Serial.print(servo_index);
    Serial.print(" angle desire : ");
    Serial.print(servo[servo_index].desire_angle);
    Serial.print("/");
    Serial.print(servo[servo_index].now_angle);
    Serial.print(" pwm desire : ");
    Serial.print(servo[servo_index].pwm_desire);
    Serial.print(" / ");
    Serial.print(servo[servo_index].pwm_past);
    Serial.print(" stable : ");
    Serial.print(servo[servo_index].is_stable());
    Serial.print(" enable : ");
    Serial.println(servo[servo_index].enable);
  }
  Serial.print("\n");
}



bool Arm::movetoPoint(float angle_first, float angle_final, float point[], float desireAngle_array[]) {

  float y_reference = point[0] - SERVO_LENGTH[0] * cos(angle_first / 180 * PI) + ARM_AXIS_OFFSET;
  float z_reference = point[1] - SERVO_LENGTH[0] * sin(angle_first / 180 * PI);

  desireAngle_array[0] = angle_first ;
  desireAngle_array[1] = -desireAngle_array[0] + atan(z_reference / y_reference) / M_PI * 180 + acos((pow(SERVO_LENGTH[1], 2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2)))) / M_PI * 180;
  desireAngle_array[2] = -(180 - acos((pow(SERVO_LENGTH[1], 2) + pow(SERVO_LENGTH[2], 2) - pow(y_reference, 2) - pow(z_reference, 2)) / (2 * SERVO_LENGTH[1] * SERVO_LENGTH[2])) / M_PI * 180);
  desireAngle_array[3] = angle_final;
  
  if (is_singular(point[0], point[1],  desireAngle_array))
    return true;
  else{
    for(int i = 0; i < 4; i++)
      desireAngle_array[i] = SERVO_READY_STATE[i];
    return false;
  }
}

bool Arm::is_singular(float desire_y, float desire_z, float desireAngle_array[]){
  float y = 0, z = 0, error_y, error_z;
  float theta = 0, offset = 2;
  for(int index=0; index<3; index++){
    theta += desireAngle_array[index];
    y += SERVO_LENGTH[index] * cos(theta / 180 * PI);
    z += SERVO_LENGTH[index] * sin(theta / 180 * PI);
  }
  error_y = abs(y - desire_y);
  error_z = abs(z - desire_z);
  if(error_y < offset && error_z < offset)
    return true;
  return false;
}

void Arm::Routine(){
  switch (workType) {
    case 0:
      break;
    case 111:
      if(moveServoGroup(-1, SERVO_GETBACK_STATE))
        workType = 0;
      break;
    case 112:
      if(moveServoGroup(-1, SERVO_READY_STATE))
        workType = 0;
      break;
    case 121:
    case 122:
      if(moveServoGroup(-1, serial_Angle_array))
        workType = 0;
      break;
    case 221:
    case 222:
      if(Move_series(3))
        workType = 0;
      break;
      
    case 311:
      if(fantasyBaby())
        workType = 0;
      break;
    default:
      workType = 112;
      break;
  }
}

bool Arm::fantasyBaby() {
  static const float MOTION[4][5] = {{65, 0, 0, 50, -1}, {0, 0, 0, 50, -1}, {0, 0 , -90, 50, -1}, {65, -90, -70, 50, -1}};
  for(int i = 0 ; i < 4 ; i++){
    for(int j = 0 ; j < 5 ; j++)
       motion_array[i][j] = MOTION[i][j];
  }
  Move_series(4);
}

bool Arm::Move_series(int motion_size) {
  const uint32_t period = 250;
  static uint32_t last_motion_time;
  static int motion_step = 0;
  
  if(moveServoGroup(motion_array[motion_step][4], motion_array[motion_step]))
    if(timer >= last_motion_time + period){
      motion_step++;
      if(motion_step >= motion_size){
        motion_step = 0;
        return true;
      }
    }
  else{
    last_motion_time = timer;
  }
  return false;
}

bool Arm::moveServoGroup(int order, float desireAngle_array[]){
  int index_order[2][4] = {{0, 1, 2, 3}, {3, 2, 1, 0}}; // -1 for no order  
  for(int i = 0 ; i < 4 ; i++)
    set_desire_angle(i, desireAngle_array[i]);
  if(order == -1)
    servo[0].enable = servo[1].enable = servo[2].enable = servo[3].enable = true;
  else{
    servo[0].enable = servo[1].enable = servo[2].enable = servo[3].enable = false;
    if( !servo[index_order[order][0]].is_stable() )
      servo[index_order[order][0]].enable = true;
    else if( !servo[index_order[order][1]].is_stable() )
      servo[index_order[order][1]].enable = true;
    else if( !servo[index_order[order][2]].is_stable() )
      servo[index_order[order][2]].enable = true;
    else if( !servo[index_order[order][3]].is_stable() )
      servo[index_order[order][3]].enable = true;
  }
  if(is_motion_finish())
    return true;
  caculateYZ();
  return false;
}

void Arm::caculateYZ(){
  y = z = 0;
  for(int index=0; index<3; index++){
    theta += servo[index].desire_angle;
    y += SERVO_LENGTH[index] * cos(theta / 180 * PI);
    z += SERVO_LENGTH[index] * sin(theta / 180 * PI);
  }
}

void Arm::set_desire_angle(int servo_index, float desire_angle){
  if(desire_angle != servo[servo_index].desire_angle){
    servo[servo_index].desire_angle = desire_angle;
    desire_angle *= SERVO_POSITIVE[servo_index];    
    desire_angle += SERVO_OFFSET[servo_index];
    desire_angle = (desire_angle >= SERVO_LOWER_BOUND[servo_index]) ? desire_angle : SERVO_LOWER_BOUND[servo_index];
    desire_angle = (desire_angle <= SERVO_UPPER_BOUND[servo_index]) ? desire_angle : SERVO_UPPER_BOUND[servo_index];
    servo[servo_index].pwm_desire = transform(desire_angle);
  }
}

void Arm::now_angle(){
  for(int i = 0 ; i < 4 ; i++){
    servo[i].now_angle = ( i_transform(servo[i].pwm_past) - SERVO_OFFSET[i] ) * SERVO_POSITIVE[i];
  }  
}
void Arm::Arm_Control(){
  for(int servo_index = 0 ; servo_index < 4 ; servo_index++){
    if(!servo[servo_index].is_stable()){
      if(servo[servo_index].enable){
        if((servo[servo_index].pwm_desire - servo[servo_index].pwm_past) > SERVO_SPEED)
          servo[servo_index].pwm_past += SERVO_SPEED;
        else if((servo[servo_index].pwm_desire - servo[servo_index].pwm_past) < -SERVO_SPEED)
          servo[servo_index].pwm_past -= SERVO_SPEED;
        else
          servo[servo_index].pwm_past = servo[servo_index].pwm_desire;
        servo[servo_index].myservo.writeMicroseconds(servo[servo_index].pwm_past);
      }
    }
  }
  now_angle();
}
void Arm::init(){
  servo[0].myservo.attach(SERVO1_PIN, 500, 2500); // 修正脈衝寬度範圍
  servo[1].myservo.attach(SERVO2_PIN, 500, 2500); // 修正脈衝寬度範圍
  servo[2].myservo.attach(SERVO3_PIN, 500, 2500); // 修正脈衝寬度範圍
  servo[3].myservo.attach(SERVO4_PIN, 500, 2500); // 修正脈衝寬度範圍
  float angle_array[4] = {120, -60, -60, 30};
  moveServoGroup(-1, angle_array);
}
