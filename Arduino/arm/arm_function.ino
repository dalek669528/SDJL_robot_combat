//Tranform angle(0~180) to pwm(500~2500) 
int transform(float angle){
  return 500 + int(angle/180*2000);
}

int itransform(float pwm){
  return (pwm -500)*180/2000;
}

bool caculateYZ(float desire_y, float desire_z, float desireAngle_array[]){

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

void printInfo(int motor_index, float desire_angle, int pwm_desire, int pwm_past){
    Serial.print("Motor ");
    Serial.print(motor_index);
    Serial.print(" : angle desire : ");
    Serial.print(desire_angle - SERVO_OFFSET[motor_index]);
    Serial.print(" : pwm desire : ");
    Serial.print(pwm_desire);
    Serial.print("  pwm now : ");
    Serial.println(pwm_past);
}

void moveServoGroup(int order, float desireAngle_array[]){
  int index_order[2][4] = {{0, 1, 2, 3}, {3, 2, 1, 0}};
  for(int index=0; index<4; index++){
    moveServo(index_order[order][index], desireAngle_array[index_order[order][index]]);
  }  

  float y = 0, z = 0;
  float theta = 0;
  for(int index=0; index<3; index++){
    theta += desireAngle_array[index];
    y += SERVO_LENGTH[index] * cos(theta / 180 * M_PI);
    z += SERVO_LENGTH[index] * sin(theta / 180 * M_PI);
  }   

  Serial.print("y = ");
  Serial.print(y);
  Serial.print(", z = ");
  Serial.println(z);
}

void moveServo(int motor_index, float desire_angle){

    int pwm_desire, distance;
    Serial.print("desire_angle = ");
    Serial.println(desire_angle);

    desire_angle *= SERVO_POSITIVE[motor_index];

    Serial.print("desire_angle = ");
    Serial.println(desire_angle);
    
    desire_angle += SERVO_OFFSET[motor_index];
    
    Serial.print("desire_angle = ");
    Serial.println(desire_angle);
    desire_angle = (desire_angle>=SERVO_LOWER_BOUND[motor_index]) ? desire_angle : SERVO_LOWER_BOUND[motor_index];
    desire_angle = (desire_angle<=SERVO_UPPER_BOUND[motor_index]) ? desire_angle : SERVO_UPPER_BOUND[motor_index];
    Serial.print("desire_angle = ");
    Serial.println(desire_angle);
    
    pwm_desire = transform(desire_angle);
    distance   = pwm_desire -  motor_array[motor_index].pwm_past;
    
    motor_array[motor_index].pwm_past += distance%motor_speed;
    motor_array[motor_index].myservo.writeMicroseconds(motor_array[motor_index].pwm_past);
    delay(20);
    
    while(pwm_desire != motor_array[motor_index].pwm_past){ 
      if(distance>0) 
        motor_array[motor_index].pwm_past += motor_speed;
      else 
        motor_array[motor_index].pwm_past -= motor_speed;
      
      motor_array[motor_index].myservo.writeMicroseconds(motor_array[motor_index].pwm_past);
      delay(20);
      //printInfo(motor_index, desire_angle, pwm_desire, motor_array[motor_index].pwm_past);  
    }
    printInfo(motor_index, desire_angle, pwm_desire, motor_array[motor_index].pwm_past);  
}

void autoPick(){
    const float PICK_MOTION[3][4]= {{120,60,30,30}, {30,60,30,90}, {120,60,30,90}};

    for(int motion_index=0; motion_index<3; motion_index++){
        //for(int motor_index=0; motor_index<4; motor_index++)
            //angle_array[motor_index] = PICK_MOTION[motion_index][motor_index];
        moveServoGroup(0, PICK_MOTION[motion_index]);
        //moveServo(0, PICK_MOTION[motion_index][0]);
        delay(500);
    }
}

void fantasyBaby(){

    const float FB_MOTION[3][4]= {{40,-30,0,30}, {33,-30 ,0,30}, {33,-50,-90,30}};
    int moveNumber = 5;
    int motionNumber = 3;
    for(int motion_index=0; motion_index<moveNumber*motionNumber; motion_index++){
        //for(int motor_index=0; motor_index<4; motor_index++)
        //    angle_array[motor_index] = FB_MOTION[motion_index%motionNumber][motor_index];
        if(motion_index == 2){
          moveServoGroup(1, FB_MOTION[motion_index%motionNumber]);
        }
        else
          moveServoGroup(0, FB_MOTION[motion_index%motionNumber]);
        delay(50);
    }
}

void movetoPoint(float angle, float point[]){
  
    float y_reference = point[0] - SERVO_LENGTH[0]* cos(angle / 180 * M_PI) + ARM_AXIS_OFFSET;
    float z_reference = point[1] - SERVO_LENGTH[0]* sin(angle / 180 * M_PI);
    float desireAngle_array[4];


    Serial.print("test ");
    Serial.print(SERVO_LENGTH[0]* sin(angle / 180 * M_PI));
    Serial.print(point[1]);

    Serial.print("y_reference ");
    Serial.print(y_reference);
    Serial.print(" , z_reference");
    Serial.print(z_reference);


    if(angle == 0){
        desireAngle_array[0] = angle ;
        desireAngle_array[1] = -desireAngle_array[0] + atan(z_reference/y_reference)/M_PI*180 + acos((pow(SERVO_LENGTH[1],2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2))))/M_PI*180;
        desireAngle_array[2] = -(180 - acos((pow(SERVO_LENGTH[1],2) + pow(SERVO_LENGTH[2], 2) - pow(y_reference, 2) - pow(z_reference, 2)) / (2*SERVO_LENGTH[1]*SERVO_LENGTH[2]))/M_PI*180);      
        desireAngle_array[3] = 30;
    }
    else{
        desireAngle_array[0] = angle ;
        //desireAngle_array[1] = -desireAngle_array[0] + atan(z_reference/y_reference)/M_PI*180 - acos((pow(SERVO_LENGTH[1],2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2))))/M_PI*180;
        //desireAngle_array[2] = 180 - acos((pow(SERVO_LENGTH[1],2) + pow(SERVO_LENGTH[2], 2) - pow(y_reference, 2) - pow(z_reference, 2)) / (2*SERVO_LENGTH[1]*SERVO_LENGTH[2]))/M_PI*180;

        desireAngle_array[1] = -desireAngle_array[0] + atan(z_reference/y_reference)/M_PI*180 + acos((pow(SERVO_LENGTH[1],2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2))))/M_PI*180;
        desireAngle_array[2] = -(180 - acos((pow(SERVO_LENGTH[1],2) + pow(SERVO_LENGTH[2], 2) - pow(y_reference, 2) - pow(z_reference, 2)) / (2*SERVO_LENGTH[1]*SERVO_LENGTH[2]))/M_PI*180); 
        
        //desireAngle_array[3] = 30;      
    }
   
    

    Serial.print(" 1 : ");
    Serial.print(-desireAngle_array[0]);
    Serial.print(" , 2 : ");
    Serial.print(atan(z_reference/y_reference)/M_PI*180);
    Serial.print(" , 3 : ");
    Serial.print((pow(SERVO_LENGTH[1],2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2))));
    Serial.println(acos((pow(SERVO_LENGTH[1],2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2))))/M_PI*180);
    
    for(int index=0; index<4; index++){
      desireAngle_array[index] = (desireAngle_array[index]>=-90 && desireAngle_array[index]<=90) ? desireAngle_array[index] : itransform(motor_array[index].pwm_past)-SERVO_OFFSET[index];
      if(index == 3)
        desireAngle_array[index] = itransform(motor_array[index].pwm_past)-SERVO_OFFSET[index];  
    }
    Serial.print(" Angle ");
    Serial.print(desireAngle_array[0]);
    Serial.print(" , ");
    Serial.print(desireAngle_array[1]);
    Serial.print(", ");
    Serial.print(desireAngle_array[2]);
    Serial.print(", ");
    Serial.println(desireAngle_array[3]);
    if(caculateYZ(point[0], point[1],  desireAngle_array) == true)
      moveServoGroup(1, desireAngle_array);
}
