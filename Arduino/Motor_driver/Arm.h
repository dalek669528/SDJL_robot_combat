#ifndef _Arm_H_
#define _Arm_H_

#include <Servo.h>

struct servo_struct {
    Servo myservo;
    bool enable = true;
    bool stable = false;
    float desire_angle = 0;
    int pwm_past = 1500; //transform(90)
    int pwm_desire = 1500; //transform(90)
};

class Arm{
public:

  const int servo_speed = 20;
  float y = 0, z = 0, theta = 0;
  int routine_state = 0;
  servo_struct servo[4];
  
  Arm();
  void Arm_Control();
  void set_desire_angle(int servo_index, float desire_angle);
  void Routine();
  
  void caculateYZ();
  void printInfo(int servo_index);
  void Serial_r(String str);
  void moveServoGroup(int order, float desireAngle_array[]);
  bool autoPick();
  bool fantasyBaby();
  
  bool is_YZ_safe(float desire_y, float desire_z, float desireAngle_array[]);
  void movetoPoint(float angle, float point[]);
  
  bool is_motion_finish(){
    return( servo[0].stable && servo[1].stable && servo[2].stable && servo[3].stable);
  }
  int transform(float angle){
    return 500 + int(angle/180*2000);
  }
  int i_transform(float pwm){
    return (pwm -500)*180/2000;
  }
  
  //Servo const variable
  const int SERVO_POSITIVE[4]     = {1,    -1,  -1,   1};
  const int SERVO_OFFSET[4]       = {0,    90,  90,   0};
  const int SERVO_LOWER_BOUND[4]  = {0,     0,   0,  30};
  const int SERVO_UPPER_BOUND[4]  = {180, 180, 180,  90};
  //const uint8_t SERVO_INIT_STATE[4]  = {180, 180, 180,  90};
  
  //Servo state
  const float   SERVO_GETBACK_STATE[4] = {90,   80,   0,  30};
  const float   SERVO_READY_STATE[4]   = {120, -60, -60,  30};
  const float   SERVO_PICKUP_STATE[4]  = {120, -60, -60,  60};
  const float   SERVO_LENGTH[3]        = {10.6, 7.8, 14};
  //const float   ARM_AXIS_OFFSET       = 6.9;
  const float   ARM_AXIS_OFFSET        = 0;
  
  //Pick const variable
  const float   ARM_PICK_HEIGHT       = 14;
  const float   ARM_PICK_LOWER_BOUND  = 12;
  const float   ARM_PICK_UPPER_BOUND  = 40;

};
#endif
