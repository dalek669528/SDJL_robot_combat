/*
111                     -> move to {90,   80,   0,  30}
112                     -> move to {120, -60, -60,  30}
121 ang1 ang2 ang3 ang4 -> move to [ang1, ang2, ang3, ang4]
*/

void Arm::Serial_r(String str) {
  char* intput_string_c = str.c_str();
  
  if (str != "") {
    int workType = atoi( strtok(intput_string_c, " ") );
    char* substr = strtok(NULL, " ");
    switch (workType) {
      case 111:
        moveServoGroup(0, SERVO_GETBACK_STATE);
        break;
      case 112:
        moveServoGroup(0, SERVO_READY_STATE);
        break;
      case 121:
        float desireAngle_array[4] = {0};
        for(int i=0; i<4; i++){
          substr = strtok(NULL, " ");
          if(substr != NULL)
            desireAngle_array[i] = atof(substr);
          else
            break;
        }
        moveServoGroup(0, desireAngle_array);
        break;
      case 122:
        routine_state = 1;
        break;
      case 123:
        routine_state = 2;
        break;
        
      case 211:
        break;

      case 221:
//        float pointYZ[2];
//        do {
//          float axis = atof(substr);
//          pointYZ[counter] = axis;
//          substr = strtok(NULL, " ");
//          counter++;
//        } while (substr);
//
//        if (pointYZ[0] > ARM_PICK_LOWER_BOUND && pointYZ[0] < ARM_PICK_UPPER_BOUND) {
//          //pointYZ[1] = ARM_PICK_HEIGHT;
//          set_desire_angle(3, 30);
//          movetoPoint(0, pointYZ);
//          //Pick up
//          set_desire_angle(3, 60);
//          //
//          moveServoGroup(0, SERVO_PICKUP_STATE);
//        }
        break;

      case 222:
//        do {
//          float axis = atof(substr);
//          pointYZ[counter] = axis;
//          substr = strtok(NULL, " ");
//          counter++;
//        } while (substr);
//
//        movetoPoint(60, pointYZ);
//        set_desire_angle(3, 30);
//        moveServoGroup(0, SERVO_READY_STATE);
        break;

      case 231:
        break;

      default:
        break;
    }
  }
}


void Arm::printInfo(int servo_index) {
  Serial.print("Motor ");
  Serial.print(servo_index);
  Serial.print(" : angle desire : ");
  Serial.print(servo[servo_index].desire_angle);
  Serial.print(" : pwm desire : ");
  Serial.print(servo[servo_index].pwm_desire);
  Serial.print("  pwm now : ");
  Serial.println(servo[servo_index].pwm_past);
}

//void Arm::movetoPoint(float angle, float point[]) {
//
//  float y_reference = point[0] - SERVO_LENGTH[0] * cos(angle / 180 * M_PI) + ARM_AXIS_OFFSET;
//  float z_reference = point[1] - SERVO_LENGTH[0] * sin(angle / 180 * M_PI);
//  float desireAngle_array[4];
//
//
//  Serial.print("test ");
//  Serial.print(SERVO_LENGTH[0]* sin(angle / 180 * M_PI));
//  Serial.print(point[1]);
//
//  Serial.print("y_reference ");
//  Serial.print(y_reference);
//  Serial.print(" , z_reference");
//  Serial.print(z_reference);
//
//
//  if (angle == 0) {
//    desireAngle_array[0] = angle ;
//    desireAngle_array[1] = -desireAngle_array[0] + atan(z_reference / y_reference) / M_PI * 180 + acos((pow(SERVO_LENGTH[1], 2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2)))) / M_PI * 180;
//    desireAngle_array[2] = -(180 - acos((pow(SERVO_LENGTH[1], 2) + pow(SERVO_LENGTH[2], 2) - pow(y_reference, 2) - pow(z_reference, 2)) / (2 * SERVO_LENGTH[1] * SERVO_LENGTH[2])) / M_PI * 180);
//    desireAngle_array[3] = 30;
//  }
//  else {
//    desireAngle_array[0] = angle ;
//    //desireAngle_array[1] = -desireAngle_array[0] + atan(z_reference/y_reference)/M_PI*180 - acos((pow(SERVO_LENGTH[1],2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2))))/M_PI*180;
//    //desireAngle_array[2] = 180 - acos((pow(SERVO_LENGTH[1],2) + pow(SERVO_LENGTH[2], 2) - pow(y_reference, 2) - pow(z_reference, 2)) / (2*SERVO_LENGTH[1]*SERVO_LENGTH[2]))/M_PI*180;
//
//    desireAngle_array[1] = -desireAngle_array[0] + atan(z_reference / y_reference) / M_PI * 180 + acos((pow(SERVO_LENGTH[1], 2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2)))) / M_PI * 180;
//    desireAngle_array[2] = -(180 - acos((pow(SERVO_LENGTH[1], 2) + pow(SERVO_LENGTH[2], 2) - pow(y_reference, 2) - pow(z_reference, 2)) / (2 * SERVO_LENGTH[1] * SERVO_LENGTH[2])) / M_PI * 180);
//
//    //desireAngle_array[3] = 30;
//  }
//
//
//
//  Serial.print(" 1 : ");
//  Serial.print(-desireAngle_array[0]);
//  Serial.print(" , 2 : ");
//  Serial.print(atan(z_reference / y_reference) / M_PI * 180);
//  Serial.print(" , 3 : ");
//  Serial.print((pow(SERVO_LENGTH[1], 2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2))));
//  Serial.println(acos((pow(SERVO_LENGTH[1], 2) + pow(y_reference, 2) + pow(z_reference, 2) - pow(SERVO_LENGTH[2], 2)) / (2 * SERVO_LENGTH[1] * sqrt(pow(y_reference, 2) + pow(z_reference, 2)))) / M_PI * 180);
//
//  for (int index = 0; index < 4; index++) {
//    desireAngle_array[index] = (desireAngle_array[index] >= -90 && desireAngle_array[index] <= 90) ? desireAngle_array[index] : i_transform(servo[index].pwm_past) - SERVO_OFFSET[index];
//    if (index == 3)
//      desireAngle_array[index] = i_transform(servo[index].pwm_past) - SERVO_OFFSET[index];
//  }
//  Serial.print(" Angle ");
//  Serial.print(desireAngle_array[0]);
//  Serial.print(" , ");
//  Serial.print(desireAngle_array[1]);
//  Serial.print(", ");
//  Serial.print(desireAngle_array[2]);
//  Serial.print(", ");
//  Serial.println(desireAngle_array[3]);
//  if (is_YZ_safe(point[0], point[1],  desireAngle_array) == true)
//    moveServoGroup(1, desireAngle_array);
//}
