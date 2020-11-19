#ifndef _Arm_H_
#define _Arm_H_

#define S_CPR 390 //count per round
#define S_TIRE_RADIUS 3 //3cm
#define S_MAX_PWM 255

#define SERVO1_PIN A3
#define SERVO2_PIN A4
#define SERVO3_PIN A5
#define SERVO4_PIN A6

#define INT_S1 2
#define INT_S2 3
#define Motor_S1 4
#define Motor_S2 5
#define button A8
#define Vcc A9
#define Gnd A10

#include <Servo.h>


class Slide{
public:
    bool is_init = false;
    int pwm, control_type;
    long encoder;
    float Kp, Ki, Kd;
    float Kp_b, Ki_b, Kd_b;
    int desire_encode;
    int MAX_ENCODER, MIN_ENCODER;
    float err, err_sum, err_past;
    
    Slide();
    void set_PID(float p, float i, float d, float pb, float ib, float db);
    void PWM_Calculate();
    void Slide_Control();
    void Serial_r(String str);
    void printInfo();
    void reset_error();
    void reset(){
        reset_error();
        is_init = false;
    }
    
};

class servo_struct {
    public:
        Servo myservo;
        bool enable = true;
        bool is_stable(){return (pwm_past == pwm_desire);}
        float desire_angle = 0;
        float now_angle = 0;
        int pwm_past = 1500; //transform(90)
        int pwm_desire = 1500; //transform(90)
};

class Arm{
    public:
        bool is_fantasy = false;
        servo_struct servo[4];
        const float SERVO_SPEED_INIT = 30;
        float SERVO_SPEED;
        float Y = 0, Z = 0, Theta = 0;
        float pointYZ[2] = {0, 0};
        int workType = 0;
        float serial_Angle_array[4] = {0};
        float motion_array[32][5] = {0};

        Arm(){}
        void Arm::init();
        void Arm_Control();
        void printInfo(int servo_index);
        void Serial_r(String str);
        void now_angle();
        void caculateYZ();
        void Routine();
        
        bool movetoPoint(float angle, float angle_final, float point[], float desireAngle_array[]);
        void set_desire_angle(int servo_index, float desire_angle);
        bool moveServoGroup(int order, float desireAngle_array[]);
        bool Move_series(int motion_size, uint32_t period = 250);
        bool fantasyBaby();
        
        void reset_motion(){
            for(int i =0 ; i < 32 ; i++){
                motion_array[i][0] = SERVO_READY_STATE[0];
                motion_array[i][1] = SERVO_READY_STATE[1];
                motion_array[i][2] = SERVO_READY_STATE[2];
                motion_array[i][3] = SERVO_READY_STATE[3];
            }
        }
        bool is_n_singular(float desire_y, float desire_z, float desireAngle_array[]);
        bool is_motion_finish(){
            return( workType == 0 ) ;
        }
        bool is_move_finish(){
            return( servo[0].is_stable() && servo[1].is_stable() && servo[2].is_stable() && servo[3].is_stable());
        }
        int transform(float angle){
            return 500 + int(angle/180*2000);
        }
        int i_transform(float pwm){
            return (pwm - 500)*180/2000;
        }
        
        
        //Servo const variable
        const int SERVO_POSITIVE[4]       = {-1,    1,  1,  1};
        const int SERVO_OFFSET[4]         = {184,   90, 90, 0};
        const int SERVO_LOWER_BOUND[4]    = {30,    0,  0,  00};
        const int SERVO_UPPER_BOUND[4]    = {184, 180, 180, 90};
        
        //const uint8_t SERVO_INIT_STATE[4]    = {180, 180, 180,    90};
        
        //Servo state
        const float     SERVO_GETBACK_STATE[4]   = {90, 80, 0, 30};
        const float     SERVO_READY_STATE[4]     = {120, -60, -60, 30};
        const float     SERVO_PICKUP_STATE[4]    = {120, -60, -60, 60};
        const float     SERVO_SINGLUAR_STATE[4]  = {120, -60, -60, 90};
        const float     SERVO_LENGTH[3]          = {12.2, 9.3, 13};
        const float     ARM_AXIS_OFFSET[2]       = {5, -17};
        const float     ARM_PUSH_OFFSET          = -4.5;
        
        //Pick const variable
        const float     ARM_PICK_HEIGHT             = 14;
        const float     ARM_PICK_LOWER_BOUND    = 12;
        const float     ARM_PICK_UPPER_BOUND    = 40;

};
#endif
