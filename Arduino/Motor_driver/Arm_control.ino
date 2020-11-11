void Arm::Routine(){
  switch(routine_state){
    case 0:
      break;
    case 1:
      if(autoPick())
        routine_state = 0;
      break;
    case 2:
      if(fantasyBaby())
        routine_state = 0;
      break;
  }
}

bool Arm::fantasyBaby() {

  static const float MOTION[3][4] = {{40, -30, 0, 30}, {33, -30 , 0, 30}, {33, -50, -90, 30}};
  const uint32_t period = 500;
  static uint32_t last_motion_time;
  static int motion_step = 0;
  if (motion_step == 2)
    moveServoGroup(1, MOTION[motion_step]);
  else
    moveServoGroup(0, MOTION[motion_step]);
  if(is_motion_finish())
    if(timer >= last_motion_time + period){
      motion_step++;
      if(motion_step >=3){
        return true;
      }
    }
  else{
    last_motion_time = timer;
  }
  return false;
}


bool Arm::autoPick() {
  const float MOTION[3][4] = {{120, 60, 30, 30}, {30, 60, 30, 90}, {120, 60, 30, 90}};
  const uint32_t period = 500;
  static uint32_t last_motion_time;
  static int motion_step = 0;
  
  moveServoGroup(0, MOTION[motion_step]);
  if(is_motion_finish())
    if(timer >= last_motion_time + period){
      motion_step++;
      if(motion_step >=3){
        return true;
      }
    }
  else{
    last_motion_time = timer;
  }
  return false;
}


bool Arm::is_YZ_safe(float desire_y, float desire_z, float desireAngle_array[]){
  float y = 0, z = 0, error_y, error_z;
  float theta = 0, offset = 5;
  for(int index=0; index<3; index++){
    theta += desireAngle_array[index];
    y += SERVO_LENGTH[index] * cos(theta / 180 * M_PI);
    z += SERVO_LENGTH[index] * sin(theta / 180 * M_PI);
  }   
  error_y = ((y - desire_y) > 0) ? (y - desire_y) : -(y - desire_y);
  error_z = ((z - desire_z) > 0) ? (z - desire_z) : -(z - desire_z);
  
  if(error_y < offset && error_z < offset)
    return true;
  return false;
}

void Arm::moveServoGroup(int order, float desireAngle_array[]){
  int index_order[2][4] = {{0, 1, 2, 3}, {3, 2, 1, 0}}; // -1 for no order  
  for(int i = 0 ; i < 4 ; i++)
    set_desire_angle(i, desireAngle_array[i]);
  if(order == -1)
    servo[0].enable = servo[1].enable = servo[2].enable = servo[3].enable = true;
  else{
    servo[0].enable = servo[1].enable = servo[2].enable = servo[3].enable = false;
    if(servo[index_order[order][0]].desire_angle != desireAngle_array[index_order[order][0]])
      servo[index_order[order][0]].enable = true;
    else if(servo[index_order[order][1]].desire_angle != desireAngle_array[index_order[order][1]])
      if(servo[index_order[order][0]].stable)
        servo[index_order[order][1]].enable = true;
    else if(servo[index_order[order][2]].desire_angle != desireAngle_array[index_order[order][2]])
      if(servo[index_order[order][0]].stable && servo[index_order[order][1]].stable)
        servo[index_order[order][2]].enable = true;
    else if(servo[index_order[order][3]].desire_angle != desireAngle_array[index_order[order][3]])
      if(servo[index_order[order][0]].stable && servo[index_order[order][1]].stable && servo[index_order[order][2]].stable)
        servo[index_order[order][3]].enable = true;
  }
  caculateYZ();
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
    servo[servo_index].stable = false;
    desire_angle *= SERVO_POSITIVE[servo_index];    
    desire_angle += SERVO_OFFSET[servo_index];
    desire_angle = (desire_angle >= SERVO_LOWER_BOUND[servo_index]) ? desire_angle : SERVO_LOWER_BOUND[servo_index];
    desire_angle = (desire_angle <= SERVO_UPPER_BOUND[servo_index]) ? desire_angle : SERVO_UPPER_BOUND[servo_index];
    servo[servo_index].pwm_desire = transform(desire_angle);
  }
}

void Arm::Arm_Control(){
  for(int servo_index = 0 ; servo_index < 4 ; servo_index++){
    if(servo[servo_index].pwm_desire != servo[servo_index].pwm_past){
      servo[servo_index].stable = false;
      if(servo[servo_index].enable){
        if((servo[servo_index].pwm_desire - servo[servo_index].pwm_past) % servo_speed != 0){
          servo[servo_index].pwm_past += (servo[servo_index].pwm_desire - servo[servo_index].pwm_past) % servo_speed;
        }
        else if(servo[servo_index].pwm_desire > servo[servo_index].pwm_past)
          servo[servo_index].pwm_past += servo_speed;
        else 
          servo[servo_index].pwm_past -= servo_speed;      
        servo[servo_index].myservo.writeMicroseconds(servo[servo_index].pwm_past);
      }
    }
    else{
      servo[servo_index].stable = true;
    }
//    printInfo(servo_index);
  }
}

Arm::Arm(){
  servo[0].myservo.attach(SERVO1_PIN, 500, 2500); // 修正脈衝寬度範圍
  servo[1].myservo.attach(SERVO2_PIN, 500, 2500); // 修正脈衝寬度範圍
  servo[2].myservo.attach(SERVO3_PIN, 500, 2500); // 修正脈衝寬度範圍
  servo[3].myservo.attach(SERVO4_PIN, 500, 2500); // 修正脈衝寬度範圍
  float angle_array[4] = {120, -60, -60, 30};
  for(int i=0;i<4;i++)
    servo[i].pwm_past = transform(angle_array[i]);
  moveServoGroup(1, angle_array);
}
