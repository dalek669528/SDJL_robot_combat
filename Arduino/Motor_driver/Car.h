#ifndef _WHEEL_H_
#define _WHEEL_H_

//定义引脚名称 
#define EN            A1    //使能输出引脚，该引脚时高电平才允许控制直流电机，低电平时电机停止
#define AD            A0    //PWM输入引脚，读取电池电压
#define MotorA1 8     //PWM输出引脚，控制直流电机A
#define MotorA2 13    //Dig输出引脚，控制直流电机A
#define MotorB1 9     //PWM输出引脚，控制直流电机B
#define MotorB2 12    //Dig输出引脚，控制直流电机B
#define MotorC1 10    //PWM输出引脚，控制直流电机C
#define MotorC2 11    //Dig输出引脚，控制直流电机C
#define MotorD1 6     //PWM输出引脚，控制直流电机D
#define MotorD2 7     //Dig输出引脚，控制直流电机D

#define SPD_INT_A1 18
#define SPD_INT_A2 14
#define SPD_INT_B1 19
#define SPD_INT_B2 15
#define SPD_INT_C1 20
#define SPD_INT_C2 16
#define SPD_INT_D1 21
#define SPD_INT_D2 17

#define CPR 390 //count per round
#define TIRE_RADIUS 3 //3cm
#define MAX_PWM 128
#define W 12.5
#define L 10

class Wheel{
    public:
        int MAX_V = 30;
        int pwm = 0;
        long encoder = 0, encoder_past = 0;
        float Kp = 0, Ki = 0, Kd = 0;
        float delta_x = 0, v = 0;
        float desire_V = 0;
        uint32_t SpeedTimer;
        float err = 0, err_sum = 0, err_past;
        Wheel(){
            SpeedTimer = millis();
        }
        void set_PID(float p, float i, float d){
            Kp = p;
            Ki = i;
            Kd = d;
        }
        void speed_renew(uint32_t timer){
            delta_x = (float)(encoder - encoder_past) / CPR * PI * 2 * TIRE_RADIUS;
            v = delta_x / (timer-SpeedTimer)*1000; //cm/sec
            SpeedTimer = timer;
            encoder_past = encoder;
        }
        void pwm_calculate(){
            float desire_V_temp = desire_V;
            
            desire_V_temp = (desire_V_temp > MAX_V) ? MAX_V : desire_V_temp;
            desire_V_temp = (desire_V_temp < -MAX_V) ? -MAX_V : desire_V_temp;
            
            err = desire_V_temp - v;
            err_sum += err;
            pwm = Kp * err + Ki * err_sum + Kd * (err - err_past);
            err_past = err;
        }
        void reset_error(){
            err = 0;
            err_sum = 0;
            err_past = 0;
            pwm = 0;
        }
};

class Car{
public:
    
    Wheel A, B, C, D;
    float X = 0, Y = 0, theta = 0;
    float Vx = 0, Vy = 0, w = 0;
    float desire_X = 0, desire_Y = 0, desire_theta = 0;
    float desire_Vx = 0, desire_Vy = 0, desire_w = 0;
    
    float pos_err[3] = {0, 0, 0};
    float pos_err_sum[3] = {0, 0, 0};
    float pos_err_past[3] = {0, 0, 0};
    float p_Kp = 1, p_Ki = 0, p_Kd = 4; 

    int control_type = 0, past_control_type = 0;

    Car(){
        A.set_PID(1, 0.5, 2);
        B.set_PID(1, 0.5, 2);
        C.set_PID(1, 0.5, 2);
        D.set_PID(1, 0.5, 2);
    }
    void Car_Control();
    void PWM_Calculate();
    void Serial_r(String str);
    void printInfo();
    void position_PID();
    void car_stop(){
        A.desire_V = B.desire_V = C.desire_V = D.desire_V = 0;
    }
    void reset_error(){
        A.reset_error();
        B.reset_error();
        C.reset_error();
        D.reset_error();
        pos_err[0] = pos_err[1] = pos_err[2] = 0;
        pos_err_past[0] = pos_err_past[1] = pos_err_past[2] = 0;
        pos_err_sum[0] = pos_err_sum[1] = pos_err_sum[2] = 0;
    }
    void reset(){
        control_type = -2;
        car_stop();
        reset_error();
        X = 0, Y = 0, theta = 0;
        Vx = 0, Vy = 0, w = 0;
        desire_X = 0, desire_Y = 0, desire_theta = 0;
        desire_Vx = 0, desire_Vy = 0, desire_w = 0;
    }
};




#endif
